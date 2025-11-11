"""
Document Renderer - Convert DOCX to HTML/Markdown for Beautiful Display
Formats APQR documents for rich display in chat interfaces like ChatGPT
"""

import sys
from pathlib import Path
from typing import Dict, Any
from docx import Document
from docx.shared import Pt
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
import html

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def docx_to_html(docx_path: str) -> str:
    """
    Convert a DOCX document to beautiful HTML with styling.
    This HTML can be rendered in web interfaces for document-like appearance.
    
    Args:
        docx_path: Path to the .docx file
        
    Returns:
        HTML string with embedded CSS styling
    """
    doc = Document(docx_path)
    
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Calibri', 'Arial', sans-serif;
            max-width: 850px;
            margin: 0 auto;
            padding: 40px;
            background: white;
            color: #333;
            line-height: 1.6;
        }
        
        h1 {
            text-align: center;
            color: #1a1a1a;
            font-size: 24px;
            font-weight: bold;
            margin: 30px 0;
            border-bottom: 2px solid #2c5aa0;
            padding-bottom: 10px;
        }
        
        h2 {
            color: #2c5aa0;
            font-size: 16px;
            font-weight: bold;
            margin: 25px 0 15px 0;
            border-left: 4px solid #2c5aa0;
            padding-left: 12px;
        }
        
        p {
            margin: 10px 0;
            text-align: justify;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        table th {
            background: #2c5aa0;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
            border: 1px solid #1a3d6b;
        }
        
        table td {
            padding: 10px 12px;
            border: 1px solid #ddd;
            background: white;
        }
        
        table tr:nth-child(even) {
            background: #f8f9fa;
        }
        
        table tr:hover {
            background: #e8f4f8;
        }
        
        .document-header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 8px;
        }
        
        .document-title {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .document-subtitle {
            font-size: 14px;
            opacity: 0.95;
        }
        
        .sign-off-table {
            background: #f8f9fa;
            border: 2px solid #2c5aa0;
            margin: 20px 0;
        }
        
        .data-not-available {
            color: #dc3545;
            font-style: italic;
        }
        
        .section-number {
            display: inline-block;
            background: #2c5aa0;
            color: white;
            width: 30px;
            height: 30px;
            line-height: 30px;
            text-align: center;
            border-radius: 50%;
            margin-right: 10px;
            font-weight: bold;
        }
        
        .page-break {
            page-break-after: always;
            margin: 40px 0;
            border-bottom: 2px dashed #ccc;
        }
        
        @media print {
            body {
                padding: 20px;
            }
            .page-break {
                page-break-after: always;
            }
        }
    </style>
</head>
<body>
"""
    
    # Process document
    for element in doc.element.body:
        if isinstance(element, CT_P):
            para = Paragraph(element, doc)
            html_content += _paragraph_to_html(para)
        elif isinstance(element, CT_Tbl):
            table = Table(element, doc)
            html_content += _table_to_html(table)
    
    html_content += """
</body>
</html>
"""
    
    return html_content


def _paragraph_to_html(para: Paragraph) -> str:
    """Convert paragraph to HTML with appropriate styling"""
    text = para.text.strip()
    
    if not text:
        return "<br>\n"
    
    # Check if it's a heading
    if para.style.name.startswith('Heading 1') or para.style.name == 'Title':
        return f"<h1>{html.escape(text)}</h1>\n"
    elif para.style.name.startswith('Heading'):
        return f"<h2>{html.escape(text)}</h2>\n"
    else:
        # Check for special markers
        if "[Data not available]" in text or "[Not specified" in text:
            # Escape first, then replace newlines with <br> (so <br> doesn't get escaped)
            escaped_text = html.escape(text)
            formatted_text = escaped_text.replace('\n', '<br>')
            return f'<p class="data-not-available">{formatted_text}</p>\n'
        else:
            # Preserve line breaks in multi-line paragraphs
            # Escape first to prevent XSS, then replace newlines with <br> (so <br> doesn't get escaped)
            escaped_text = html.escape(text)
            formatted_text = escaped_text.replace('\n', '<br>')
            return f"<p>{formatted_text}</p>\n"


def _table_to_html(table: Table) -> str:
    """Convert table to HTML with proper styling"""
    html_str = '<table>\n'
    
    # Process rows
    for i, row in enumerate(table.rows):
        html_str += '  <tr>\n'
        for cell in row.cells:
            cell_text = cell.text.strip()
            
            # First row is typically headers
            if i == 0:
                html_str += f'    <th>{html.escape(cell_text)}</th>\n'
            else:
                # Check for special values
                if "[Data not available]" in cell_text:
                    html_str += f'    <td class="data-not-available">{html.escape(cell_text)}</td>\n'
                else:
                    html_str += f'    <td>{html.escape(cell_text)}</td>\n'
        html_str += '  </tr>\n'
    
    html_str += '</table>\n'
    return html_str


def docx_to_markdown(docx_path: str) -> str:
    """
    Convert a DOCX document to Markdown format.
    Useful for platforms that render Markdown nicely.
    
    Args:
        docx_path: Path to the .docx file
        
    Returns:
        Markdown formatted string
    """
    doc = Document(docx_path)
    
    markdown = ""
    
    for element in doc.element.body:
        if isinstance(element, CT_P):
            para = Paragraph(element, doc)
            markdown += _paragraph_to_markdown(para)
        elif isinstance(element, CT_Tbl):
            table = Table(element, doc)
            markdown += _table_to_markdown(table)
    
    return markdown


def _paragraph_to_markdown(para: Paragraph) -> str:
    """Convert paragraph to Markdown"""
    text = para.text.strip()
    
    if not text:
        return "\n"
    
    # Headings
    if para.style.name.startswith('Heading 1') or para.style.name == 'Title':
        return f"\n# {text}\n\n"
    elif para.style.name.startswith('Heading 2'):
        return f"\n## {text}\n\n"
    elif para.style.name.startswith('Heading 3'):
        return f"\n### {text}\n\n"
    else:
        # Check for special markers
        if "[Data not available]" in text:
            return f"*{text}*\n\n"
        else:
            return f"{text}\n\n"


def _table_to_markdown(table: Table) -> str:
    """Convert table to Markdown format"""
    md = "\n"
    
    # Get column count from first row
    if not table.rows:
        return ""
    
    col_count = len(table.rows[0].cells)
    
    # Header row
    header_cells = [cell.text.strip() for cell in table.rows[0].cells]
    md += "| " + " | ".join(header_cells) + " |\n"
    md += "| " + " | ".join(["---"] * col_count) + " |\n"
    
    # Data rows
    for row in table.rows[1:]:
        cells = [cell.text.strip() for cell in row.cells]
        md += "| " + " | ".join(cells) + " |\n"
    
    md += "\n"
    return md


def render_apqr_for_display(docx_path: str, format: str = "html") -> Dict[str, Any]:
    """
    Main function to render APQR document in displayable format.
    
    Args:
        docx_path: Path to the DOCX file
        format: 'html' or 'markdown'
        
    Returns:
        Dictionary with rendered content and metadata
    """
    if format == "html":
        content = docx_to_html(docx_path)
        content_type = "text/html"
    elif format == "markdown":
        content = docx_to_markdown(docx_path)
        content_type = "text/markdown"
    else:
        raise ValueError(f"Unsupported format: {format}")
    
    return {
        "status": "success",
        "format": format,
        "content": content,
        "content_type": content_type,
        "file_path": docx_path
    }


if __name__ == "__main__":
    # Test with latest APQR
    from pathlib import Path
    
    output_dir = Path(__file__).resolve().parent.parent / "output" / "apqr_drafts"
    latest_file = max(output_dir.glob("*.docx"), key=lambda p: p.stat().st_mtime)
    
    print("=" * 80)
    print("RENDERING APQR AS HTML")
    print("=" * 80)
    
    result = render_apqr_for_display(str(latest_file), format="html")
    
    # Save HTML for viewing
    html_output = latest_file.with_suffix('.html')
    with open(html_output, 'w', encoding='utf-8') as f:
        f.write(result['content'])
    
    print(f"✅ HTML saved to: {html_output}")
    print(f"📄 Content length: {len(result['content'])} characters")
    print("\nPreview (first 500 chars):")
    print(result['content'][:500])

