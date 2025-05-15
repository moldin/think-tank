import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from content_publisher.tools import markdown_to_pdf, publish_pdf

# Load environment variables
load_dotenv()

# Get the model from environment variables
MODEL = os.getenv("VERTEX_AI_MODEL")

# Agent description
description = """
Central control agent that analyzes the user problem, selects the most appropriate workflow, 
manages specialist personas, enforces global constraints, and returns a reader-friendly executive plan.
"""

# Root agent prompt
ROOT_AGENT_PROMPT = """
You are a content publishing agent. Your task is to take markdown input from the user, convert it to a PDF artifact using the markdown_to_pdf tool, and save the PDF as a local file using the publish_pdf tool. The markdown_to_pdf tool takes markdown text and an optional filename, returning a dictionary with the artifact name. The publish_pdf tool takes the artifact name and an optional filename, returning a dictionary with the saved file path. Return a clear summary of the actions taken and the location of the saved file.
"""

# Create the content publisher agent
content_publisher_agent = LlmAgent(
    name="content_publisher",
    model=MODEL,
    description=description,
    instruction=ROOT_AGENT_PROMPT,
    tools=[markdown_to_pdf, publish_pdf]
)

# Root agent
root_agent = content_publisher_agent