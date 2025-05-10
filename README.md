# Think Tank

A multi-agent system for multi-perspective problem solving using Google ADK and Vertex AI.

## Features
- Modular root agent (`think_tank`) orchestrates sub-agents
- Sub-agents for McKinsey consultant and Organizational Psychologist perspectives
- Easily extensible for more expert agents
- Uses Google ADK for agent orchestration and Vertex AI for LLMs

## Project Structure
```
src/
  think_tank/
    agent.py
    prompt.py
    __main__.py
    sub_agents/
      mckinsey/
        agent.py
        prompt.py
        __init__.py
      org_psychologist/
        agent.py
        prompt.py
        __init__.py
    __init__.py
    sub_agents/__init__.py
.env
pyproject.toml
README.md
```

## Setup
1. Install [uv](https://github.com/astral-sh/uv):
   ```bash
   pip install uv
   ```
2. Sync dependencies:
   ```bash
   uv sync
   ```
3. Set up your `.env` file with Google Cloud and Vertex AI credentials.

## Usage
Run the root agent:
```bash
python -m think_tank
```

## References
- [Google ADK Documentation](https://google.github.io/adk-docs)
- [Vertex AI Python SDK](https://cloud.google.com/python/docs/reference/aiplatform/latest)

## License
Apache 2.0 