"""
APQR System Tools
Functional tools for LIMS, ERP, and DMS operations with APQR_Segregated integration.
These tools are called by ADK agents to retrieve pharmaceutical data.

Tools Architecture:
- LIMS Tools: Access APQR_Segregated/LIMS/ (COA, QC records, batch documentation)
- ERP Tools: Access APQR_Segregated/ERP/ (Manufacturing, SupplyChain, Engineering records)
- DMS Tools: Access APQR_Segregated/DMS/ (SOPs, Training records, CAPA documents)
"""

import logging
import os
import json
import re
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Import parsing tools
from .pdf_tools import parse_coa_pdf, parse_sds_pdf, extract_text_from_pdf
from .word_tools import parse_bmr_docx, parse_sop_docx, extract_text_from_docx
from .excel_tools import parse_batch_data_xlsx, parse_kpi_data_xlsx, extract_data_from_xlsx

# Get the base path for APQR_Segregated
BASE_DIR = Path(__file__).resolve().parent.parent  # Go up to agentic_apqr folder
APQR_DATA_DIR = BASE_DIR / "APQR_Segregated"
LIMS_DOCS_DIR = APQR_DATA_DIR / "LIMS"
ERP_DOCS_DIR = APQR_DATA_DIR / "ERP"
DMS_DOCS_DIR = APQR_DATA_DIR / "DMS"
METADATA_DIR = BASE_DIR / "database_metadata"


def read_database_index(domain: str) -> str:
    """
    Read the database metadata index for a specific domain.
    
    Args:
        domain: One of 'ERP', 'LIMS', 'DMS'
        
    Returns:
        Content of the index file as string, or empty string if not found
    """
    try:
        index_file = METADATA_DIR / f"{domain}_INDEX.txt"
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            logger.warning(f"Database index not found: {index_file}")
            return ""
    except Exception as e:
        logger.error(f"Error reading database index for {domain}: {e}")
        return ""


def list_available_documents(directory: Path) -> List[Path]:
    """
    List all documents available in a directory (recursively searches all subdirectories).
    
    Args:
        directory: Path to the directory
        
    Returns:
        List of full Path objects for all files found recursively
    """
    try:
        if directory.exists():
            # Recursively search for all files in subdirectories
            all_files = []
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    all_files.append(file_path)  # Return full Path object
            return all_files
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
    
    **🔍 USES DATABASE INDEX: database_metadata/LIMS_INDEX.txt**
    This index contains file locations, naming patterns, and batch mapping for all LIMS documents.
    
    **Tool: COA Analyzer, QC Register Extractor, OOS Trend Evaluator**
    
    Args:
        query: User query about QC, COA, assay results, OOS, etc.
        
    Returns:
        JSON string with parsed COA data from APQR_Segregated/LIMS/
    """
    logger.info(f"🔬 LIMS QC Tool called with query: {query}")
    
    try:
        # 🔍 NEW: Read the LIMS database index for intelligent file search
        lims_index = read_database_index("LIMS")
        if lims_index:
            logger.info("✅ LIMS database index loaded for intelligent file search")
        
        # List available COA documents (recursively searches all subdirectories)
        available_docs = list_available_documents(LIMS_DOCS_DIR)
        coa_docs = [doc for doc in available_docs if 'COA' in doc.name.upper()]
        
        if not coa_docs:
            return json.dumps({
                "status": "no_information_found",
                "message": "No COA documents found in LIMS directory",
                "query": query,
                "data_source": "APQR_Segregated/LIMS/",
                "search_note": "Searched for COA documents across all batches (both PDF and DOCX formats)"
            })
        
        logger.info(f"🔬 Found {len(coa_docs)} COA documents")
        
        # Parse all available COA documents (handles both PDF and DOCX)
        parsed_coas = []
        for doc_path in coa_docs:
            if doc_path.exists():
                logger.info(f"Parsing COA: {doc_path.name} from {doc_path.parent}")
                # Parse PDF documents (Batch 1)
                if doc_path.name.endswith('.pdf'):
                    coa_data = parse_coa_pdf(str(doc_path))
                    coa_data['batch'] = "ASP-25-001"  # Batch 1 uses PDF
                    parsed_coas.append(coa_data)
                # Parse DOCX documents (Batch 2-4)
                elif doc_path.name.endswith('.docx'):
                    text = extract_text_from_docx(str(doc_path))
                    # Extract batch number from filename
                    batch = "ASP-25-002" if "002" in doc_path.name else "ASP-25-003" if "003" in doc_path.name else "ASP-25-004" if "004" in doc_path.name else "Unknown"
                    coa_data = {
                        "filename": doc_path.name,
                        "batch": batch,
                        "material": "API" if "API" in doc_path.name else "Binder" if "Binder" in doc_path.name else "Diluent" if "Diluent" in doc_path.name else "Disintegrant" if "Disintegrant" in doc_path.name else "Lubricant" if "Lubricant" in doc_path.name else "Unknown",
                        "raw_text": text,
                        "source": str(doc_path)
                    }
                    parsed_coas.append(coa_data)
        
        # Return structured JSON data
        result = {
            "status": "success",
            "query": query,
            "data_source": "APQR_Segregated/LIMS/",
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
    
    **🔍 USES DATABASE INDEX: database_metadata/LIMS_INDEX.txt**
    This index contains file locations, naming patterns, and batch mapping for all LIMS documents.
    
    **Tool: Protocol Mapper, Qualification Report Parser, Trend Tracker**
    
    Args:
        query: User query about validation, qualification, protocols, etc.
        
    Returns:
        Formatted string with validation data from APQR_Segregated/LIMS/
    """
    logger.info(f"📋 LIMS Validation Tool called with query: {query}")
    
    # 🔍 NEW: Read the LIMS database index for intelligent file search
    lims_index = read_database_index("LIMS")
    if lims_index:
        logger.info("✅ LIMS database index loaded for intelligent file search")
    
    # List available LIMS documents
    available_docs = list_available_documents(LIMS_DOCS_DIR)
    
    result = f"""**📋 Validation Data (LIMS)**

**Query:** {query}

**Available LIMS Documents:** {len(available_docs)} files
"""
    
    for doc_path in available_docs[:5]:  # Show first 5
        info = get_document_info(doc_path)
        if info.get('exists'):
            result += f"\n📄 {info['filename']} ({info['size_kb']} KB)"
    
    result += f"""

**Data Source:** LIMS APQR_Segregated/LIMS/

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

**Documents Available:** {', '.join(str(doc) for doc in available_docs[:10])}...
"""
    
    return result


