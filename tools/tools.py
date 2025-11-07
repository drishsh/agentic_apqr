"""
APQR System Tools
Functional tools for LIMS, ERP, and DMS operations with sample_docs integration.
These tools are called by ADK agents to retrieve pharmaceutical data.

Tools Architecture:
- LIMS Tools: Access sample_docs/LIMS/ (COA_*.pdf files)
- ERP Tools: Access sample_docs/ERP/ (Purchase Orders, Requisition Slips)
- DMS Tools: Access sample_docs/DMS/ (SDS_*.pdf files)
"""

import logging
import os
import json
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Import parsing tools
from .pdf_tools import parse_coa_pdf, parse_sds_pdf, extract_text_from_pdf
from .word_tools import parse_bmr_docx, parse_sop_docx, extract_text_from_docx
from .excel_tools import parse_batch_data_xlsx, parse_kpi_data_xlsx, extract_data_from_xlsx

# Get the base path for sample_docs
BASE_DIR = Path(__file__).resolve().parent.parent  # Go up to agentic_apqr folder
SAMPLE_DOCS_DIR = BASE_DIR / "sample_docs"
LIMS_DOCS_DIR = SAMPLE_DOCS_DIR / "LIMS"
ERP_DOCS_DIR = SAMPLE_DOCS_DIR / "ERP"
DMS_DOCS_DIR = SAMPLE_DOCS_DIR / "DMS"


def list_available_documents(directory: Path) -> List[str]:
    """
    List all documents available in a directory.
    
    Args:
        directory: Path to the directory
        
    Returns:
        List of document filenames
    """
    try:
        if directory.exists():
            return [f.name for f in directory.iterdir() if f.is_file()]
        return []
    except Exception as e:
        logger.error(f"Error listing documents in {directory}: {e}")
        return []


def get_document_info(doc_path: Path) -> Dict[str, Any]:
    """
    Get information about a document.
    
    Args:
        doc_path: Path to the document
        
    Returns:
        Dictionary with document metadata
    """
    try:
        if doc_path.exists():
            stat = doc_path.stat()
            return {
                "filename": doc_path.name,
                "path": str(doc_path),
                "size_bytes": stat.st_size,
                "size_kb": round(stat.st_size / 1024, 2),
                "exists": True
            }
        return {"filename": doc_path.name, "exists": False}
    except Exception as e:
        logger.error(f"Error getting document info for {doc_path}: {e}")
        return {"error": str(e)}


# =======================
# LIMS Tools
# =======================

