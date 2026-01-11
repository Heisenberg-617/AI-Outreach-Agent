# main.py
import asyncio

# MUST be first import that touches anything related to Agents, 
# so the Groq client is available before any Agent is instantiated
import model

# 2. Register it as the SDK's DEFAULT client (critical!)
from agents import set_default_openai_client
set_default_openai_client(model.groq_client)

from agents import RunConfig, Runner
from My_agents.outreach_manager import outreach_manager
from My_agents.discovery_agent_test import run_discovery # Change to My_agents.discovery_agent for production
from My_agents.outreach_manager import OutreachContext

from pathlib import Path
import json

# Load environment variables
from dotenv import load_dotenv
load_dotenv(override=True)

# in main.py, right after imports
import model

DATA_PATH = Path("data/prospects_test.json") # Change to data/real_prospects_test.json for production

if __name__ == "__main__":
    print("\n=== Running Discovery Agent ===\n")
    run_discovery()

    # Load prospects
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        prospects = json.load(f)

    print("\nLoaded prospects:")
    for p in prospects:
        print(f"{p['business_name']} | {p['email']} | {p.get('city', 'unknown')}")

    print("\n=== Starting Outreach ===\n")

    async def main():
        for prospect in prospects:
            print(f"\nProcessing prospect: {prospect['business_name']}")
            # Run the Outreach Manager
            result = await Runner.run(outreach_manager, json.dumps(prospect), run_config=RunConfig(tracing_disabled=True), context=OutreachContext())
            # Print the final output if any
            print("✅ Outreach result:", result.final_output)


    asyncio.run(main())

    print("\n=== Outreach Complete ===")