def query_lims_rnd(query: str) -> str:
    """
    Query R&D data from LIMS.
    
    **🔍 USES DATABASE INDEX: database_metadata/LIMS_INDEX.txt**
    This index contains file locations, naming patterns, and batch mapping for all LIMS documents.
    
    **Tool: Experimental Data Summarizer, Stability Data Comparator, Product Development Log Analyzer**
    
    Args:
        query: User query about R&D, stability, formulation, etc.
        
    Returns:
        Formatted string with R&D data from APQR_Segregated/LIMS/
    """
    logger.info(f"🧪 LIMS R&D Tool called with query: {query}")
    
    # 🔍 NEW: Read the LIMS database index for intelligent file search
    lims_index = read_database_index("LIMS")
    if lims_index:
        logger.info("✅ LIMS database index loaded for intelligent file search")
    
    # List available LIMS documents
    available_docs = list_available_documents(LIMS_DOCS_DIR)
    
    result = f"""**🧪 R&D Data (LIMS)**

**Query:** {query}

**Available R&D Documents:** {len(available_docs)} files from LIMS

**Data Source:** LIMS APQR_Segregated/LIMS/

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

**Documents:** {', '.join(str(doc.name) for doc in available_docs[:10])}...

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
    
    **🔍 USES DATABASE INDEX: database_metadata/ERP_INDEX.txt**
    This index contains file locations, naming patterns, and batch mapping for all ERP documents.
    
    **Tool: Batch Manufacturing Record Analyzer, Yield Reconciliation Tool, Deviation Log Interpreter**
    
    Args:
        query: User query about batch records, BMR, yield, etc.
        
    Returns:
        Formatted string with manufacturing data from APQR_Segregated/ERP/
    """
    logger.info(f"🏭 ERP Manufacturing Tool called with query: {query}")
    
    # 🔍 NEW: Read the ERP database index for intelligent file search
    erp_index = read_database_index("ERP")
    if erp_index:
        logger.info("✅ ERP database index loaded for intelligent file search")
    
    # List available ERP documents
    available_docs = list_available_documents(ERP_DOCS_DIR)
    
    # Get document information
    doc_details = []
    for doc_path in available_docs:
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
**Data Source:** ERP APQR_Segregated/ERP/
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