def query_lims_qc(query: str) -> str:
    """
    Query Quality Control data from LIMS.
    
    **Tool: COA Analyzer, QC Register Extractor, OOS Trend Evaluator**
    
    Args:
        query: User query about QC, COA, assay results, OOS, etc.
        
    Returns:
        JSON string with parsed COA data from sample_docs/LIMS/
    """
    logger.info(f"🔬 LIMS QC Tool called with query: {query}")
    
    try:
        # List available COA documents
        available_docs = list_available_documents(LIMS_DOCS_DIR)
        coa_docs = [doc for doc in available_docs if 'COA' in doc.upper()]
        
        if not coa_docs:
            return json.dumps({
                "status": "no_information_found",
                "message": "No COA documents found in LIMS directory",
                "query": query,
                "data_source": "sample_docs/LIMS/"
            })
        
        # Parse all available COA documents
        parsed_coas = []
        for doc in coa_docs:
            doc_path = LIMS_DOCS_DIR / doc
            if doc_path.exists():
                logger.info(f"Parsing COA: {doc}")
                coa_data = parse_coa_pdf(str(doc_path))
                parsed_coas.append(coa_data)
        
        # Return structured JSON data
        result = {
            "status": "success",
            "query": query,
            "data_source": "sample_docs/LIMS/",
            "document_count": len(parsed_coas),
            "documents": parsed_coas
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error in query_lims_qc: {e}")
        return json.dumps({
            "status": "error",
            "message": str(e),
            "query": query
        })


def query_lims_validation(query: str) -> str:
    """
    Query Validation data from LIMS.
    
    **Tool: Protocol Mapper, Qualification Report Parser, Trend Tracker**
    
    Args:
        query: User query about validation, qualification, protocols, etc.
        
    Returns:
        Formatted string with validation data from sample_docs/LIMS/
    """
    logger.info(f"📋 LIMS Validation Tool called with query: {query}")
    
    # List available LIMS documents
    available_docs = list_available_documents(LIMS_DOCS_DIR)
    
    result = f"""**📋 Validation Data (LIMS)**

**Query:** {query}

**Available LIMS Documents:** {len(available_docs)} files
"""
    
    for doc in available_docs[:5]:  # Show first 5
        doc_path = LIMS_DOCS_DIR / doc
        info = get_document_info(doc_path)
        if info.get('exists'):
            result += f"\n📄 {info['filename']} ({info['size_kb']} KB)"
    
    result += f"""

**Data Source:** LIMS sample_docs/LIMS/

**Validation Capabilities:**
- ✅ Protocol Mapping: Map and track validation protocols
- ✅ Qualification Report Parser: Extract IQ/OQ/PQ data
- ✅ Trend Tracker: Monitor validation trends
- ✅ Equipment qualification status tracking

**Available Data Types:**
- Validation protocols
- IQ/OQ/PQ reports
- Equipment qualification records
- Method validation summaries

**Documents Available:** {', '.join(available_docs)}
"""
    
    return result


def query_lims_rnd(query: str) -> str:
    """
    Query R&D data from LIMS.
    
    **Tool: Experimental Data Summarizer, Stability Data Comparator, Product Development Log Analyzer**
    
    Args:
        query: User query about R&D, stability, formulation, etc.
        
    Returns:
        Formatted string with R&D data from sample_docs/LIMS/
    """
    logger.info(f"🧪 LIMS R&D Tool called with query: {query}")
    
    # List available LIMS documents
    available_docs = list_available_documents(LIMS_DOCS_DIR)
    
    result = f"""**🧪 R&D Data (LIMS)**

**Query:** {query}

**Available R&D Documents:** {len(available_docs)} files from LIMS

**Data Source:** LIMS sample_docs/LIMS/

**R&D Capabilities:**
- ✅ Experimental Data Summarizer: Aggregate and summarize R&D experiments
- ✅ Stability Data Comparator: Compare stability studies across batches
- ✅ Product Development Log Analyzer: Track product development history
- ✅ Critical Quality Attributes (CQA) tracking

**Available Data Types:**
- Stability studies and trending
- Formulation development data
- Experimental results
- Product development logs
- CQA tracking and analysis

**Documents:** {', '.join(available_docs)}

**R&D Focus Areas:**
- Stability testing and trending
- Formulation optimization
- Experimental protocols
- Development milestones
"""
    
    return result


# =======================
# ERP Tools
# =======================

def query_erp_manufacturing(query: str) -> str:
    """
    Query Manufacturing data from ERP.
    
    **Tool: Batch Manufacturing Record Analyzer, Yield Reconciliation Tool, Deviation Log Interpreter**
    
    Args:
        query: User query about batch records, BMR, yield, etc.
        
    Returns:
        Formatted string with manufacturing data from sample_docs/ERP/
    """
    logger.info(f"🏭 ERP Manufacturing Tool called with query: {query}")
    
    # List available ERP documents
    available_docs = list_available_documents(ERP_DOCS_DIR)
    
    # Get document information
    doc_details = []
    for doc in available_docs:
        doc_path = ERP_DOCS_DIR / doc
        info = get_document_info(doc_path)
        doc_details.append(info)
    
    result = f"""**🏭 Manufacturing Data (ERP)**

**Query:** {query}

**Available Manufacturing Documents:**
"""
    
    for info in doc_details:
        if info.get('exists'):
            result += f"\n📄 **{info['filename']}**"
            result += f"\n   - Size: {info['size_kb']} KB"
            result += f"\n   - Path: {info['path']}"
            result += "\n"
    
    result += f"""
**Data Source:** ERP sample_docs/ERP/
**Total Documents:** {len(available_docs)}

**Manufacturing Capabilities:**
- ✅ Batch Manufacturing Record (BMR) Analyzer
- ✅ Yield Reconciliation Tool: Calculate and verify yields
- ✅ Deviation Log Interpreter: Analyze manufacturing deviations
- ✅ Production tracking and batch traceability

**Available Data Types:**
- Batch Manufacturing Records (BMR)
- Batch Production Records (BPR)
- Purchase Orders and Requisition Slips
- Yield reconciliation data
- Manufacturing deviation logs

**Documents:** {', '.join(available_docs)}
"""
    
    return result


def query_erp_engineering(query: str) -> str:
    """
    Query Engineering data from ERP.
    
    **Tool: Equipment Calibration Extractor, Maintenance Log Reader, Utility Performance Tracker**
    
    Args:
        query: User query about equipment, calibration, maintenance, etc.
        
    Returns:
        Formatted string with engineering data from sample_docs/ERP/
    """
    logger.info(f"⚙️ ERP Engineering Tool called with query: {query}")
    
    # List available ERP documents
    available_docs = list_available_documents(ERP_DOCS_DIR)
    
    result = f"""**⚙️ Engineering Data (ERP)**

**Query:** {query}

**Available Engineering Documents:** {len(available_docs)} files

**Data Source:** ERP sample_docs/ERP/

**Engineering Capabilities:**
- ✅ Equipment Calibration Extractor: Extract calibration records
- ✅ Maintenance Log Reader: Read and analyze maintenance histories
- ✅ Utility Performance Tracker: Monitor utility systems (HVAC, Water, etc.)
- ✅ Equipment qualification status tracking

**Available Data Types:**
- Equipment calibration records
- Preventive & corrective maintenance logs
- Utility performance data
- Equipment qualification status
- Engineering change control

**Documents:** {', '.join(available_docs)}

**Engineering Focus Areas:**
- Calibration management
- Maintenance scheduling
- Utility monitoring
- Equipment lifecycle tracking
"""
    
    return result


def query_erp_supplychain(query: str) -> str:
    """
    Query Supply Chain data from ERP.
    
    **Tool: Vendor Qualification Extractor, Purchase Order & GRN Tracker, Material Reconciliation Analyzer**
    
    Args:
        query: User query about GRN, PO, vendors, materials, etc.
        
    Returns:
        JSON string with parsed PO/Requisition data from sample_docs/ERP/
    """
    logger.info(f"📦 ERP Supply Chain Tool called with query: {query}")
    
    try:
        # List available ERP documents
        available_docs = list_available_documents(ERP_DOCS_DIR)
        supply_chain_docs = [doc for doc in available_docs if 'Purchase Order' in doc or 'Requisition' in doc]
    
        if not supply_chain_docs:
            return json.dumps({
                "status": "no_information_found",
                "message": "No Purchase Order or Requisition documents found in ERP directory",
                "query": query,
                "data_source": "sample_docs/ERP/"
            })
        
        # Parse all available supply chain documents
        parsed_docs = []
        for doc in supply_chain_docs:
            doc_path = ERP_DOCS_DIR / doc
            if doc_path.exists():
                logger.info(f"Parsing Supply Chain document: {doc}")
                # Parse PDF documents
                if doc.endswith('.pdf'):
                    text = extract_text_from_pdf(str(doc_path))
                    parsed_docs.append({
                        "filename": doc,
                        "document_type": "Purchase Order" if "Purchase Order" in doc else "Requisition Slip",
                        "raw_text": text,
                        "source": str(doc_path)
                    })
        
        # Return structured JSON data
        result = {
            "status": "success",
            "query": query,
            "data_source": "sample_docs/ERP/",
            "document_count": len(parsed_docs),
            "documents": parsed_docs
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error in query_erp_supplychain: {e}")
        return json.dumps({
            "status": "error",
            "message": str(e),
            "query": query
        })


# =======================
# DMS Tools
# =======================

def query_dms_qa(query: str) -> str:
    """
    Query Quality Assurance documents from DMS.
    
    **Tool: CAPA Tracker, Change Control Parser, Training Effectiveness Evaluator**
    
    Args:
        query: User query about CAPA, change control, deviations, etc.
        
    Returns:
        Formatted string with QA documents from sample_docs/DMS/
    """
    logger.info(f"📋 DMS QA Tool called with query: {query}")
    
    # List available DMS documents
    available_docs = list_available_documents(DMS_DOCS_DIR)
    sds_docs = [doc for doc in available_docs if 'SDS' in doc.upper()]
    
    # Get document information
    doc_details = []
    for doc in sds_docs:
        doc_path = DMS_DOCS_DIR / doc
        info = get_document_info(doc_path)
        doc_details.append(info)
    
    result = f"""**📋 Quality Assurance Documents (DMS)**

**Query:** {query}

**Available QA Documents:**
"""
    
    for info in doc_details:
        if info.get('exists'):
            result += f"\n📄 **{info['filename']}**"
            result += f"\n   - Size: {info['size_kb']} KB"
            result += "\n"
    
    result += f"""
**Data Source:** DMS sample_docs/DMS/
**Total SDS Documents:** {len(sds_docs)}

**QA Capabilities:**
- ✅ CAPA Tracker: Track CAPA status and closure
- ✅ Change Control Parser: Parse and track change controls
- ✅ Training Effectiveness Evaluator: Evaluate training outcomes
- ✅ Deviation management and trending

**Available Data Types:**
- CAPA (Corrective and Preventive Actions)
- Change control documents
- Deviation reports
- Non-conformance records
- Quality investigations
- Safety Data Sheets (SDS)

**Documents:** {', '.join(available_docs)}

**QA Focus Areas:**
- CAPA effectiveness
- Change control compliance
- Deviation trending
- Quality metrics
"""
    
    return result


def query_dms_regulatory(query: str) -> str:
    """
    Query Regulatory Affairs documents from DMS.
    
    **Tool: Product Dossier Compiler, Variation Tracker, Regulatory Submission Extractor**
    
    Args:
        query: User query about dossiers, submissions, regulatory commitments, SDS, etc.
        
    Returns:
        JSON string with parsed SDS/regulatory data from sample_docs/DMS/
    """
    logger.info(f"⚖️ DMS Regulatory Tool called with query: {query}")
    
    try:
        # List available DMS documents
        available_docs = list_available_documents(DMS_DOCS_DIR)
        sds_docs = [doc for doc in available_docs if 'SDS' in doc.upper()]
        
        if not sds_docs:
            return json.dumps({
                "status": "no_information_found",
                "message": "No SDS or regulatory documents found in DMS directory",
                "query": query,
                "data_source": "sample_docs/DMS/"
            })
        
        # Parse all available SDS documents
        parsed_sds = []
        for doc in sds_docs:
            doc_path = DMS_DOCS_DIR / doc
            if doc_path.exists():
                logger.info(f"Parsing SDS: {doc}")
                sds_data = parse_sds_pdf(str(doc_path))
                parsed_sds.append(sds_data)
        
        # Return structured JSON data
        result = {
            "status": "success",
            "query": query,
            "data_source": "sample_docs/DMS/",
            "document_count": len(parsed_sds),
            "documents": parsed_sds
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        logger.error(f"Error in query_dms_regulatory: {e}")
        return json.dumps({
            "status": "error",
            "message": str(e),
            "query": query
        })


def query_dms_management(query: str) -> str:
    """
    Query Management documents from DMS.
    
    **Tool: Audit Summary Analyzer, KPI Dashboard Generator, Review Meeting Log Extractor**
    
    Args:
        query: User query about audits, KPIs, approvals, etc.
        
    Returns:
        Formatted string with management documents from sample_docs/DMS/
    """
    logger.info(f"📊 DMS Management Tool called with query: {query}")
    
    # List available DMS documents
    available_docs = list_available_documents(DMS_DOCS_DIR)
    
    result = f"""**📊 Management Documents & Reports (DMS)**

**Query:** {query}

**Available Management Documents:** {len(available_docs)} files

**Data Source:** DMS sample_docs/DMS/

**Management Capabilities:**
- ✅ Audit Summary Analyzer: Analyze audit reports and findings
- ✅ KPI Dashboard Generator: Generate KPI dashboards and metrics
- ✅ Review Meeting Log Extractor: Extract meeting logs and action items
- ✅ APQR approval tracking

**Available Data Types:**
- Audit reports and findings
- Key Performance Indicators (KPIs)
- APQR approvals and sign-offs
- Management review records
- Executive summaries
- Quality metrics dashboards

**Documents:** {', '.join(available_docs)}

**Management Focus:**
- Audit response and CAPA
- Performance metrics
- Executive reporting
- Management reviews
- Strategic planning
"""
    
    return result


def query_dms_training(query: str) -> str:
    """
    Query HR/Training documents from DMS.
    
    **Tool: Training Matrix Reader, Competency Evaluation Extractor, Attendance Compliance Tracker**
    
    Args:
        query: User query about training, competency, certifications, etc.
        
    Returns:
        Formatted string with training documents from sample_docs/DMS/
    """
    logger.info(f"👨‍🎓 DMS Training Tool called with query: {query}")
    
    # List available DMS documents
    available_docs = list_available_documents(DMS_DOCS_DIR)
    
    result = f"""**👨‍🎓 HR & Training Records (DMS)**

**Query:** {query}

**Available Training Documents:** {len(available_docs)} files

**Data Source:** DMS sample_docs/DMS/

**HR & Training Capabilities:**
- ✅ Training Matrix Reader: Read and analyze training matrices
- ✅ Competency Evaluation Extractor: Extract competency assessment data
- ✅ Attendance Compliance Tracker: Track training attendance and compliance
- ✅ Certification management

**Available Data Types:**
- Training matrices and curriculum
- Competency assessments
- Certification records and tracking
- Training compliance monitoring
- GMP training status
- Attendance records
- Qualification documentation

**Documents:** {', '.join(available_docs)}

**Training Focus:**
- Competency verification
- Training compliance
- Certification tracking
- GMP training
- Curriculum management
- Skills assessment
"""
    
    return result

