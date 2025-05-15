# Working with Artifacts, FunctionTool, and ToolContext in ADK

This guide explains how to build tools for agents using the Google Agent Development Kit (ADK), focusing on:
- Creating tools with `FunctionTool`
- Saving and loading artifacts (binary data, e.g., PDFs)
- Using `ToolContext` for artifact management
- Async mechanics and best practices

## 1. What is a FunctionTool?
A `FunctionTool` is a wrapper that allows you to expose a Python function as a callable tool for an agent. The function can perform any logic, including interacting with files, APIs, or the ADK artifact system.

**Example:**
```python
from google.adk.tools import FunctionTool
from google.genai.types import Part

async def markdown_to_pdf(tool_context, markdown_text: str, filename: str = "generated_report.pdf") -> dict:
    # ... implementation ...

markdown_to_pdf_tool = FunctionTool(
    func=markdown_to_pdf,
    name="markdown_to_pdf",
    description="Convert markdown text to a PDF and save as an artifact."
)
```

## 2. ToolContext: The Bridge to Artifacts
`ToolContext` is passed as the first argument to every tool function. It provides methods to interact with the agent's runtime, including saving and loading artifacts.

### Key Methods:
- `await tool_context.save_artifact(filename, part)` — Save a binary/text artifact
- `await tool_context.load_artifact(filename)` — Load a previously saved artifact
- `tool_context.list_artifacts()` — List available artifact filenames

**Artifacts** are versioned, named binary blobs (e.g., PDFs, images) that can be shared between tools and agent runs.

## 3. Saving an Artifact (PDF Example)
To save a PDF as an artifact:
1. Generate the PDF as bytes
2. Wrap it in a `Part` using `Part.from_bytes(data=..., mime_type=...)`
3. Save it with `await tool_context.save_artifact(...)`

**Example:**
```python
from google.genai.types import Part
from fpdf import FPDF

async def markdown_to_pdf(tool_context, markdown_text: str, filename: str = "generated_report.pdf") -> dict:
    # Convert markdown to plain text (MVP)
    plain_text = markdown_text.replace("#", "").replace("*", "").replace("`", "")
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in plain_text.split("\n"):
        pdf.cell(0, 10, txt=line, ln=1)
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_part = Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")
    artifact_name = f"user:{filename}"
    await tool_context.save_artifact(artifact_name, pdf_part)
    return {"status": "success", "artifact_name": artifact_name}
```

**Note:**
- Use the `user:` prefix for artifact names to make them accessible across sessions and tool calls.
- Always `await` the save/load methods (they are async coroutines).

## 4. Loading an Artifact
To retrieve a previously saved artifact:
```python
async def publish_pdf(tool_context, pdf_artifact_name: str, filename: str = "published_report.pdf") -> dict:
    pdf_part = await tool_context.load_artifact(pdf_artifact_name)
    if not pdf_part or not hasattr(pdf_part, 'inline_data') or not pdf_part.inline_data.data:
        return {"status": "error", "message": f"Artifact '{pdf_artifact_name}' not found or invalid."}
    # Use pdf_part.inline_data.data (bytes) as needed
```

## 5. Registering Tools with an Agent
Add your tools to the agent's `tools` list:
```python
from content_publisher.tools import markdown_to_pdf, publish_pdf
from google.adk.agents import LlmAgent

content_publisher_agent = LlmAgent(
    name="content_publisher",
    model=MODEL,
    description=description,
    instruction=ROOT_AGENT_PROMPT,
    tools=[markdown_to_pdf, publish_pdf]
)
```

## 6. Async/Await: Why and How
- ADK's artifact methods are async. Always use `async def` and `await`.
- If you forget to await, you will get warnings and your code will not work as expected.

## 7. Namespacing and Best Practices
- Use `user:` prefix for artifact names to persist across tool calls and sessions.
- Use clear, descriptive filenames (e.g., `user:report_2024.pdf`).
- Always check for errors when loading artifacts.

## 8. Example Workflow
1. User asks agent to convert markdown to PDF.
2. Agent calls `markdown_to_pdf`, which saves the PDF as an artifact (`user:generated_report.pdf`).
3. Agent calls `publish_pdf`, which loads the artifact and saves it as a file on disk.

## 9. Debugging Tips
- Use `tool_context.list_artifacts()` to see what artifacts are available.
- Ensure you use the exact artifact name (including `user:` if used) when loading.
- If you see coroutine warnings, make sure your tool functions are async and you use `await`.

---

For more, see the [official ADK artifact documentation](https://google.github.io/adk-docs/artifacts/). 