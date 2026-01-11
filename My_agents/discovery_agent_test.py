import json
import os
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(override=True)

DATA_PATH = Path("data/prospects.json")


def run_discovery():
    """
    Mock discovery agent.
    In real version, this would call Google Places API.
    For now, it saves high-quality Moroccan SME prospects locally.
    """

    prospects = [
        {
            "business_name": "Clinique Dentaire Al Wifaq",
            "city": "Casablanca",
            "category": "Dentist",
            "rating": 4.5,
            "reviews": 183,
            "email": os.getenv("GMAIL_USER"),
            "owner_name": "Dr. El Amrani",
            "has_website": False
        },
        {
            "business_name": "Atlas Fitness",
            "city": "Rabat",
            "category": "Gym",
            "rating": 4.2,
            "reviews": 146,
            "email": os.getenv("GMAIL_USER"),
            "owner_name": None,
            "has_website": False
        }
    ]


    DATA_PATH.parent.mkdir(exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(prospects, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(prospects)} prospects to {DATA_PATH}")

run_discovery()