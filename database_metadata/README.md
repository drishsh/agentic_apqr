# Database Metadata Index

## Purpose

This folder contains comprehensive index files that map the entire `APQR_Segregated` database structure. These files help agents quickly locate specific documents without having to recursively search the entire directory tree.

## Index Files

### 1. **ERP_INDEX.txt**
- **Domain:** Enterprise Resource Planning
- **Coverage:** All ERP documents across 4 batches
- **Categories:**
  - Supply Chain (Purchase Orders, Requisition Slips, COAs, SDS, Shipment Details)
  - Manufacturing (BMRs, Dispensing Logs, Compression, Coating, Blending)
  - Engineering (Equipment Logs, Quarantine, Sampling, HVAC Monitoring)

### 2. **LIMS_INDEX.txt**
- **Domain:** Laboratory Information Management System
- **Coverage:** All LIMS/QC documents across 4 batches
- **Categories:**
  - Raw Material QC (COAs, SDS, Shipment Details)
  - Finished Product QC (Final COAs, IPC data)
  - Sampling Records (Sampling booth logs)
  - Quarantine Logs (GRN, Quarantine registers)
  - Packaging Material QC

### 3. **DMS_INDEX.txt**
- **Domain:** Document Management System
- **Coverage:** All regulatory and quality documents
- **Categories:**
  - Standard Operating Procedures (SOPs - Version 1 & 2)
  - Training Records (Training matrices, attendance, assessments)
  - CAPA Documents (Corrective/Preventive Actions for all batches)
  - Regulatory Documents (SDS register, DMF, Product specifications)

## How Agents Should Use These Indexes

### Step 1: Read the Relevant Index
Before searching the file system, agents should **first read the appropriate index file** based on their domain:
- `erp_*_agent` → Read `ERP_INDEX.txt`
- `lims_*_agent` → Read `LIMS_INDEX.txt`
- `dms_*_agent` → Read `DMS_INDEX.txt`

### Step 2: Identify the Target Files
Use the index to:
1. **Identify which batch** contains the data
2. **Identify the exact filename** or file pattern
3. **Identify the folder location**
4. **Understand what data** the file contains

### Step 3: Construct the Search Path
Use the information from the index to construct the exact file path:
```
APQR_Segregated/[DOMAIN]/[BATCH]/[SUBFOLDER]/[FILENAME]
```

### Step 4: Parse the Identified Files
Once the correct files are identified, use the appropriate parsing tools to extract data.

## Example Usage

### ❌ OLD METHOD (Inefficient):
```
Query: "Binder purchase order summary from all four batches"
Agent: Searches for "Purchase Order" in all files
Result: Only finds Batch 1 (because other batches use different naming: "Binder - ASP-25-002.docx")
```

### ✅ NEW METHOD (Using Index):
```
Query: "Binder purchase order summary from all four batches"
Agent: 
1. Reads ERP_INDEX.txt
2. Finds:
   - Batch 1: "Binder - Purchase Order.pdf"
   - Batch 2: "Binder - ASP-25-002.docx"
   - Batch 3: "Binder - ASP-25-003.docx"
   - Batch 4: "Binder - ASP-25-004.docx"
3. Searches for all 4 files specifically
4. Parses all 4 files
Result: Complete summary from ALL four batches ✅
```

## Key Benefits

1. **Faster Search**: No need to recursively scan thousands of files
2. **Complete Results**: Finds files even with inconsistent naming
3. **Batch-Aware**: Easily identifies which batch a file belongs to
4. **Content Preview**: Knows what data to expect before parsing
5. **Cross-Batch Queries**: Can easily aggregate data across multiple batches

## File Naming Patterns (From Index)

### Purchase Orders:
- **Batch 1**: `[Material] - Purchase Order.pdf`
- **Batch 2-4**: `[Material] - ASP-25-00X.docx`

### COAs:
- **Batch 1**: `COA_[Material].pdf`
- **Batch 2-4**: `COA_[Material]_ASP-25-00X.docx`

### Requisition Slips:
- **Batch 1**: `Req. Slip - [Material] - ASP-25-001.docx` to `ASP-25-010.docx`
- **Batch 2-4**: Not available

## Material Code Mapping

From the index, agents know:
- **API** = Salicylic Acid
- **Binder** = HPMC (Hydroxypropyl methyl cellulose)
- **Diluent** = MCC (Microcrystalline Cellulose)
- **Disintegrant** = Cornstarch
- **Lubricant** = Magnesium Stearate

## Batch Identification

- **Batch 1** = ASP-25-001 (Jan-Feb) → `Batch_1_Jan_Feb/`
- **Batch 2** = ASP-25-002 (Feb-Mar) → `Batch_2_Feb_Mar/`
- **Batch 3** = ASP-25-003 (Mar-Apr) → `Batch_3_Mar_Apr/`
- **Batch 4** = ASP-25-004 (Apr-May) → `Batch_4_Apr_May/`

## Maintenance

**When to Update:**
- New batches added to database
- Files renamed or moved
- New document types added
- Folder structure changes

**How to Update:**
Run the metadata generation script (to be created) or manually update the relevant index file.

---

**Last Updated:** 2025-11-10  
**Version:** 1.0

