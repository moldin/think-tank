import io
import os
from fpdf import FPDF
from google.genai.types import Part
import markdown2
from weasyprint import HTML, CSS
#from weasyprint.fonts import FontConfiguration # Optional: for advanced font control if ever needed


ARTIFACTS_DIR = os.getenv("ARTIFACTS_DIR")


REPORT_STYLES = """
    @page {
        size: A4;
        margin: 20mm 18mm 25mm 18mm; /* Top, Right, Bottom, Left */

        @bottom-left {
            content: "Company Confidential"; /* Or your preferred footer text */
            font-family: 'Helvetica Neue', Arial, sans-serif;
            font-size: 8pt;
            color: #777777;
        }

        @bottom-right {
            content: "Page " counter(page) " of " counter(pages);
            font-family: 'Helvetica Neue', Arial, sans-serif;
            font-size: 8pt;
            color: #777777;
        }
    }

    body {
        font-family: 'Helvetica Neue', Arial, sans-serif; /* Common, clean sans-serif */
        font-size: 10.5pt;
        line-height: 1.55;
        color: #222222; /* Darker gray for better contrast */
        text-rendering: optimizeLegibility;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Helvetica Neue', Arial, sans-serif;
        color: #1A3A6D; /* A deeper, more muted blue */
        margin-top: 2em;
        margin-bottom: 0.8em;
        line-height: 1.25;
        page-break-after: avoid;
        font-weight: 300; /* Lighter font weight for modern feel */
    }

    h1 {
        font-size: 22pt;
        font-weight: 500; /* Medium weight for main title */
        color: #102A52;
        border-bottom: 1.5pt solid #1A3A6D;
        padding-bottom: 0.4em;
        margin-top: 0;
        letter-spacing: -0.5px;
    }

    h2 {
        font-size: 17pt;
        font-weight: 400; /* Normal/Regular weight */
        border-bottom: 0.75pt solid #AEC8E5; /* Lighter blue underline */
        padding-bottom: 0.3em;
        margin-top: 2.2em;
    }

    h3 {
        font-size: 13pt;
        font-weight: 500; /* Medium weight */
        color: #2D5A8D;
        margin-top: 1.8em;
        margin-bottom: 0.6em;
    }

    h4 {
        font-size: 11pt;
        font-weight: 500; /* Medium weight */
        color: #333333;
        font-style: italic;
        margin-top: 1.5em;
    }
    
    h5 {
        font-size: 10.5pt;
        font-weight: bold;
        color: #444444;
        margin-top: 1.5em;
    }

    h6 {
        font-size: 10pt;
        font-weight: bold;
        color: #555555;
        font-style: italic;
        margin-top: 1.5em;
    }

    p {
        margin-bottom: 1em;
        text-align: left; /* Left align is often cleaner */
        hyphens: auto;
    }

    a {
        color: #0056b3;
        text-decoration: none;
    }
    a:hover { text-decoration: underline; }

    ul, ol {
        margin-bottom: 1em;
        padding-left: 1.5em;
    }
    ul { list-style-type: disc; }
    ul ul { list-style-type: circle; }
    ol { list-style-type: decimal; }
    li {
        margin-bottom: 0.5em;
        padding-left: 0.3em; /* Space between bullet/number and text */
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 1.2em;
        margin-bottom: 1.8em;
        font-size: 9.5pt;
        page-break-inside: avoid;
        border-top: 1.5pt solid #4A6C8E;
        border-bottom: 1pt solid #4A6C8E;
    }

    th, td {
        border-bottom: 0.5pt solid #DDE5ED; /* Light horizontal lines only */
        padding: 10px 8px;
        text-align: left;
        vertical-align: top;
    }

    th {
        background-color: #F0F4F8;
        font-weight: 500; /* Medium weight */
        color: #1A3A6D;
        border-bottom-width: 1pt; /* Thicker line below header */
    }

    blockquote {
        margin: 1.5em 0em 1.5em 1em;
        padding: 0.8em 1.2em;
        border-left: 3px solid #AEC8E5;
        background-color: #F8FAFC;
        color: #4A5568;
        font-style: italic;
    }

    pre {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 3px;
        padding: 1em;
        overflow-x: auto;
        font-size: 9pt;
        line-height: 1.45;
        page-break-inside: avoid;
        white-space: pre-wrap;
        word-wrap: break-word;
    }

    code { /* Inline code */
        font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
        background-color: #EFF2F5;
        padding: 0.2em 0.4em;
        border-radius: 3px;
        font-size: 0.88em;
        color: #BF0711;
    }
    pre code { /* Reset for code inside pre */
        background-color: transparent;
        padding: 0;
        border-radius: 0;
        font-size: inherit;
        color: inherit;
    }

    hr {
        border: 0;
        border-top: 0.75pt solid #cccccc;
        margin: 2.5em auto;
        width: 75%;
    }

    /* Class for a potential title page if you generate one separately */
    .title-page {
        text-align: center;
        page-break-after: always;
    }
    .title-page h1 {
        font-size: 28pt; /* Adjusted for the new heading style */
        font-weight: 500;
        margin-top: 2.5in; /* Push title down */
        border-bottom: none;
        color: #102A52;
    }
    .title-page p {
        font-size: 12pt; /* Adjusted */
        color: #4A5568;
        text-align: center;
        margin-top: 0.5em;
    }
    .title-page .author, .title-page .date {
        font-size: 11pt;
        color: #555555;
        margin-top: 1.5em;
    }
"""

