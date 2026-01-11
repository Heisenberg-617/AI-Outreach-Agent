import requests
import time
import json
import os
import asyncio
import sys
import re
import unicodedata
from urllib.parse import quote
from dotenv import load_dotenv
from openai import AsyncOpenAI
from settings import MODEL_NAME_PROSPECTION
# ✅ Path setup
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(override=True)

# ========================
# CONFIGURATION
# ========================
GOOGLE_PLACES_API_KEY = os.getenv("GOOGLE_API_KEY")
SCRAPINGBEE_API_KEY = os.getenv("SCRAPINGBEE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

RADIUS = 25000
OUTPUT_FILE = "data/real_prospects.json"

client = AsyncOpenAI(api_key=GROQ_API_KEY, base_url="https://api.groq.com/openai/v1")

CITIES = [{"name": "Rabat", "lat": 34.0209, "lng": -6.8416}] 
QUERIES = ["dentist", "cabinet dentaire", "gym", "fitness center"] # Example categories

# ========================
# HELPERS: CLEANING & EXTRACTION
# ========================

def clean_query_text(text: str):
    """Normalize unicode and remove symbols for URL safety."""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s\-]', ' ', text)
    words = text.split()
    return " ".join(words[:6])

def is_real_website(url):
    """Checks if the website is an actual business domain or just a directory."""
    if not url: return False
    url = url.lower()
    directories = [
        'facebook.com', 'instagram.com', 'mondentiste.ma', 'dabadoc.com', 
        'medicalis.ma', 'telecontact.ma', 'yellowpages', 'linkedin.com',
        'pnd.ma', 'etablissements.ma', 'voiladoc.ma', 'docdiali.com', 
        'dentisto.ma', 'nabady.ma','youtube.com', 'tiktok.com', 'marocannuaire.ma'
    ]
    return not any(d in url for d in directories)

def filter_moroccan_mobile(phone):
    """Only allow mobile numbers starting with 06, 07 or +212 6/7."""
    if not phone: return None
    clean_phone = re.sub(r'[^\d+]', '', phone)
    # Check for +212 6/7 or 06/07
    if re.match(r'^(\+212|0)[67]', clean_phone):
        return clean_phone
    return None

def extract_emails_via_regex(text: str):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    found = set(re.findall(email_pattern, text))
    
    blacklist = [
        'medicalis.ma', 'mondentiste.ma', 'dabadoc.com', 'telecontact.ma', 
        'wix', 'sentry', 'google', 'facebook', 'instagram', 'domain.com',
        'example.com', 'sitemap', 'kerix.net', 'e-rdv.ma','docexpress.ma', 
        'voiladoc.ma','detaire.ma', 'support', 'info@salle',
        'noreply', 'job', 'email.com'
    ]
    
    clean = []
    for e in found:
        e_low = e.lower()
        if not any(b in e_low for b in blacklist):
            if not e_low.endswith(('.png', '.jpg', '.js', '.css', '.webp')):
                clean.append(e_low)
    return list(set(clean))

# ========================
# SCRAPING & PLACES
# ========================

def search_places(query, location, page_token=None):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": query, "location": location, "radius": RADIUS, "key": GOOGLE_PLACES_API_KEY}
    if page_token: params["pagetoken"] = page_token
    try:
        return requests.get(url, params=params).json()
    except: return {}

def get_place_details(place_id):
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id, 
        "fields": "name,formatted_address,website,types,rating,user_ratings_total,international_phone_number", 
        "key": GOOGLE_PLACES_API_KEY
    }
    return requests.get(url, params=params).json().get("result", {})

def perform_single_scrape(name, city) -> dict:
    clean_name = clean_query_text(name)
    search_q = f"{clean_name} {city} email contact"
    encoded_q = quote(search_q)
    url = f"https://app.scrapingbee.com/api/v1/google?api_key={SCRAPINGBEE_API_KEY}&search={encoded_q}&language=fr&country_code=ma"
    
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code != 200: return {"context": "", "raw_emails": []}
        data = resp.json()
        context = [f"{res.get('title')} - {res.get('description')}" for res in data.get("organic_results", [])]
        found_emails = extract_emails_via_regex(json.dumps(data))
        return {"context": "\n".join(context), "raw_emails": found_emails}
    except: return {"context": "", "raw_emails": []}

# ========================
# AI PROCESSING
# ========================

