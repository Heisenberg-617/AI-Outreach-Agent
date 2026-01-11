import model
from model import groq_models
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, function_tool
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings import MODEL_NAME_SENDER
from model import groq_client

@function_tool
def send_email(subject: str, html_body: str, to_email: str):
    """
    Sends an HTML email using Gmail SMTP.

    Inputs:
    - subject: Email subject
    - html_body: HTML formatted email body
    - to_email: Recipient email address
    """

    from_email = os.getenv("GMAIL_USER")
    gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")

    if not from_email or not gmail_app_password:
        return {
            "status": "failure",
            "message": "Missing GMAIL_USER or GMAIL_APP_PASSWORD in environment variables"
        }

    try:
        # Create MIME message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email

        # Attach HTML body
        msg.attach(MIMEText(html_body, "html"))

        # Send via Gmail SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(from_email, gmail_app_password)
            server.send_message(msg)

        return {"status": "success"}

    except Exception as e:
        return {"status": "failure", "message": str(e)}


# -------------------------------
# Sender Agent (handoff target)
# -------------------------------
instructions = """
You are an Email Sender Agent.
INPUT: business_name, email, city, body, owner_name. 
TASKS:
1. Objet: Short French title high open rate (growth/opportunity hint)
2. Greeting: "Bonjour {owner_name}," or if the owner is not specified use "Bonjour {business_name} équipe," or other neutral greeting. 
3. HTML: Bold key points, clean layout. No email body changes!! You format it, no tool calling here.
4. ALWAYS USE THIS  EXACT Signature:
---
Baddy Reda
Étudiant UM6P | IA & agents enthousiaste
reda.baddy@emines.um6p.ma
0770244313 WhatsApp
---
5. send_email(subject, html_body, email)
Format only. No email body changes.
"""
groq_models = OpenAIChatCompletionsModel(model = MODEL_NAME_SENDER, openai_client=groq_client)
    
sender_agent = Agent(
    name="Sender Agent",
    instructions=instructions,
    tools=[send_email],
    model=groq_models,
    handoff_description="Receives the finalized email and prospect info to send the email."
)