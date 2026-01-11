# 🤖 AI Outreach Agent - Moroccan Business Prospection & Cold Email Automation

An intelligent, multi-agent system that automates B2B prospection and cold email outreach for Moroccan SMEs. This system discovers businesses without websites, extracts contact information, generates personalized French cold emails, and sends them automatically.

**Made by:** Baddy Reda | UM6P Student | AI & Agents Enthusiast

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Step 1: Get API Keys](#step-1-get-api-keys)
  - [Step 2: Clone & Environment Setup](#step-2-clone--environment-setup)
  - [Step 3: Install Dependencies](#step-3-install-dependencies)
  - [Step 4: Configure Settings](#step-4-configure-settings)
  - [Step 5: Run the System](#step-5-run-the-system)
- [API Keys Guide](#api-keys-guide)
- [Project Structure](#project-structure)
- [Agent Architecture](#agent-architecture)
- [Usage Examples](#usage-examples)
- [Troubleshooting](#troubleshooting)
- [Security Best Practices](#security-best-practices)
- [Cost Considerations](#cost-considerations)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## 🎯 Overview

This system automates the entire prospection and outreach workflow:

1. **Discovery Agent** → Finds Moroccan businesses without websites
2. **Copywriter Agent** → Generates personalized French cold emails
3. **Outreach Manager** → Orchestrates the workflow
4. **Sender Agent** → Delivers emails via Gmail

The system uses **Groq's high-speed LLM models** for fast processing, **Google Places API** for business discovery, and **ScrapingBee** for web scraping contact information.

---

## ✨ Features

- ✅ **Automated Business Discovery** - Find SMEs in Morocco using Google Places API
- ✅ **Smart Website Detection** - Identify businesses WITHOUT official websites
- ✅ **Contact Extraction** - Extract owner names and emails using AI
- ✅ **Personalized Cold Emails** - Generate formal French emails using Groq LLMs
- ✅ **Multi-Agent Orchestration** - Seamless handoffs between specialized agents
- ✅ **Automatic Email Sending** - Direct Gmail SMTP integration
- ✅ **Persistent Storage** - Save prospects in JSON for tracking
- ✅ **Duplicate Prevention** - Avoid re-prospecting the same businesses
- ✅ **Batch Processing** - Process multiple prospects asynchronously

---

## 🏗️ Architecture

### Multi-Agent System


```
┌─────────────────────────────────────────────────────────────┐
│                    TWO-STAGE SYSTEM                         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                ┌──────┴──────────────┐
                │                     │
         ┌──────▼──────┐       ┌──────▼────────────────┐
         │  Discovery  │       │  Outreach Pipeline    │
         │   Agent     │─────▶│ (Iterative Loop)      │
         │             │       │                       │
         │ • Google    │       │ ┌─────────────────┐   │
         │   Places    │       │ │ Outreach Manager│◀─┼── prospects.json
         │ • Scraping  │       │ │                 │   │
         │ • Contact   │       │ │ • Calls         │   │
         │   Extract   │       │ │   Copywriter    │   │
         │ • Website   │       │ │ • Handoff to    │   │
         │   Check     │       │ │   Sender Agent  │   │
         └──────┬──────┘       │ └─────────────────┘   │
                │              │     │                 │
                │              │     ▼                 │
                ▼              │  ┌───────────────┐    │
         data/                 │  │  Sender       │    │
         prospects.json        │  │  Agent        │    │
                               │  │               │    │
                               │  │ • Personalize │    │
                               │  │ • Format      │    │
                               │  │ • Send        │    │
                               │  │               │    │
                               │  └───────────────┘    │
                               └───────────────────────┘

```

### Data Flow

```
Google Places API
      ↓
[Business Search] → [Website Check] → [Contact Extraction]
      ↓                    ↓                    ↓
[Google Details]    [AI Verification]   [Web Scraping]
      ↓                    ↓                    ↓
                    [Prospect JSON] → [Outreach Manager]
                                            ↓
                                    [Copywriter Agent]
                                            ↓
                                    [Email Generation]
                                            ↓
                                    [Sender Agent]
                                            ↓
                                    [Gmail SMTP] → 📧
```

---

## 📦 Prerequisites

- **Python 3.10+**
- **pip** (Python package manager)
- **Gmail Account** (for sending emails)
- **Internet connection** (for API calls)

**No local database needed** - all data stored in JSON files.

---

## 🚀 Setup Instructions

### Step 1: Get API Keys

You'll need 5 API keys/credentials. Follow each section carefully.

#### **1.1 Groq API Key** (LLM Provider)

1. Go to [Groq Console](https://console.groq.com/login)
2. Create an account or log in
3. Navigate to **API Keys** section (left sidebar)
4. Click **"Create API Key"**
5. Give it a name like `"ai-outreach-agent"`
6. Click **"Submit"**
7. **Copy the key immediately** (you won't see it again)
8. Save it somewhere safe

**Cost:** Free tier available (thousands of requests/month)

---

#### **1.2 Google Places API Key**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. **Create a new project:**
   - Click project dropdown (top left)
   - Click **"New Project"**
   - Name: `"AI Outreach Agent"`
   - Click **"Create"**
   - Wait for it to initialize

3. **Enable Places API:**
   - Click **"Enable APIs and Services"** (or search in search bar)
   - Search for **"Places API"**
   - Click the Places API result
   - Click **"Enable"**

4. **Create API Key:**
   - Go to **APIs & Services > Credentials**
   - Click **"+ Create Credentials"** (top left)
   - Choose **"API Key"**
   - Copy your key

5. **Enable required APIs:**
   - Enable **"Places API"** ✓
   - Enable **"Maps JavaScript API"** ✓

6. **(Optional) Set up billing:**
   - Google gives $200/month free credit
   - Add your payment method in **Billing** section
   - This is required for the API to work

**Cost:** $0.03-$0.17 per 1000 requests (covered by free credits)

---

#### **1.3 ScrapingBee API Key**

1. Go to [ScrapingBee](https://www.scrapingbee.com/)
2. Click **"Sign Up"** (top right)
3. Create account with email + password
4. Verify your email
5. Log in to dashboard
6. Go to **Account > API Key**
7. Copy your API key (looks like: `abc123xyz...`)

**Cost:** Free tier: 1,000 requests/month (perfect for testing)

---

#### **1.4 Gmail App Password**

For secure email sending without storing your main password:

1. Enable 2-factor authentication on your Gmail account:
   - Go to [myaccount.google.com/security](https://myaccount.google.com/security)
   - Look for **"2-Step Verification"**
   - Click it and follow the setup
   - You'll need to verify with your phone

2. Generate App Password:
   - Go back to **Security** page
   - Scroll down to **"App passwords"**
   - Select **Mail** and **Windows Computer** (or your device)
   - Google generates a 16-character password
   - Copy this password (spaces can be ignored)

3. Save it as `GMAIL_APP_PASSWORD` in your `.env` file

**Important:** Use your Gmail email address (not your main Google password) in the `.env` file.

---

### Step 2: Clone & Environment Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-outreach-agent.git
cd ai-outreach-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

---

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

**Key dependencies:**
- `groq>=0.15.0` - Groq SDK for LLMs
- `openai>=1.0.0` - OpenAI-compatible client
- `python-dotenv>=1.0.0` - Environment variable management
- `requests>=2.28.0` - HTTP requests
- `aiohttp>=3.8.0` - Async HTTP (included with agents SDK)
- `agents-ai>=0.1.0` - Groq Agents SDK

---

### Step 4: Configure Settings

#### **4.1 Create `.env` file**

In the project root directory, create a file named `.env`:

```bash
# .env file
# ==========================================
# API KEYS & CREDENTIALS
# ==========================================

# Groq (LLM Provider)
GROQ_API_KEY=your_groq_api_key_here

# Google Places API
GOOGLE_API_KEY=your_google_places_api_key_here

# ScrapingBee (Web Scraper)
SCRAPINGBEE_API_KEY=your_scrapingbee_api_key_here

# Gmail (SMTP Email Sending)
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password_here

# ==========================================
# OPTIONAL: MODEL PREFERENCES
# ==========================================

# Change these if you want different models
# Available Groq models:
# - mixtral-8x7b-32768 (balanced)
# - llama-2-70b-chat (strong reasoning)
# - gemma-7b-it (fast & lightweight)

GROQ_MODEL_MANAGER=mixtral-8x7b-32768
GROQ_MODEL_PROSPECTION=gemma-7b-it
GROQ_MODEL_SENDER=llama-2-70b-chat
```

**⚠️ Security:**
- **NEVER** commit `.env` to GitHub
- `.env` is already in `.gitignore`
- Keep these keys private

#### **4.2 Update `settings.py` (Optional)**

If you want different Groq models, edit `settings.py`:

```python
# settings.py
MODEL_NAME_MANAGER = "mixtral-8x7b-32768"          # Outreach orchestration
MODEL_NAME_PROSPECTION = "gemma-7b-it"             # Fast prospect research
MODEL_NAME_SENDER = "llama-2-70b-chat"             # Strong email formatting
```

**Available Groq Models (as of Jan 2026):**
- `mixtral-8x7b-32768` - Balanced, good for general tasks
- `llama-2-70b-chat` - Strong reasoning, best for copywriting
- `llama-3.1-70b-versatile` - Newest, fastest
- `gemma-7b-it` - Lightweight, great for speed

---

### Step 5: Run the System

#### **5.1 Start Discovery & Outreach**

```bash
# Make sure venv is activated
python main.py
```

This will:
1. Run Discovery Agent (finds prospects) ⏳ Takes 5-10 minutes
2. Load saved prospects from `data/prospects.json`
3. Run Outreach Manager for each prospect
4. Send emails via Gmail

#### **5.2 Monitor Progress**

Watch the terminal output:

```
=== Running Discovery Agent ===
🌍 Processing: Rabat
🔎 Query: dentist
  ✅ MATCH: Cabinet Dentaire Hassan | Email: hassan@clinic.ma
  ...

=== Starting Outreach ===

Processing prospect: Cabinet Dentaire Hassan
  ✅ Outreach result: Email sent successfully

=== Outreach Complete ===
```

---

## 📚 API Keys Guide

### Summary Table

| API | Purpose | Sign-up | Cost | Free Tier |
|-----|---------|---------|------|-----------|
| **Groq** | LLM inference | [console.groq.com](https://console.groq.com) | Pay-as-you-go | ✅ Free tier |
| **Google Places** | Business search | [console.cloud.google.com](https://console.cloud.google.com) | $0.03-0.17/1K | ✅ $200/mo credit |
| **ScrapingBee** | Web scraping | [scrapingbee.com](https://www.scrapingbee.com) | $0.01-0.05/req | ✅ 1000/mo free |
| **Gmail App Password** | Email sending | [myaccount.google.com](https://myaccount.google.com/security) | Free | ✅ Included |

### Troubleshooting API Keys

**❌ "GROQ_API_KEY is not set"**
- Check `.env` file exists
- Verify key is copied exactly
- Reload terminal after creating `.env`

**❌ "Invalid API key for Google Places"**
- Verify API is **enabled** in Google Cloud Console
- Check billing is set up
- Wait 5 minutes after creating API

**❌ "ScrapingBee API limit exceeded"**
- Upgrade to paid plan
- Or reduce CITIES/QUERIES in `discovery_agent.py`

**❌ "Gmail authentication failed"**
- Verify you used **App Password**, not main password
- Check 2FA is enabled
- Ensure Gmail address is correct in `.env`

---

## 📂 Project Structure

```
ai-outreach-agent/
│
├── main.py                          # Entry point - orchestrates everything
├── model.py                         # Groq client initialization
├── settings.py                      # Configuration & model names
├── parameters.py                    # Global parameters
│
├── My_agents/                       # Agent modules
│   ├── discovery_agent.py           # Finds businesses (Google + ScrapingBee)
│   ├── copywriter_pro.py            # Generates French cold emails
│   ├── outreach_manager.py          # Main orchestrator agent
│   ├── sender_agent.py              # Sends emails via Gmail
│   ├── has_website.py               # Website verification (standalone)
│   └── email_owner_Finder.py        # Contact finder (standalone)
│
├── data/
│   └── prospects.json               # Saved prospects (auto-generated)
│
├── .env                             # API keys & credentials (DO NOT COMMIT)
├── .gitignore                       # Excludes .env and __pycache__
├── requirements.txt                 # Python dependencies
└── README.md                        # This file

```

---

## 🤖 Agent Architecture

### 1. **Discovery Agent**
- **Input:** City + Business category (e.g., "dentist")
- **Process:**
  - Search Google Places API
  - Get place details
  - Check if business has website (Python filters + AI verification)
  - Scrape web for contact information
  - Extract emails using regex + AI validation
- **Output:** `prospects.json` with name, email, owner, phone, city

### 2. **Copywriter Agent**
- **Input:** Business name, type, city, rating, reviews
- **Process:**
  - Generate formal French cold email
  - Mention Baddy Reda (UM6P student)
  - Explain why they need a website
  - Suggest ROI & credibility benefits
  - Include clear CTA
- **Output:** HTML-formatted email body

### 3. **Outreach Manager**
- **Input:** Prospect JSON
- **Process:**
  - Calls Copywriter Agent (as tool)
  - Validates response format
  - Hands off to Sender Agent (with context)
- **Output:** Confirmed email send

### 4. **Sender Agent**
- **Input:** Business name, email, email body, owner name
- **Process:**
  - Format as professional HTML
  - Add signature (Baddy Reda + contact info)
  - Suggest WhatsApp/phone CTA
  - Call `send_email()` function (Gmail SMTP)
- **Output:** Email sent ✅

---

## 💡 Usage Examples

### Basic Run (Full Pipeline)

```bash
python main.py
```

Runs discovery → saves prospects → sends outreach emails

### Run Only Discovery

```bash
python My_agents/discovery_agent.py
```

Just finds prospects, saves to `data/prospects.json`, exits

### Modify Search Parameters

Edit `discovery_agent.py`:

```python
CITIES = [
    {"name": "Rabat", "lat": 34.0209, "lng": -6.8416},
    {"name": "Marrakesh", "lat": 31.6295, "lng": -8.0088},  # Add more cities
]

QUERIES = [
    "dentist", 
    "cabinet dentaire", 
    "gym", 
    "restaurant",  # Add business types
]
```

### Test Email Sending

Create `test_email.py`:

```python
from My_agents.sender_agent import send_email

result = send_email(
    subject="Test Email",
    html_body="<h1>Hello!</h1><p>This is a test.</p>",
    to_email="your-email@gmail.com"
)

print(result)
```

---

## 🛠️ Troubleshooting

### Common Issues

**❌ "RuntimeError: GROQ_API_KEY is not set"**
```bash
# Solution:
# 1. Check .env file exists in project root
# 2. Verify format: GROQ_API_KEY=your_key_here
# 3. Restart terminal/IDE
# 4. Check for typos in key
```

**❌ Agents SDK import error**
```bash
pip install agents-ai --upgrade
# If still fails, try:
pip install -r requirements.txt --force-reinstall
```

**❌ "ModuleNotFoundError: No module named 'agents'"**
```bash
# Activate venv first:
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Then reinstall:
pip install -r requirements.txt
```

**❌ Google Places API returns 403 error**
```
Solution:
1. Enable Places API in Google Cloud Console
2. Set up billing (required for API to work)
3. Wait 5 minutes after enabling
4. Verify API key is correct
```

**❌ Email not sending**
```
Check:
1. GMAIL_APP_PASSWORD is 16 characters
2. 2FA is enabled on Gmail account
3. Email address is correct in .env
4. Less secure apps are allowed (shouldn't be needed with app password)
5. Network connection works
```

**❌ Prospects not being saved**
```
Solutions:
1. Ensure data/ directory exists
2. Check write permissions: chmod 755 data/
3. Verify prospects.json is valid JSON (check for syntax errors)
4. Delete prospects.json and re-run discovery
```

---

## 📄 License

MIT License - Feel free to use, modify, and distribute this project.

---

## 📞 Support & Contact

**Creator:** Baddy Reda  
**Status:** UM6P Student | AI & Agents Enthusiast  

---

**Last Updated:** January 11, 2026  
**Version:** 1.0.0  
**Status:** Production Ready ✅