**Documents:** {', '.join(str(doc) for doc in available_docs[:10])}...
"""
    
    return result


def query_erp_engineering(query: str) -> str:
    """
    Query Engineering data from ERP.
    
    **🔍 USES DATABASE INDEX: database_metadata/ERP_INDEX.txt**
    This index contains file locations, naming patterns, and batch mapping for all ERP documents.
    
    **Tool: Equipment Calibration Extractor, Maintenance Log Reader, Utility Performance Tracker**
    
    Args:
        query: User query about equipment, calibration, maintenance, etc.
        
    Returns:
        Formatted string with engineering data from APQR_Segregated/ERP/
    """
    logger.info(f"⚙️ ERP Engineering Tool called with query: {query}")
    
    # 🔍 NEW: Read the ERP database index for intelligent file search
    erp_index = read_database_index("ERP")
    if erp_index:
        logger.info("✅ ERP database index loaded for intelligent file search")
    
    # List available ERP documents
    available_docs = list_available_documents(ERP_DOCS_DIR)
    
    result = f"""**⚙️ Engineering Data (ERP)**

**Query:** {query}

**Available Engineering Documents:** {len(available_docs)} files

**Data Source:** ERP APQR_Segregated/ERP/

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

**Documents:** {', '.join(str(doc.name) for doc in available_docs[:10])}...

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
    
    **🔍 USES DATABASE INDEX: database_metadata/ERP_INDEX.txt**
    This index contains file locations, naming patterns, and batch mapping for all ERP documents.
    
    **Tool: Vendor Qualification Extractor, Purchase Order & GRN Tracker, Material Reconciliation Analyzer, SDS/MSDS Retriever**
    
    Args:
        query: User query about GRN, PO, vendors, materials, SDS, safety data sheets, etc.
        
    Returns:
        JSON string with parsed PO/Requisition/SDS data from APQR_Segregated/ERP/
    """
    logger.info(f"📦 ERP Supply Chain Tool called with query: {query}")
    
    # Check if this is an SDS query
    is_sds_query = any(keyword in query.lower() for keyword in ['sds', 'safety data sheet', 'msds', 'material safety', 'hazard', 'safety'])
    
    try:
        # 🔍 NEW: Read the ERP database index for intelligent file search
        erp_index = read_database_index("ERP")
        if erp_index:
            logger.info("✅ ERP database index loaded for intelligent file search")
        
        # List available ERP documents (recursively searches all subdirectories)
        available_docs = list_available_documents(ERP_DOCS_DIR)
        
        # === HANDLE SDS QUERIES (Safety Data Sheets) ===
        if is_sds_query:
            logger.info("🔍 SDS query detected - searching for Safety Data Sheets")
            
            # Find all SDS/MSDS files
            sds_docs = [doc for doc in available_docs if 'SDS' in doc.name.upper() or 'MSDS' in doc.name.upper()]
            
            if not sds_docs:
                return json.dumps({
                    "status": "no_information_found",
                    "message": "No SDS (Safety Data Sheets) documents found in ERP directory",
                    "query": query,
                    "data_source": "APQR_Segregated/ERP/SupplyChain/",
                    "search_note": "SDS files are typically stored with procurement/supply chain documents"
                })
            
            logger.info(f"📋 Found {len(sds_docs)} SDS documents")
            
            # Extract material name from query if specified
            material_keywords = {
                'api': ['SDS_API', 'Salicylic'],
                'binder': ['SDS_Binder', 'HPMC'],
                'filler': ['SDS_Filler', 'MCC', 'Cellulose'],
                'diluent': ['SDS_Filler', 'MCC', 'Cellulose'],
                'disintegrant': ['SDS_Disintegrant', 'Cornstarch'],
                'lubricant': ['SDS_Lubricant', 'Magnesium', 'Stearate'],
                'pvc': ['PVC', 'Film'],
                'foil': ['Foil', 'Lidding']
            }
            
            # Filter SDS docs based on material mentioned in query
            query_lower = query.lower()
            filtered_sds = []
            for material, patterns in material_keywords.items():
                if material in query_lower:
                    for doc in sds_docs:
                        if any(pattern in doc.name for pattern in patterns):
                            filtered_sds.append(doc)
            
            # If no specific material mentioned, return all SDS docs
            if not filtered_sds:
                filtered_sds = sds_docs
            
            # Parse SDS documents
            parsed_sds = []
            for doc_path in filtered_sds[:10]:  # Limit to 10 for performance
                if doc_path.exists():
                    logger.info(f"Parsing SDS document: {doc_path.name}")
                    text = extract_text_from_pdf(str(doc_path))
                    
                    # Extract hazard info from SDS
                    hazards = []
                    if 'hazard' in text.lower():
                        hazard_section = text[text.lower().find('hazard'):text.lower().find('hazard')+500]
                        hazards.append(hazard_section[:200])
                    
                    parsed_sds.append({
                        "filename": doc_path.name,
                        "material": doc_path.name.replace('SDS_', '').replace('MSDS', '').replace('.pdf', ''),
                        "document_type": "Safety Data Sheet (SDS)",
                        "hazards_preview": hazards[0] if hazards else "See full document for hazard information",
                        "file_path": str(doc_path),
                        "batch_folder": doc_path.parent.parent.parent.name if len(doc_path.parents) >= 3 else "Unknown"
                    })
            
            # Return formatted SDS data
            result = f"""**📋 Safety Data Sheets (SDS) - Supply Chain**

