
from google.adk.agents import LlmAgent, ParallelAgent
from think_tank.sub_agents.think_tank.prompt import MCKINSEY_PROMPT, ORG_PSYCHOLOGIST_PROMPT, CHANGE_MANAGEMENT_PROMPT
from think_tank.sub_agents.think_tank.prompt import AIML_LEAD_PROMPT, AI_ETHICS_PROMPT, SCENARIO_PLANNER_PROMPT
from think_tank.sub_agents.think_tank.prompt import DEBONO_HATS_PROMPT, DEVILS_ADVOCATE_PROMPT, UX_DESIGN_THINKER_PROMPT
from dotenv import load_dotenv
import os
load_dotenv()
MODEL = os.getenv("VERTEX_AI_MODEL")

MCKINSEY_DESCRIPTION = """
Strategy consultant applying MECE, issue‑tree thinking, 
and 7‑S analysis to frame the problem, size opportunities, and surface no‑regret moves.
"""
mckinsey_agent = LlmAgent(
    name="mckinsey",
    model=MODEL,
    description=MCKINSEY_DESCRIPTION,
    instruction=MCKINSEY_PROMPT,
    output_key="mckinsey_output"
) 

ORG_PSYCHOLOGIST_DESCRIPTION = """
Expert in human behaviour and change management, revealing cultural blockers, motivation levers, and intervention roadmaps.
"""
org_psychologist_agent = LlmAgent(
    name="org_psychologist",
    model=MODEL,
    description=ORG_PSYCHOLOGIST_DESCRIPTION,
    instruction=ORG_PSYCHOLOGIST_PROMPT,
    output_key="org_psychologist_output"
) 
CM_DESCRIPTION = """
Guides organisations through adoption by crafting a compelling change narrative, activating champions and sequencing interventions for maximum uptake.
"""
change_management_agent = LlmAgent(
    name="change_management",
    model=MODEL,
    description=CM_DESCRIPTION,
    instruction=CHANGE_MANAGEMENT_PROMPT,
    output_key="change_management_output"
)

AIML_LEAD_DESCRIPTION = """
Technical lead who defines data strategy, model approach, and MLOps path to production while safeguarding performance, cost, and responsibility.
"""
aiml_lead_agent = LlmAgent(
    name="aiml_lead",
    model=MODEL,
    description=AIML_LEAD_DESCRIPTION,
    instruction=AIML_LEAD_PROMPT,
    output_key="aiml_lead_output"
)

AI_ETHICS_DESCRIPTION = """
Evaluates ethical tensions and societal impact, ensuring alignment with legal frameworks and human values.
"""
ai_ethics_agent = LlmAgent(
    name="ai_ethics",
    model=MODEL,
    description=AI_ETHICS_DESCRIPTION,
    instruction=AI_ETHICS_PROMPT,
    output_key="ai_ethics_output"
)

UX_DESIGN_THINKER_DESCRIPTION = """
Uncovers user needs and pain points, turning insights into prototype hypotheses and test plans.
"""
ux_design_thinker_agent = LlmAgent(
    name="ux_design_thinker",
    model=MODEL,
    description=UX_DESIGN_THINKER_DESCRIPTION,
    instruction=UX_DESIGN_THINKER_PROMPT,
    output_key="ux_design_thinker_output"
)

SCENARIO_PLANNER_DESCRIPTION = """
CExplores plausible futures, stress‑testing strategies against external drivers across 5‑ and 10‑year horizons.
"""
scenario_planner_agent = LlmAgent(
    name="scenario_planner",
    model=MODEL,
    description=SCENARIO_PLANNER_DESCRIPTION,
    instruction=SCENARIO_PLANNER_PROMPT,
    output_key="scenario_planner_output"
)

DEBONO_HATS_DESCRIPTION = """
Applies the Six Thinking Hats methodology to generate balanced viewpoints and organise group thinking.
"""
debono_hats_agent = LlmAgent(
    name="debono_hats",
    model=MODEL,
    description=DEBONO_HATS_DESCRIPTION,
    instruction=DEBONO_HATS_PROMPT,
    output_key="debono_hats_output"
)

DEVILS_ADVOCATE_DESCRIPTION = """
Stress‑tests proposals by inverting assumptions, spotlighting failure modes, and articulating the strongest counterarguments.
"""
devils_advocate_agent = LlmAgent(
    name="devils_advocate",
    model=MODEL,
    description=DEVILS_ADVOCATE_DESCRIPTION,
    instruction=DEVILS_ADVOCATE_PROMPT,
    output_key="devils_advocate_output"
)

think_tank_agent = ParallelAgent(
    name="think_tank",
    description="Think Tank agent runs multiple paralell analysis to provide a comprehensive multi-perspective analysis.",
    sub_agents=[
        mckinsey_agent,
        org_psychologist_agent,
        change_management_agent,
        #aiml_lead_agent,
        #ai_ethics_agent,
        #ux_design_thinker_agent,
        scenario_planner_agent,
        debono_hats_agent,
        devils_advocate_agent
    ]
) 