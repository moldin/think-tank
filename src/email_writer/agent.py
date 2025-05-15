import os
from google.adk.agents import LlmAgent


from pydantic import BaseModel, Field

from dotenv import load_dotenv
load_dotenv()

MODEL = os.getenv("VERTEX_AI_MODEL")

class EmailContent(BaseModel):
    date: str = Field(description="The date of the email")
    from_address: str = Field(description="The sender of the email")
    to_address: str = Field(description="The recipient of the email")
    subject: str = Field(description="The subject of the email")
    body: str = Field(description="The body of the email. Should well-formatted with proper paragraphs and spacing.")
    

email_writer_agent = LlmAgent(
    name="email_writer",
    model=MODEL,
    description="GEnerates emails with structured subject, body and other fields",
    instruction="""
    Understand the user's request and generate an email with the following fields:
    - Date {todays_date}
    - From address {user_email}
    - To address
    - Subject
    - Body
   

    IMPORTANT: Youre response MUST be valid JSON matching this schema:
    {
        "date": "Date of the email here",
        "from_address": "Sender of the email here",
        "to_address": "Recipient of the email here"
        "subject": "Subject line here",
        "body": "Email body here",
        
    }

    DO NOT include any other text than the JSON response, no explanations, no other text, only the JSON response.
    """,
    output_schema=EmailContent,
    output_key="email"
) 

root_agent = email_writer_agent