async def ai_decision(name, city, context, raw_emails):
    prompt = f"""
Business: {name} in {city}
Found Emails: {raw_emails}
Search Context: {context[:2000]}

TASK:
1. Select the direct email for this business.
2. ACCEPT: Gmails/Official domains matching the business or owner.
3. REJECT: Directory platforms (medicalis, mondentiste, ma-salle, etc).

Respond ONLY in JSON:
{{"email": "chosen_email_or_null", "owner_name": "Name_or_null"}}
"""
    try:
        resp = await client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={ "type": "json_object" }
        )
        return json.loads(resp.choices[0].message.content)
    except: return {"email": None, "owner_name": None}


async def ai_verify_website(business_name, city, website_url, serp_context):
    """
    Second opinion from AI to ensure we don't skip leads with 'fake' websites.
    """
    if not website_url: return {"has_official_website": False}
    
    prompt = f"""
Business: "{business_name}" in {city}
Website found in Google: {website_url}
Search Context: {serp_context[:1500]}

TASK: Is the link '{website_url}' an OFFICIAL, PRIVATE website for this specific business?
- REJECT (False): Facebook, Instagram, LinkedIn, Dabadoc, Medicalis, or any directory.
- ACCEPT (True): A dedicated domain like 'www.clinique-dentaire-xyz.ma'.

Respond ONLY in JSON:
{{"has_official_website": true/false}}
"""
    try:
        resp = await client.chat.completions.create(
            model=MODEL_NAME_PROSPECTION,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_format={ "type": "json_object" }
        )
        return json.loads(resp.choices[0].message.content)
    except:
        return {"has_official_website": True} # Default to skip if AI fails to be safe
    
# ========================
# MAIN LOOP
# ========================

async def run_discovery():
    # --- LOAD EXISTING DATA ---
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            prospects = json.load(f)
            print(f"📂 Loaded {len(prospects)} existing leads.")
    else:
        prospects = []

    seen_ids = {p.get('place_id') for p in prospects}

    for city in CITIES:
        print(f"\n🌍 Processing: {city['name']}")
        for q in QUERIES:
            print(f"🔎 Query: {q}")
            data = search_places(q, f"{city['lat']},{city['lng']}")
            
            for place in data.get("results", []):
                pid = place['place_id']
                if pid in seen_ids: continue
                seen_ids.add(pid)

                details = get_place_details(pid)
                name = details.get("name")
                website = details.get("website")
                
                # 1. Preliminary check with Python list (fast)
                preliminary_is_real = is_real_website(website)
                
                # 2. Scrape anyway to get context for the AI
                scrape = perform_single_scrape(name, city['name'])
                
                # 3. If Python thought it was a real website, ask AI to double-check
                if website and preliminary_is_real:
                    ai_web_check = await ai_verify_website(name, city['name'], website, scrape['context'])
                    if ai_web_check.get("has_official_website") is True:
                        print(f"    ⏭️ Skipping {name}: AI confirmed official website ({website})")
                        continue
                    else:
                        print(f"    ℹ️ {name}: AI flagged website as directory/low-quality. Proceeding...")
                scrape = perform_single_scrape(name, city['name'])
                
                # Try to get mobile phone from Google
                mobile_phone = filter_moroccan_mobile(details.get("international_phone_number"))

                # AI Decision on emails
                decision = {"email": None, "owner_name": None}
                if scrape["raw_emails"]:
                    print(f"    🔎 Debug Found: {scrape['raw_emails']}")
                    decision = await ai_decision(name, city['name'], scrape['context'], scrape['raw_emails'])

                email = decision.get("email")
                
                # ONLY SAVE if we have an Email OR a Mobile Phone
                if (email and "@" in email and "null" not in email.lower()) or mobile_phone:
                    entry = {
                        "place_id": pid,
                        "name": name,
                        "category": q.title(),
                        "rating": details.get("rating"),
                        "reviews": details.get("user_ratings_total"),
                        "email": email if email and "@" in email else "unavailable",
                        "phone": mobile_phone if mobile_phone else "unavailable",
                        "owner": decision.get("owner_name"),
                        "city": city['name'],
                        "address": details.get("formatted_address")
                    }
                    prospects.append(entry)
                    print(f"    ✅ MATCH: {name} | Email: {entry['email']} | Phone: {entry['phone']}")
                    
                    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                        json.dump(prospects, f, indent=2, ensure_ascii=False)
                else:
                    print(f"    ❌ {name}: No valid contact found.")

if __name__ == "__main__":
    asyncio.run(run_discovery())