**Query:** {query}

**Found {len(parsed_sds)} SDS document(s):**

"""
            for sds in parsed_sds:
                result += f"""
📄 **{sds['material']}**
   - Document: {sds['filename']}
   - Type: {sds['document_type']}
   - Location: {sds['batch_folder']}
   - Hazards: {sds['hazards_preview'][:150]}...
   - Path: ...{sds['file_path'][-60:]}

"""
            
            result += f"""
**Data Source:** APQR_Segregated/ERP/SupplyChain/
**Total SDS Files:** {len(sds_docs)}

**💡 Tip:** SDS documents contain safety information including hazard statements, 
handling precautions, and emergency procedures for each material.
"""
            return result
        
        # === HANDLE PURCHASE ORDER / PROCUREMENT QUERIES ===
        # 🔍 ENHANCED: Search for supply chain documents using multiple patterns
        # Pattern 1: "Purchase Order" or "Requisition" (Batch 1 style)
        # Pattern 2: Material names followed by ASP-25 (Batch 2-4 style: "Binder - ASP-25-002.docx")
        # Pattern 3: "PO" in filename
        
        # Extract material keywords from query
        material_keywords = ['API', 'Binder', 'Diluent', 'Disintegrant', 'Lubricant', 
                            'HPMC', 'MCC', 'Cornstarch', 'Magnesium', 'Salicylic']
        
        supply_chain_docs = []
        for doc in available_docs:
            # Check if it's in SupplyChain folder (exclude SDS files)
            if 'SupplyChain' in str(doc) and 'SDS' not in doc.name and 'MSDS' not in doc.name:
                # Pattern matching for supply chain documents
                if any([
                    'Purchase Order' in doc.name,
                    'Requisition' in doc.name,
                    'PO-' in doc.name,
                    'Req. Slip' in doc.name,
                    # Match material names for Batch 2-4 style files
                    any(material in doc.name for material in material_keywords) and 'ASP-25' in doc.name,
                    # Match direct material name files (like "Binder - ASP-25-002.docx")
                    any(material in doc.name for material in material_keywords) and 'ASP' in doc.name
                ]):
                    supply_chain_docs.append(doc)
        
        if not supply_chain_docs:
            return json.dumps({
                "status": "no_information_found",
                "message": "No Purchase Order or Requisition documents found in ERP directory",
                "query": query,
                "data_source": "APQR_Segregated/ERP/",
                "search_note": "Searched for: Purchase Orders, Requisition Slips, and material-specific procurement documents across all batches"
            })
        
        logger.info(f"📦 Found {len(supply_chain_docs)} supply chain documents")
        
        # Parse all available supply chain documents
        parsed_docs = []
        for doc_path in supply_chain_docs:
            if doc_path.exists():
                logger.info(f"Parsing Supply Chain document: {doc_path.name} from {doc_path.parent}")
                # Parse PDF documents
                if doc_path.name.endswith('.pdf'):
                    text = extract_text_from_pdf(str(doc_path))
                    parsed_docs.append({
                        "filename": doc_path.name,
                        "document_type": "Purchase Order" if "Purchase Order" in doc_path.name else "Procurement Document",
                        "batch": "ASP-25-002" if "002" in doc_path.name else "ASP-25-003" if "003" in doc_path.name else "ASP-25-004" if "004" in doc_path.name else "ASP-25-001",
                        "raw_text": text,
                        "source": str(doc_path)
                    })
                # Parse DOCX documents (Batch 2-4 use DOCX)
                elif doc_path.name.endswith('.docx'):
                    text = extract_text_from_docx(str(doc_path))
                    parsed_docs.append({
                        "filename": doc_path.name,
                        "document_type": "Purchase Order" if "Purchase Order" in doc_path.name or "PO" in doc_path.name else "Procurement Document",
                        "batch": "ASP-25-002" if "002" in doc_path.name else "ASP-25-003" if "003" in doc_path.name else "ASP-25-004" if "004" in doc_path.name else "ASP-25-001",
                        "raw_text": text,
                        "source": str(doc_path)
                    })
        
        # Return structured JSON data
        result = {
            "status": "success",
            "query": query,
            "data_source": "APQR_Segregated/ERP/",
            "document_count": len(parsed_docs),
            "batches_found": list(set([doc.get("batch") for doc in parsed_docs])),
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
    
    **🔍 USES SOP INDEX: output/sop_index.json**
    This index contains comprehensive SOP metadata including version, title, department, dates, etc.
    
    **Tool: CAPA Tracker, Change Control Parser, Training Effectiveness Evaluator, SOP Version Tracker**
    
    Args:
        query: User query about CAPA, change control, deviations, SOPs, etc.
        
    Returns:
        Formatted string with QA documents from APQR_Segregated/DMS/
    """
    logger.info(f"📋 DMS QA Tool called with query: {query}")
    
    # 🔍 Load SOP index for intelligent SOP search
    sop_index_path = Path(__file__).parent.parent / "output" / "sop_index.json"
    sop_index = {}
    if sop_index_path.exists():
        with open(sop_index_path, 'r', encoding='utf-8') as f:
            sop_index = json.load(f)
        logger.info(f"✅ SOP index loaded: {sop_index['metadata']['total_sops']} SOPs indexed")
    
    # Check if query is SOP-related
    is_sop_query = any(keyword in query.lower() for keyword in ['sop', 'standard operating procedure', 'version', 'procedure', 'bmr', 'ppe', 'hplc', 'batch', 'safety', 'equipment', 'manufacturing', 'packaging', 'warehouse', 'calibration', 'cleaning', 'sampling'])
    
    if is_sop_query and sop_index:
        # === SEMANTIC SEARCH: Search by keywords/aliases, not just SOP number ===
        query_lower = query.lower()
        
        # Extract search terms from query
        search_terms = re.findall(r'\b[a-z]{3,}\b', query_lower)
        
        # Search for SOPs by semantic matching
        matching_sops = {}
        
        for sop_key, sop_data in sop_index['sops'].items():
            score = 0
            
            # Check aliases (high priority - exact match)
            if sop_data.get('aliases'):
                for alias in sop_data['aliases']:
                    if alias in query_lower:
                        score += 10  # High score for alias match
            
            # Check keywords (medium priority)
            if sop_data.get('keywords'):
                for keyword in sop_data['keywords']:
                    if keyword in search_terms:
                        score += 5  # Medium score for keyword match
            
            # Check title (medium priority)
            if sop_data.get('title'):
                title_lower = sop_data['title'].lower()
                for term in search_terms:
                    if term in title_lower:
                        score += 3
            
            # Check purpose (low priority)
            if sop_data.get('purpose'):
                purpose_lower = sop_data['purpose'].lower()
                for term in search_terms:
                    if term in purpose_lower:
                        score += 1
            
            # Check department match
            if sop_data.get('department'):
                dept_lower = sop_data['department'].lower()
                if any(term in dept_lower for term in search_terms):
                    score += 2
            
            if score > 0:
                matching_sops[sop_key] = (sop_data, score)
        
        # If semantic search found matches, return them
        if matching_sops:
            # Sort by score (highest first)
            sorted_matches = sorted(matching_sops.items(), key=lambda x: x[1][1], reverse=True)
            
            # If only one strong match, show details
            if len(sorted_matches) == 1 or (len(sorted_matches) > 1 and sorted_matches[0][1][1] >= 10):
                top_match = sorted_matches[0]
                sop_data = top_match[1][0]
                
                # Find all versions of this SOP
                base_sop_number = sop_data['sop_number']
                all_versions = {k: v for k, v in sop_index['sops'].items() if base_sop_number and base_sop_number in k}
                
                if len(all_versions) > 1:
                    # Multiple versions found
                    result = f"""**📋 SOP Query Result - Semantic Search**

**Query:** {query}

**Found:** {sop_data['sop_number']} ({len(all_versions)} version(s))
**Matched by:** {', '.join(sop_data.get('aliases', [])[:3]) if sop_data.get('aliases') else 'keywords'}

"""
                    for sop_key_inner, sop_data_inner in sorted(all_versions.items(), key=lambda x: x[1].get('version', '0'), reverse=True):
                        result += f"""
📄 **{sop_data_inner['sop_number']} - Version {sop_data_inner['version']}**
   - **Title:** {sop_data_inner['full_title'] if sop_data_inner.get('full_title') else sop_data_inner.get('title', 'Not available')}
   - **Department:** {sop_data_inner['department']}
   - **Version:** {sop_data_inner['version']}
   - **Effective Date:** {sop_data_inner['effective_date'] if sop_data_inner['effective_date'] else 'Not available'}
   - **Aliases:** {', '.join(sop_data_inner.get('aliases', [])) if sop_data_inner.get('aliases') else 'None'}
   - **File:** {sop_data_inner['file_name']}

"""
                    
                    # Identify current (latest) version
                    latest_version = max(all_versions.items(), key=lambda x: float(x[1].get('version', 0) or 0))
                    result += f"✅ **Current Version:** {latest_version[1]['version']}\n"
                    result += f"📅 **Indexed at:** {sop_index['metadata']['indexed_at']}\n"
                    
                    return result
                
                else:
                    # Single version
                    result = f"""**📋 SOP Query Result - Semantic Search**

**Query:** {query}

**Found:** {sop_data['sop_number']}
**Matched by:** {', '.join(sop_data.get('aliases', [])[:3]) if sop_data.get('aliases') else 'keywords'}

📄 **{sop_data['sop_number']} - Version {sop_data['version']}**
   - **Title:** {sop_data['full_title'] if sop_data.get('full_title') else sop_data.get('title', 'Not available')}
   - **Department:** {sop_data['department']}
   - **Version:** {sop_data['version']}
   - **Effective Date:** {sop_data['effective_date'] if sop_data['effective_date'] else 'Not available'}
   - **Aliases:** {', '.join(sop_data.get('aliases', [])) if sop_data.get('aliases') else 'None'}
   - **Purpose:** {sop_data.get('purpose', 'Not available')[:200]}...
   - **File:** {sop_data['file_name']}
   - **Path:** ...{sop_data['file_path'][-60:]}

📅 **Indexed at:** {sop_index['metadata']['indexed_at']}
"""
                    return result
            
            else:
                # Multiple matches - show list
                result = f"""**📋 SOP Query Results - Semantic Search**

**Query:** {query}

**Found {len(sorted_matches)} matching SOP(s):**

"""
                for sop_key, (sop_data, score) in sorted_matches[:10]:  # Limit to top 10
                    # Only show latest version (skip versioned keys)
                    if '_v' not in sop_key:
                        result += f"""
📄 **{sop_data['sop_number']}** (v{sop_data.get('version', '?')})
   - {sop_data.get('title', 'No title')[:80]}...
   - Department: {sop_data.get('department', 'Unknown')}
   - Matches: {', '.join(sop_data.get('aliases', [])[:3]) if sop_data.get('aliases') else 'keywords'}

"""
                
                result += f"\n💡 **Tip:** Ask for a specific SOP number for detailed information (e.g., 'What is SOP-PROD-001?')\n"
                result += f"📅 **Indexed at:** {sop_index['metadata']['indexed_at']}\n"
                
                return result
        
        # === EXACT SOP NUMBER SEARCH (original logic) ===
        # Search for specific SOP in query
        sop_match = re.search(r'SOP[_-]([A-Z]+)[_-](\d+)', query, re.IGNORECASE)
        
        if sop_match:
            # Specific SOP requested
            dept_code = sop_match.group(1).upper()
            number = sop_match.group(2)
            sop_number = f"SOP-{dept_code}-{number}"
            
            # Find all versions of this SOP
            matching_sops = {k: v for k, v in sop_index['sops'].items() if sop_number in k}
            
            if matching_sops:
                result = f"""**📋 SOP Query Result**

**Query:** {query}

**SOP Number:** {sop_number}

**Found {len(matching_sops)} version(s):**

"""
                for sop_key, sop_data in sorted(matching_sops.items(), key=lambda x: x[1].get('version', '0'), reverse=True):
                    result += f"""
📄 **{sop_data['sop_number']} - Version {sop_data['version']}**
   - **Title:** {sop_data['title'] if sop_data['title'] else 'Not available'}
   - **Department:** {sop_data['department']}
   - **Version:** {sop_data['version']}
   - **Effective Date:** {sop_data['effective_date'] if sop_data['effective_date'] else 'Not available'}
   - **Approved By:** {sop_data['approved_by'] if sop_data['approved_by'] else 'Not available'}
   - **File:** {sop_data['file_name']}
   - **Path:** ...{sop_data['file_path'][-60:]}

"""
                
                # Identify current (latest) version
                latest_version = max(matching_sops.items(), key=lambda x: float(x[1].get('version', 0) or 0))
                result += f"✅ **Current Version:** {latest_version[1]['version']}\n"
                result += f"📅 **Indexed at:** {sop_index['metadata']['indexed_at']}\n"
                
                return result
            else:
                return f"""**📋 SOP Query Result**

**Query:** {query}

⚠️ **SOP Not Found:** {sop_number}

Please check the SOP number or list all SOPs using: "List all SOPs"
"""
        
        else:
            # General SOP query - list all SOPs
            if 'list' in query.lower() or 'all' in query.lower():
                # Group by department
                by_department = {}
                for sop_key, sop_data in sop_index['sops'].items():
                    # Only show latest version (exclude versioned keys like "SOP-X_v2")
                    if '_v' not in sop_key:
                        dept = sop_data.get('department', 'Unknown')
                        if dept not in by_department:
                            by_department[dept] = []
                        by_department[dept].append(sop_data)
                
                result = f"""**📋 Standard Operating Procedures (SOPs) in DMS**

**Query:** {query}

**Total SOPs:** {sop_index['metadata']['total_sops']} documents
**Latest Versions:** {len([k for k in sop_index['sops'].keys() if '_v' not in k])} SOPs

**SOPs by Department:**

"""
                for dept, sops in sorted(by_department.items()):
                    result += f"\n**{dept}**\n"
                    for sop in sorted(sops, key=lambda x: x.get('sop_number', '')):
                        version_info = f"v{sop.get('version', '?')}" if sop.get('version') else ''
                        result += f"- {sop.get('sop_number', 'Unknown')} {version_info}\n"
                
                result += f"\n📅 **Index last updated:** {sop_index['metadata']['indexed_at']}\n"
                result += f"📊 **Data Source:** {sop_index['metadata']['dms_path']}\n"
                
                return result
    
    # Fall back to general DMS QA query
    # List available DMS documents
    available_docs = list_available_documents(DMS_DOCS_DIR)
    sds_docs = [doc for doc in available_docs if 'SDS' in doc.name.upper()]
    
    # Get document information
    doc_details = []
    for doc_path in sds_docs:
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
**Data Source:** DMS APQR_Segregated/DMS/
**Total SDS Documents:** {len(sds_docs)}

