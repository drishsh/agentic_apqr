"""
APQR System Tools Package
Centralized tools accessible to all agents (LIMS, ERP, DMS, and their sub-agents).

Tool Categories:
- PDF Tools: PDF parsing and extraction
- Word Tools: DOCX parsing and extraction
- Excel Tools: XLSX parsing and analysis
- Image Tools: Image processing (PNG, JPEG, JPG)
- OCR Tools: Optical Character Recognition
- Domain-Specific Tools: LIMS, ERP, DMS query tools
"""

# Import all tools from specialized modules
from .pdf_tools import (
    extract_text_from_pdf,
    extract_tables_from_pdf,
    extract_metadata_from_pdf,
    parse_coa_pdf,
    parse_sds_pdf,
    search_pdf_content
)

from .word_tools import (
    extract_text_from_docx,
    extract_tables_from_docx,
    parse_bmr_docx,
    parse_sop_docx,
    extract_metadata_from_docx
)

from .excel_tools import (
    extract_sheets_from_xlsx,
    extract_data_from_xlsx,
    parse_batch_data_xlsx,
    parse_kpi_data_xlsx,
    extract_metadata_from_xlsx
)

from .image_tools import (
    extract_text_from_image,
    analyze_chart_image,
    extract_metadata_from_image,
    process_screenshot
)

from .ocr_tools import (
    perform_ocr,
    perform_ocr_with_layout,
    extract_table_from_scanned_doc,
    extract_handwritten_text,
    batch_ocr
)

# Import domain-specific tools
from .tools import (
    # LIMS Tools
    query_lims_qc,
    query_lims_validation,
    query_lims_rnd,
    
    # ERP Tools
    query_erp_manufacturing,
    query_erp_engineering,
    query_erp_supplychain,
    
    # DMS Tools
    query_dms_qa,
    query_dms_regulatory,
    query_dms_management,
    query_dms_training
)

__all__ = [
    # PDF Tools
    'extract_text_from_pdf',
    'extract_tables_from_pdf',
    'extract_metadata_from_pdf',
    'parse_coa_pdf',
    'parse_sds_pdf',
    'search_pdf_content',
    
    # Word Tools
    'extract_text_from_docx',
    'extract_tables_from_docx',
    'parse_bmr_docx',
    'parse_sop_docx',
    'extract_metadata_from_docx',
    
    # Excel Tools
    'extract_sheets_from_xlsx',
    'extract_data_from_xlsx',
    'parse_batch_data_xlsx',
    'parse_kpi_data_xlsx',
    'extract_metadata_from_xlsx',
    
    # Image Tools
    'extract_text_from_image',
    'analyze_chart_image',
    'extract_metadata_from_image',
    'process_screenshot',
    
    # OCR Tools
    'perform_ocr',
    'perform_ocr_with_layout',
    'extract_table_from_scanned_doc',
    'extract_handwritten_text',
    'batch_ocr',
    
    # LIMS Tools
    'query_lims_qc',
    'query_lims_validation',
    'query_lims_rnd',
    
    # ERP Tools
    'query_erp_manufacturing',
    'query_erp_engineering',
    'query_erp_supplychain',
    
    # DMS Tools
    'query_dms_qa',
    'query_dms_regulatory',
    'query_dms_management',
    'query_dms_training'
]
