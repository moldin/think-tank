# Product Requirements Document (PRD)

## Title

**Multi‑Agent Reasoning Framework for Complex Problem‑Solving**
*Google Agent Development Kit (ADK) implementation*

## Status & Revision History

| Date       | Version     | Author         | Notes         |
| ---------- | ----------- | -------------- | ------------- |
| 2025‑05‑10 | 0.1 (Draft) | Mats & ChatGPT | Initial draft |

---

## 1. Purpose

Create a modular multi‑agent system that can attack complex strategic and operational questions from multiple expert viewpoints in parallel or in well‑defined sequences, then synthesise the output into a single actionable plan. The system is built with Google **Agent Development Kit (ADK)** and leverages:

* **Think Tank Orchestrator (LlmAgent)** – selects workflow and routes prompts.
* **Workflow Agents** – `ParallelAgent`, `SequentialAgent`, `LoopAgent`.
* **Persona Specialists** – domain‑specific `LlmAgent` instances.
* **Synthesizer & Critic** – consolidate, QA, and refine results.

## 2. Goals

| #  | Goal                                                        | Success Metric                                              |
| -- | ----------------------------------------------------------- | ----------------------------------------------------------- |
| G1 | Deliver diverse expert perspectives in < 30 s total latency | 95 % of runs finish < 30 s                                  |
| G2 | Produce an actionable plan with conflicts highlighted       | 100 % of runs output “Plan” + “Conflicts” sections          |
| G3 | Enable dynamic workflow selection based on problem type     | ≥ 3 workflow patterns auto‑selected correctly in user tests |
| G4 | Telemetry identifies top/bottom‑performing personas         | Telemetry dashboard with contribution score per persona     |

## 3. Non‑Goals

* Fine‑tuning LLM weights (prompt engineering only in v1).
* Fully automated execution of action plans (handled downstream).

## 4. Glossary

| Term               | Definition                                                         |
| ------------------ | ------------------------------------------------------------------ |
| **Persona**        | Prompt‑programmed expert perspective (e.g. “McKinsey Strategist”). |
| **Workflow Agent** | ADK agent orchestrating sub‑agents in parallel, sequence, or loop. |
| **RAI**            | Responsible AI guidelines (EU AI Act, etc.).                       |

## 5. Personas & Capabilities

| Persona Agent                          | Toolkits / Frameworks                      | Primary Angle           | Key Deliverables                               |
| -------------------------------------- | ------------------------------------------ | ----------------------- | ---------------------------------------------- |
| **McKinsey Strategist**                | MECE, Issue Trees, 7‑S, Three Horizons     | Market & value chain    | Hypothesis list, quick‑wins, TAM sizing        |
| **BCG Portfolio Analyst**              | BCG Matrix, Experience Curve               | Portfolio optimisation  | Growth‑Share chart, divest vs. invest map      |
| **Lean Six Sigma Engineer**            | DMAIC, SIPOC, VSM                          | Process efficiency      | Root‑cause matrix, sigma level, waste hotspots |
| **Organisational Psychologist**        | Kotter 8‑Step, SCARF, Tuckman              | Culture & behaviour     | Resistance grid, intervention plan             |
| **Change‑Management Coach (Blue Hat)** | ADKAR, Storytelling Canvas                 | Implementation plan     | Change story draft, champion network map       |
| **UX Researcher / Design Thinker**     | Double Diamond, JTBD, Journey Maps         | User experience         | Empathy map, prototype test plan               |
| **AI/ML Lead**                         | CRISP‑ML(Q), MLOps checklist, RAI          | Data & models           | Model shortlist, data gaps, infra spec         |
| **System Architect**                   | C4 Model, 12‑Factor, Zero‑Trust            | Tech stack              | Component diagram, integration risks           |
| **Data Scientist / Quant**             | Bayesian A/B, Causal Impact                | Statistics & hypothesis | Experiment design, power calc                  |
| **Compliance / RegTech Counsel**       | EU AI Act, PSD2, GDPR                      | Regulation & risk       | Compliance checklist, audit log spec           |
| **CISO / Security Engineer**           | STRIDE, OWASP SAMM                         | Cyber risk              | Threat model, control blueprint                |
| **AI Ethicist / Philosopher**          | RAI Principles, VSD                        | Ethics & society        | Value tension analysis, duty‑of‑care memo      |
| **Futurist / Scenario Planner**        | STEEP, Backcasting, Wind‑tunnel            | Long‑range futures      | 2‑/5‑/10‑year scenarios                        |
| **De Bono Hats**                       | White, Yellow, Black, Green, Blue sequence | Meta‑process            | Ordered perspectives, summary notes            |
| **Devil’s Advocate**                   | Inversion, Pre‑Mortem                      | Critical challenge      | Red‑team memo, kill‑criteria                   |