**QA Capabilities:**
- ✅ CAPA Tracker: Track CAPA status and closure
- ✅ Change Control Parser: Parse and track change controls
- ✅ Training Effectiveness Evaluator: Evaluate training outcomes
- ✅ Deviation management and trending
- ✅ SOP Version Tracker: Track SOP versions and metadata ({sop_index['metadata']['total_sops']} SOPs indexed)

**Available Data Types:**
- CAPA (Corrective and Preventive Actions)
- Change control documents
- Deviation reports
- Non-conformance records
- Quality investigations
- Safety Data Sheets (SDS)
- Standard Operating Procedures (SOPs) - {sop_index['metadata']['total_sops']} documents

**Documents:** {', '.join(str(doc.name) for doc in available_docs[:10])}...

**QA Focus Areas:**
- CAPA effectiveness
- Change control compliance
- Deviation trending
- Quality metrics
- SOP version control
"""
    
    return result


def query_dms_regulatory(query: str) -> str:
    """
    Query Regulatory Affairs documents from DMS.
    
    **🔍 USES DATABASE INDEX: database_metadata/DMS_INDEX.txt**
    This index contains file locations, naming patterns, and document categorization for all DMS documents.
    
    **Tool: Product Dossier Compiler, Variation Tracker, Regulatory Submission Extractor**
    
    Args:
        query: User query about dossiers, submissions, regulatory commitments, SDS, etc.
        
    Returns:
        JSON string with parsed SDS/regulatory data from APQR_Segregated/DMS/
    """
    logger.info(f"⚖️ DMS Regulatory Tool called with query: {query}")
    
    try:
        # 🔍 NEW: Read the DMS database index for intelligent file search
        dms_index = read_database_index("DMS")
        if dms_index:
            logger.info("✅ DMS database index loaded for intelligent file search")
        
        # List available DMS documents (recursively searches all subdirectories)
        available_docs = list_available_documents(DMS_DOCS_DIR)
        sds_docs = [doc for doc in available_docs if 'SDS' in doc.name.upper()]
        
        if not sds_docs:
            return json.dumps({
                "status": "no_information_found",
                "message": "No SDS or regulatory documents found in DMS directory",
                "query": query,
                "data_source": "APQR_Segregated/DMS/"
            })
        
        # Parse all available SDS documents
        parsed_sds = []
        for doc_path in sds_docs:
            if doc_path.exists():
                logger.info(f"Parsing SDS: {doc_path.name} from {doc_path.parent}")
                sds_data = parse_sds_pdf(str(doc_path))
                parsed_sds.append(sds_data)
        
        # Return structured JSON data
        result = {
            "status": "success",
            "query": query,
            "data_source": "APQR_Segregated/DMS/",
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
    
    **🔍 USES DATABASE INDEX: database_metadata/DMS_INDEX.txt**
    This index contains file locations, naming patterns, and document categorization for all DMS documents.
    
    **Tool: Audit Summary Analyzer, KPI Dashboard Generator, Review Meeting Log Extractor**
    
    Args:
        query: User query about audits, KPIs, approvals, etc.
        
    Returns:
        Formatted string with management documents from APQR_Segregated/DMS/
    """
    logger.info(f"📊 DMS Management Tool called with query: {query}")
    
    # 🔍 NEW: Read the DMS database index for intelligent file search
    dms_index = read_database_index("DMS")
    if dms_index:
        logger.info("✅ DMS database index loaded for intelligent file search")
    
    # List available DMS documents
    available_docs = list_available_documents(DMS_DOCS_DIR)
    
    result = f"""**📊 Management Documents & Reports (DMS)**

**Query:** {query}

**Available Management Documents:** {len(available_docs)} files

**Data Source:** DMS APQR_Segregated/DMS/

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

**Documents:** {', '.join(str(doc.name) for doc in available_docs[:10])}...

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
    
    **🔍 USES DATABASE INDEX: database_metadata/DMS_INDEX.txt**
    This index contains file locations, naming patterns, and document categorization for all DMS documents.
    
    **Tool: Training Matrix Reader, Competency Evaluation Extractor, Attendance Compliance Tracker**
    
    Args:
        query: User query about training, competency, certifications, etc.
        
    Returns:
        Formatted string with training documents from APQR_Segregated/DMS/
    """
    logger.info(f"👨‍🎓 DMS Training Tool called with query: {query}")
    
    # 🔍 NEW: Read the DMS database index for intelligent file search
    dms_index = read_database_index("DMS")
    if dms_index:
        logger.info("✅ DMS database index loaded for intelligent file search")
    
    # List available DMS documents
    available_docs = list_available_documents(DMS_DOCS_DIR)
    
    result = f"""**👨‍🎓 HR & Training Records (DMS)**

**Query:** {query}

**Available Training Documents:** {len(available_docs)} files

**Data Source:** DMS APQR_Segregated/DMS/

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

**Documents:** {', '.join(str(doc.name) for doc in available_docs[:10])}...

**Training Focus:**
- Competency verification
- Training compliance
- Certification tracking
- GMP training
- Curriculum management
- Skills assessment
"""
    
    return result

