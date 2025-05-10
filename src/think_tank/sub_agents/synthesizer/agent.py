
from google.adk.agents import LlmAgent
from think_tank.sub_agents.synthesizer.prompt import PROMPT
from dotenv import load_dotenv
import os
load_dotenv()
MODEL = os.getenv("VERTEX_AI_MODEL")
DESCRIPTION = """
Aggregation agent that consolidates specialist outputs, resolves conflicts, and crafts a concise yet engaging action plan.
"""
synthesizer_agent = LlmAgent(
    name="synthesizer",
    model=MODEL,
    description=DESCRIPTION,
    instruction=PROMPT
) 