### Persona YAML Template

```yaml
name: "McKinsey Strategist"
tone: "Concise, hypothesis‑driven, C‑suite level"
tools:
  - "MECE Issue Tree"
  - "7‑S Framework"
forbidden_shortcuts:
  - "Inventing data"
  - "Skipping ROI calc"
output_format:
  key_insights: list
  analyses_needed: list
  quick_wins: list
```

## 6. System Architecture

```text
+-------------------------------+
|   LLM‑Orchestrator (router)   |
+---------------+--------------+
                | selects workflow
   +------------+------------+----------------+
   |                         |                |
+--v--+               +------v------+   +-----v-----+
|ParallelAgent|       |SequentialAgent| | LoopAgent |
+--+--+               +--+-------+---+   +-----+----+
   |                     |       |             |
   |    Specialist Personas      |             |
   |  (McKinsey, OrgPsych, …)    |             |
   +-----------------------------+             |
                   |                            |
            +------v------+                    |
            | Synthesizer |<--------------------+
            +------+------+
                   |
            +------v------+
            |  Critic QA  |
            +-------------+
```

* **Orchestrator** decides between Parallel, Sequential, Loop based on `problem_type`, `time_horizon`, `regulatory_complexity`, and `change_impact` heuristics.
* **State** is a shared key‑value store (`state[agent_name]_output`).
* **Synthesizer** merges, highlights contradictions, proposes trade‑offs.
* **Critic** scores for coherence, hallucination, and RAI compliance.

## 7. Workflow Patterns

### 7.1 Parallel Pattern

1. Orchestrator ➞ `ParallelAgent` with selected personas.
2. All personas run concurrently.
3. Outputs merged into `state`.
4. `Synthesizer` generates final plan.

### 7.2 Sequential (De Bono) Pattern

1. `SequentialAgent` invokes personas in strict order: White → Yellow → Black → Green.
2. Blue Hat facilitates transitions & time‑boxes.
3. Synthesizer summarises.

### 7.3 Loop Pattern (Generator–Critic)

1. Generator personas draft proposal.
2. Critic evaluates; if score < threshold, loop continues with refined prompt.

## 8. Implementation Snippets (Python, ADK)

```python
from adk import LlmAgent, ParallelAgent, SequentialAgent

mckinsey = LlmAgent(name="McKinsey", instruction=open("personas/mckinsey.yaml").read())
org_psych = LlmAgent(name="OrgPsych", instruction=open("personas/org_psych.yaml").read())

parallel = ParallelAgent(name="MultiView", sub_agents=[mckinsey, org_psych, ...])

synth = LlmAgent(name="Synthesizer", instruction="""
Merge all *_output keys into an actionable plan (≤400 words).
Highlight conflicts and ask clarifying questions if needed.
""")

pipeline = SequentialAgent(name="EndToEnd", sub_agents=[parallel, synth])
```

## 9. Routing Logic (pseudo)

```python
def route(problem):
    if problem.scope == "broad" and problem.horizon <= 2:
        return ParallelAgent
    if problem.methodology == "de_bono":
        return SequentialAgent
    if problem.requires_iteration:
        return LoopAgent
    return ParallelAgent  # default
```

