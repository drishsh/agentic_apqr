"""
PDF Tools - PDF parsing, extraction, and analysis tools.
Handles PDF document processing for LIMS, ERP, and DMS agents.
"""

import logging
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from PDF file.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text content
    """
    logger.info(f"Extracting text from PDF: {pdf_path}")
    
    try:
        path = Path(pdf_path)
        if not path.exists():
            return f"Error: File not found: {pdf_path}"
        
        text_content = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    text_content += f"\n--- Page {page_num} ---\n{page_text}\n"
        
        return text_content.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return f"Error: {str(e)}"


def extract_tables_from_pdf(pdf_path: str) -> List[Dict[str, Any]]:
    """
    Extract tables from PDF file.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        List of extracted tables with page numbers and data
    """
    logger.info(f"Extracting tables from PDF: {pdf_path}")
    
    try:
        path = Path(pdf_path)
        if not path.exists():
            return [{"error": f"File not found: {pdf_path}"}]
        
        all_tables = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                tables = page.extract_tables()
                for table_idx, table in enumerate(tables, 1):
                    all_tables.append({
                        "page": page_num,
                        "table_id": f"page{page_num}_table{table_idx}",
                        "data": table,
                        "rows": len(table),
                        "columns": len(table[0]) if table else 0
                    })
        
        return all_tables
    except Exception as e:
        logger.error(f"Error extracting tables from PDF: {e}")
        return [{"error": str(e)}]


def extract_metadata_from_pdf(pdf_path: str) -> Dict[str, Any]:
    """
    Extract metadata from PDF file.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Dictionary with PDF metadata
    """
    logger.info(f"Extracting metadata from PDF: {pdf_path}")
    
    try:
        path = Path(pdf_path)
        if path.exists():
            stat = path.stat()
            metadata = {
                "filename": path.name,
                "size_bytes": stat.st_size,
                "size_kb": round(stat.st_size / 1024, 2),
                "path": str(path),
                "exists": True
            }
            
            # Extract PDF-specific metadata
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    metadata["num_pages"] = len(pdf.pages)
                    metadata["pdf_metadata"] = pdf.metadata
            except Exception as e:
                logger.error(f"Error reading PDF metadata: {e}")
            
            return metadata
        return {"filename": path.name, "exists": False}
    except Exception as e:
        logger.error(f"Error extracting metadata from PDF: {e}")
        return {"error": str(e)}


def parse_coa_pdf(pdf_path: str) -> Dict[str, Any]:
    """
    Parse Certificate of Analysis (COA) from PDF.
    
    Args:
        pdf_path: Path to COA PDF file
        
    Returns:
        Structured COA data with material, batch, test results
    """
    logger.info(f"Parsing COA from PDF: {pdf_path}")
    
    try:
        text = extract_text_from_pdf(pdf_path)
        tables = extract_tables_from_pdf(pdf_path)
        
        # Extract material name (typically in filename or early in document)
        material_name = Path(pdf_path).stem.replace("COA_", "")
        
        # Parse structured data from text using regex patterns
        coa_data = {
            "document_type": "Certificate of Analysis (COA)",
            "material_name": material_name,
            "source": pdf_path,
            "raw_text": text,
            "tables": tables,
            "test_results": [],
            "metadata": extract_metadata_from_pdf(pdf_path)
        }
        
        # Extract batch/lot number patterns
        batch_patterns = [
            r"Batch\s*(?:Number|No\.?|#)?\s*:?\s*([A-Z0-9\-]+)",
            r"Lot\s*(?:Number|No\.?|#)?\s*:?\s*([A-Z0-9\-]+)"
        ]
        for pattern in batch_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                coa_data["batch_number"] = match.group(1)
                break
        
        # Extract test results from tables if available
        for table_info in tables:
            table_data = table_info.get("data", [])
            if table_data and len(table_data) > 1:
                # Assume first row is header
                headers = table_data[0]
                for row in table_data[1:]:
                    if len(row) == len(headers):
                        test_entry = dict(zip(headers, row))
                        coa_data["test_results"].append(test_entry)
        
        return coa_data
        
    except Exception as e:
        logger.error(f"Error parsing COA PDF: {e}")
        return {
            "document_type": "COA",
            "error": str(e),
            "source": pdf_path
        }


def parse_sds_pdf(pdf_path: str) -> Dict[str, Any]:
    """
    Parse Safety Data Sheet (SDS) from PDF.
    
    Args:
        pdf_path: Path to SDS PDF file
        
    Returns:
        Structured SDS data with hazards, handling, storage info
    """
    logger.info(f"Parsing SDS from PDF: {pdf_path}")
    
    try:
        text = extract_text_from_pdf(pdf_path)
        
        # Extract chemical name (typically in filename or early in document)
        chemical_name = Path(pdf_path).stem.replace("SDS_", "")
        
        sds_data = {
            "document_type": "Safety Data Sheet (SDS)",
            "chemical_name": chemical_name,
            "source": pdf_path,
            "raw_text": text,
            "sections": {},
            "hazards": [],
            "handling_precautions": [],
            "storage_conditions": [],
            "metadata": extract_metadata_from_pdf(pdf_path)
        }
        
        # Extract SDS sections (typically numbered 1-16)
        section_patterns = [
            (r"Section\s+1[:\.\s]+Identification", "identification"),
            (r"Section\s+2[:\.\s]+Hazard", "hazards"),
            (r"Section\s+3[:\.\s]+Composition", "composition"),
            (r"Section\s+4[:\.\s]+First[- ]?Aid", "first_aid"),
            (r"Section\s+5[:\.\s]+Fire[- ]?Fighting", "fire_fighting"),
            (r"Section\s+6[:\.\s]+Accidental\s+Release", "accidental_release"),
            (r"Section\s+7[:\.\s]+Handling\s+and\s+Storage", "handling_storage"),
            (r"Section\s+8[:\.\s]+Exposure\s+Controls", "exposure_controls"),
        ]
        
        for pattern, section_name in section_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                sds_data["sections"][section_name] = True
        
        # Extract hazard information
        hazard_patterns = [
            r"Hazard[s]?[:\s]+([^\n]+)",
            r"Danger[:\s]+([^\n]+)",
            r"Warning[:\s]+([^\n]+)"
        ]
        for pattern in hazard_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            sds_data["hazards"].extend(matches)
        
        # Extract storage conditions
        storage_patterns = [
            r"Storage[:\s]+([^\n]+)",
            r"Store\s+(?:in|at|under)\s+([^\n]+)"
        ]
        for pattern in storage_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            sds_data["storage_conditions"].extend(matches)
        
        return sds_data
        
    except Exception as e:
        logger.error(f"Error parsing SDS PDF: {e}")
        return {
            "document_type": "SDS",
            "error": str(e),
            "source": pdf_path
        }


def search_pdf_content(pdf_path: str, search_term: str) -> List[Dict[str, Any]]:
    """
    Search for specific content in PDF.
    
    Args:
        pdf_path: Path to PDF file
        search_term: Term to search for
        
    Returns:
        List of search results with page numbers and context
    """
    logger.info(f"Searching PDF {pdf_path} for term: {search_term}")
    
    try:
        path = Path(pdf_path)
        if not path.exists():
            return [{"error": f"File not found: {pdf_path}"}]
        
        results = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text and search_term.lower() in page_text.lower():
                    # Find all occurrences with context
                    lines = page_text.split('\n')
                    for line_num, line in enumerate(lines):
                        if search_term.lower() in line.lower():
                            # Get context (1 line before and after)
                            context_start = max(0, line_num - 1)
                            context_end = min(len(lines), line_num + 2)
                            context = '\n'.join(lines[context_start:context_end])
                            
                            results.append({
                                "page": page_num,
                                "line": line_num + 1,
                                "match": line.strip(),
                                "context": context
                            })
        
        return results
        
    except Exception as e:
        logger.error(f"Error searching PDF: {e}")
        return [{"error": str(e)}]

