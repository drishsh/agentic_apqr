# Database Metadata Implementation Plan

## ✅ COMPLETED

### 1. Created Database Metadata Folder
- Location: `/database_metadata/`
- Purpose: Store comprehensive index files for the entire APQR_Segregated database

### 2. Created Index Files
- **ERP_INDEX.txt**: Complete inventory of 700+ ERP files across 4 batches
- **LIMS_INDEX.txt**: Complete inventory of LIMS/QC files across 4 batches
- **DMS_INDEX.txt**: Complete inventory of DMS files (SOPs, Training, CAPA, Regulatory)
- **README.md**: Instructions for how agents should use these indexes

### 3. Index File Features
Each index includes:
- ✅ Batch-by-batch organization
- ✅ Folder structure mapping
- ✅ File naming patterns
- ✅ Content descriptions
- ✅ Material code mapping (API, Binder, Diluent, etc.)
- ✅ Batch identification (ASP-25-001 to ASP-25-004)
- ✅ Search tips for agents
- ✅ Document type categorization

## 🔄 NEXT STEPS (To Be Implemented)

### 1. Update Tool Functions (`tools/tools.py`)

#### Current Problem:
- `query_erp_supplychain()` only searches for files with "Purchase Order" or "Requisition" in the name
- Misses Batch 2-4 binder POs: "Binder - ASP-25-002.docx", "Binder - ASP-25-003.docx", "Binder - ASP-25-004.docx"

#### Solution:
Add index file reading at the start of each query function:

```python
def query_erp_supplychain(query: str) -> str:
    """Query ERP supply chain data (procurement)."""
    
    # NEW: Read the ERP index first
    index_file = BASE_DIR / "database_metadata" / "ERP_INDEX.txt"
    if index_file.exists():
        with open(index_file, 'r') as f:
            index_content = f.read()
        # Use index content to identify relevant files
        # Extract file paths based on query keywords
    
    # Then proceed with file parsing...
```

### 2. Update Sub-Agent Instructions

#### ERP Supply Chain Agent (`erp/supplychain_agent.py`)
**Add to instructions:**
```
🔍 CRITICAL - USE DATABASE INDEX:

Before searching for files, ALWAYS consult the database index:
- Location: database_metadata/ERP_INDEX.txt
- Purpose: Find exact file locations and naming patterns for all batches

KEY NAMING PATTERNS (from index):
- Batch 1 PO: "[Material] - Purchase Order.pdf"
- Batch 2-4 PO: "[Material] - ASP-25-00X.docx"
- Materials: API, Binder, Diluent, Disintegrant, Lubricant

EXAMPLE:
Query: "Binder purchase order for all batches"
1. Check ERP_INDEX.txt → Find 4 files:
   - Batch_1_Jan_Feb/SupplyChain/.../Binder - Purchase Order.pdf
   - Batch_2_Feb_Mar/SupplyChain/.../Binder - ASP-25-002.docx
   - Batch_3_Mar_Apr/SupplyChain/.../Binder - ASP-25-003.docx
   - Batch_4_Apr_May/SupplyChain/.../Binder - ASP-25-004.docx
2. Parse all 4 files
3. Return aggregated data
```

#### LIMS QC Agent (`lims/qc_agent.py`)
**Add to instructions:**
```
🔍 CRITICAL - USE DATABASE INDEX:

Before searching for files, ALWAYS consult the database index:
- Location: database_metadata/LIMS_INDEX.txt

KEY NAMING PATTERNS (from index):
- Batch 1 COA: "COA_[Material].pdf"
- Batch 2-4 COA: "COA_[Material]_ASP-25-00X.docx"

EXAMPLE:
Query: "COA for Lubricant from all batches"
1. Check LIMS_INDEX.txt → Find 4 files across all batches
2. Parse all 4 files
3. Return aggregated test results
```

#### DMS QA/Regulatory/Training Agents
**Add to instructions:**
```
🔍 CRITICAL - USE DATABASE INDEX:

Before searching for files, ALWAYS consult the database index:
- Location: database_metadata/DMS_INDEX.txt

KEY CATEGORIES (from index):
- SOPs: "13. List of all the SOPs/Version-2/" (current version)
- Training: "14. Comprehensive_training_records/training_matrices/"
- CAPA: "CAPA Documents/" (includes batch-specific CAPAs)

SOP NAMING: "SOP-[DEPT]-[NUMBER]_[Title].pdf"
Departments: MFG, QC, QA, ENG, WH, HR
```

### 3. Update Tool Docstrings

Add index file references to all domain-specific query tools:

```python
def query_lims_qc(query: str) -> str:
    """
    Query LIMS QC data.
    
    📋 USES DATABASE INDEX: database_metadata/LIMS_INDEX.txt
    This index contains file locations, naming patterns, and batch mapping for all LIMS documents.
    
    Args:
        query: Natural language query about QC data
        
    Returns:
        JSON string with COA data, test results, and specifications
        
    Data Source: APQR_Segregated/LIMS/
    """
```

### 4. Create Index Reading Utility Function

Add a helper function in `tools/tools.py`:

```python
def read_database_index(domain: str) -> str:
    """
    Read the database index for a specific domain.
    
    Args:
        domain: One of 'ERP', 'LIMS', 'DMS'
        
    Returns:
        Content of the index file as string
    """
    index_file = BASE_DIR / "database_metadata" / f"{domain}_INDEX.txt"
    if index_file.exists():
        with open(index_file, 'r', encoding='utf-8') as f:
            return f.read()
    return ""
```

### 5. Update Orchestrator Instructions

Add to `orchestrator_agent.py`:

```
🗂️ DATABASE STRUCTURE:

The system uses indexed metadata for efficient file location:
- database_metadata/ERP_INDEX.txt
- database_metadata/LIMS_INDEX.txt
- database_metadata/DMS_INDEX.txt

When routing queries involving multiple batches, inform domain agents to:
1. Consult the relevant index first
2. Identify ALL relevant files across batches
3. Aggregate results from all batches
```

## 📊 Expected Impact

### Before (Current Issue):
```
Query: "Binder PO summary from all four batches"
Result: Only Batch 1 found (3 batches missed)
Reason: Inconsistent file naming
```

### After (With Index):
```
Query: "Binder PO summary from all four batches"
Result: All 4 batches found and summarized ✅
Reason: Index maps all file naming patterns
```

## 🎯 Implementation Priority

1. **HIGH**: Update `query_erp_supplychain()` tool (fixes immediate binder PO issue)
2. **HIGH**: Update ERP Supply Chain agent instructions
3. **MEDIUM**: Update LIMS QC agent instructions
4. **MEDIUM**: Update all other sub-agent instructions
5. **LOW**: Create index reading utility function
6. **LOW**: Update orchestrator instructions

## 📝 Testing Plan

After implementation, test with these queries:
1. ✅ "Binder purchase order summary from all four batches" (should return 4 results)
2. ✅ "COA for API from all batches" (should return 4 COAs)
3. ✅ "Requisition slips for Lubricant in Batch 1" (should return 10 files)
4. ✅ "CAPA documents for Batch 4" (should return CAPA_004)
5. ✅ "Current version of SOP for tablet compression" (should return Version 2)

---

**Status:** Metadata indexes created ✅  
**Next:** Update tool functions and agent instructions  
**Owner:** To be implemented  
**Date Created:** 2025-11-10