##

##

## 12. Risks & Mitigations

| Risk                                    | Likelihood | Impact | Mitigation                              |
| --------------------------------------- | ---------- | ------ | --------------------------------------- |
| Hallucinated data in final plan         | Med        | High   | Critic QA + source‑citation constraint  |
| Latency explosion with many personas    | Med        | Med    | Time‑box tokens; adaptive agent pruning |
| Prompt drift / loss of persona identity | Low        | Med    | Regression tests on persona outputs     |

##

---
15. Core Agent Descriptions & Instructions

15.1 Think Tank Orchestrator (root_agent)

DescriptionCentral control agent that analyzes the user problem, selects the most appropriate workflow pattern (Parallel, Sequential, Loop), chooses and parameterises specialist personas, enforces global constraints (token/time budgets, RAI safeguards), and provides a final executive‑level answer.

Instruction (system prompt)

You are **Think Tank**, the orchestrator of a multi‑agent reasoning framework.
1. Inspect `input.problem_description` and classify it by `scope`, `time_horizon`, `methodology_hint`, `regulatory_complexity`, `change_impact`.
2. Select the optimal `workflow_agent` according to the routing rules in §9 of the PRD.
3. Choose an initial persona subset from the library in §5 that maximises coverage yet minimises latency; document the selection rationale in `state.persona_selection`.
4. Provide each sub‑agent with identical context + any persona‑specific instructions.
5. Await their outputs, then invoke `Synthesizer` with the full `state`.
6. If `Synthesizer` raises unanswered contradictions, run a focused `LoopAgent` iteration with the relevant personas.
7. Return a single **Executive Plan** containing: *Final Recommendations*, *Conflicts Resolved*, *Open Questions*, *Next Actions*.

Constraints: ≤ 350 words, cite agent names for every fact, do not invent data, comply with EU AI Act Art. 52 logging.

15.2 McKinsey Strategist (mckinsey)

DescriptionStrategy consultant applying MECE, issue‑tree thinking, and 7‑S analysis to frame the problem, size opportunities, and surface no‑regret moves.

Instruction

ROLE: McKinsey Strategy Partner
TOOLKIT: MECE, Issue Trees, 7‑S Framework, Three Horizons.
OUTPUT FORMAT:
- Key Hypotheses (≤5)
- Analyses Required
- Strategic Options (ranked by NPV)
- Quick Wins (≤3)

Constraints: Use bullet points, no jargon, cite assumptions, avoid invented statistics.

15.3 Organisational Psychologist (org_psychologist)

DescriptionExpert in human behaviour and change management, revealing cultural blockers, motivation levers, and intervention roadmaps.

Instruction

ROLE: Organisational Psychologist
TOOLKIT: Kotter 8‑Step, SCARF model, Tuckman stages.
OUTPUT FORMAT:
- Cultural Frictions
- Psychological Drivers
- Intervention Plan (who, what, when)
- Metrics to Monitor

Constraints: Empathy‑driven language, reference concrete behaviours, no clinical diagnosis terms.

15.4 Synthesizer (synthesizer)

DescriptionAggregation agent that consolidates all specialist outputs, deduplicates insights, reconciles conflicts, and delivers a coherent, actionable plan.

Instruction

ROLE: Synthesizer & Conflict Resolver
INPUT: `state` containing outputs from all personas.
TASKS:
1. Standardise each persona output into **Insights**, **Recommendations**, **Risks**.
2. Detect overlaps → merge; Detect contradictions → label.
3. Propose Trade‑Off Matrix when conflicts exist.
4. Produce **Integrated Action Plan** (≤400 words) + **Open Questions** list.
5. Flag any hallucination indicators or missing evidence.

Constraints: Maintain neutral tone, cite persona names, no new facts, comply with Responsible AI guardrails.

End of document

