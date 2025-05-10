import os

from google.adk.agents import LlmAgent, SequentialAgent
from think_tank.sub_agents.think_tank.agent import think_tank_agent
from think_tank.sub_agents.synthesizer.agent import synthesizer_agent
from think_tank.prompt import ROOT_AGENT_PROMPT, CLARIFICATION_PROMPT
from dotenv import load_dotenv
load_dotenv()

MODEL = os.getenv("VERTEX_AI_MODEL")





facilitator_agent = SequentialAgent(
    name="facilitator",
    description="Facilitator agent that coordinates the parallel agents.",
    sub_agents=[
        think_tank_agent,
        synthesizer_agent
    ]
)

clarification_agent = LlmAgent(
    name="clarification",
    model=MODEL,
    description="Pre‑processing agent launched before giving the 'facilitator_agent' the user's prompt. It reviews the user’s initial prompt and the list of available personas to detect information gaps, then asks the user 4‑5 focused questions that will supply the data each persona needs to provide high‑quality answers.",
    instruction=CLARIFICATION_PROMPT,
    output_key="clarification_questions"
)

description = """
Central control agent that analyses the user problem, selects the most appropriate workflow, manages specialist personas, enforces global constraints, and returns a reader‑friendly executive plan.
"""
problem_solver_agent = LlmAgent(
    name="problem_solver",
    model=MODEL,
    description=description,
    instruction=ROOT_AGENT_PROMPT,
    sub_agents=[
        clarification_agent,
        facilitator_agent,
    ]
) 
root_agent = problem_solver_agent