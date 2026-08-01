#!/usr/bin/env python3
"""Render COMPARE_1STEP_2STEP.md to a styled PDF using Playwright."""

from pathlib import Path
import markdown

SCRIPT_DIR = Path(__file__).resolve().parent
MD_FILE    = SCRIPT_DIR / "COMPARE_1STEP_2STEP.md"
HTML_FILE  = SCRIPT_DIR / "COMPARE_1STEP_2STEP.html"
PDF_FILE   = SCRIPT_DIR / "COMPARE_1STEP_2STEP.pdf"

md_text = MD_FILE.read_text(encoding="utf-8")
body_html = markdown.markdown(md_text, extensions=["tables", "fenced_code"])

css = """
    @page { size: A4; margin: 2cm 2.2cm; }
    body {
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #1a1a1a;
        max-width: 100%;
    }
    h1 {
        font-size: 18pt;
        color: #1F4E79;
        border-bottom: 2px solid #1F4E79;
        padding-bottom: 6px;
        margin-bottom: 12px;
    }
    h2 {
        font-size: 14pt;
        color: #2E4057;
        border-bottom: 1px solid #ccc;
        padding-bottom: 4px;
        margin-top: 24px;
    }
    h3 {
        font-size: 11.5pt;
        color: #2E4057;
        margin-top: 18px;
        margin-bottom: 6px;
    }
    p { margin: 6px 0; }
    table {
        border-collapse: collapse;
        width: 100%;
        font-size: 9.5pt;
        margin: 12px 0;
    }
    th {
        background-color: #1F4E79;
        color: white;
        font-weight: bold;
        padding: 6px 10px;
        text-align: left;
        border: 1px solid #ccc;
    }
    td {
        padding: 5px 10px;
        border: 1px solid #ddd;
        vertical-align: top;
    }
    tr:nth-child(even) td { background-color: #F0F4F9; }
    tr:nth-child(odd)  td { background-color: #ffffff; }
    code {
        background: #f0f0f0;
        border-radius: 3px;
        padding: 1px 4px;
        font-family: "Consolas", monospace;
        font-size: 9pt;
    }
    strong { color: #1a1a1a; }
    hr { border: none; border-top: 1px solid #ccc; margin: 20px 0; }
    .meta { font-size: 10pt; color: #555; margin-bottom: 16px; }
"""

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{css}
</style>
</head>
<body>
{body_html}
</body>
</html>"""

HTML_FILE.write_text(html, encoding="utf-8")
print(f"HTML written: {HTML_FILE}")

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(HTML_FILE.as_uri())
    page.pdf(
        path=str(PDF_FILE),
        format="A4",
        margin={"top": "2cm", "bottom": "2cm", "left": "2.2cm", "right": "2.2cm"},
        print_background=True,
    )
    browser.close()

print(f"PDF saved: {PDF_FILE}")
