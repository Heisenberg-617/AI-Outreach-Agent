from dataclasses import dataclass
import model
from model import groq_models
from agents import Agent, RunContextWrapper, handoff
from pydantic import BaseModel
from typing import Dict, Any, Optional
from My_agents.copywriter_pro import pro_tool
from My_agents.sender_agent import sender_agent

copywriting_tools = [pro_tool]

instructions = """
You will:
1. Receive a business prospect
2. Use the tool copywriter_pro to generate a professional cold email in French
You MUST call copywriter_pro EXACTLY like:
    copywriter_pro(input="Business_name, type, city, rating, reviews")
    Do not add extra fields to the tool call.
3. Hand it off with EXACT schema: business_name, email, city, body, owner_name. No extra reasoning.
"""

@dataclass
class OutreachContext:
    handoff_data: Optional[HandoffData] = None
    
class HandoffData(BaseModel):
    business_name: str
    email: str
    city: str
    body: str
    owner_name: Optional[str] = None  # Optional fields OK

async def on_handoff_to_sender(ctx: RunContextWrapper[OutreachContext], data: HandoffData):
    """Store data for sender_agent."""
    ctx.context.handoff_data = data  # <- Store in custom context
    print(f"✅ Handoff stored: {data.business_name}")


outreach_manager = Agent(
    name="Outreach Manager",
    instructions=instructions,
    model = groq_models,
    tools=copywriting_tools,
    handoffs=[handoff(
            sender_agent,
            tool_name_override="handoff_to_sender",
            tool_description_override=(
                "Call when you have selected the final email. "
                "Pass prospect details and email body."
            ),
            input_type=HandoffData,
            on_handoff=on_handoff_to_sender
        )]
    )