async def markdown_to_pdf(tool_context, markdown_text: str, filename: str = "generated_report.pdf") -> dict:
    """
    Converts a markdown string to a professional-looking PDF using WeasyPrint,
    saves it as an artifact, and returns a JSON-compatible dictionary.
    It includes styles for headers, lists, tables, code blocks, etc.

    Args:
        tool_context: The ADK ToolContext for managing artifacts.
        markdown_text: The markdown text to convert.
        filename: The name for the PDF artifact (optional).

    Returns:
        A dictionary with status, message, and artifact name.
    """
    try:
        # --- 1. Define the CSS for a professional report look ---
        css_stylesheet = CSS(string=REPORT_STYLES)

        # --- 2. Convert Markdown to HTML ---
        html_body_content = markdown2.markdown(
            markdown_text,
            extras=[
                "tables",
                "fenced-code-blocks",
                "nofollow",
                "cuddled-lists",
                "strike",
                "task_list",
                "smarty-pants"
            ]
        )

        # --- 3. Construct the full HTML document ---
        # Corrected the comment to use proper HTML comment syntax # Also, it's generally better to place comments on their own line or after content
        # for clarity within the f-string, though not strictly necessary for HTML.
        title_text = filename.replace('.pdf', '')
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{title_text}</title> </head>
        <body>
            {html_body_content}
        </body>
        </html>
        """

        # --- 4. Generate PDF using WeasyPrint ---
        
        html_doc = HTML(string=full_html)
        pdf_bytes = html_doc.write_pdf(stylesheets=[css_stylesheet])

        # --- 5. Create and save artifact ---
        pdf_part = Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")
        artifact_name = f"user:{filename}"
        await tool_context.save_artifact(artifact_name, pdf_part)

        return {
            "status": "success",
            "message": f"Professional PDF artifact '{artifact_name}' created and saved.",
            "artifact_name": artifact_name
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to convert markdown to PDF: {str(e)}",
            "artifact_name": None
        }

async def markdown_to_pdf_old(tool_context, markdown_text: str, filename: str = "generated_report.pdf") -> dict:
    """
    Converts a markdown string to a PDF, saves it as an artifact, and returns a JSON-compatible dictionary.
    MVP: No advanced markdown rendering, just basic text output.
    Args:
        tool_context: The ADK ToolContext for managing artifacts.
        markdown_text: The markdown text to convert.
        filename: The name for the PDF artifact (optional).
    Returns:
        A dictionary with status, message, and artifact name.
    """
    try:
        # Basic markdown to plain text (MVP: ignore formatting)
        plain_text = markdown_text.replace("#", "").replace("*", "").replace("`", "")

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for line in plain_text.split("\n"):
            pdf.cell(0, 10, txt=line, ln=1)
        
        # Get PDF as bytes
        pdf_bytes = pdf.output(dest='S').encode('latin1')

        # Create artifact part
        pdf_part = Part.from_bytes(data=pdf_bytes, mime_type="application/pdf")

        # Save artifact using ToolContext
        artifact_name = f"user:{filename}"
        await tool_context.save_artifact(artifact_name, pdf_part)

        return {
            "status": "success",
            "message": f"PDF artifact '{artifact_name}' created and saved.",
            "artifact_name": artifact_name
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to convert markdown to PDF: {str(e)}",
            "artifact_name": None
        }

async def publish_pdf(tool_context, pdf_artifact_name: str, filename: str = "published_report.pdf") -> dict:
    """
    Saves a PDF artifact as a local file in the artifacts directory.
    Args:
        tool_context: The ADK ToolContext for accessing artifacts.
        pdf_artifact_name: The name of the PDF artifact to retrieve.
        filename: The name to use for the saved PDF file (optional).
    Returns:
        A dictionary with status, message, and file path.
    """
    try:
        # Ensure the output directory exists
        output_dir = ARTIFACTS_DIR
        os.makedirs(output_dir, exist_ok=True)

        # Retrieve the PDF artifact
        pdf_part = await tool_context.load_artifact(pdf_artifact_name)
        if not pdf_part or not hasattr(pdf_part, 'inline_data') or not pdf_part.inline_data.data:
            return {
                "status": "error",
                "message": f"Artifact '{pdf_artifact_name}' not found or invalid.",
                "file_path": None
            }

        # Extract PDF bytes
        pdf_bytes = pdf_part.inline_data.data

        # Write the PDF to a local file
        output_path = os.path.join(output_dir, filename)
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

        return {
            "status": "success",
            "message": f"PDF saved locally as {output_path}",
            "file_path": output_path
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to publish PDF: {str(e)}",
            "file_path": None
        }