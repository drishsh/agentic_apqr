# APQR Agentic System

**Advanced Pharmaceutical Quality & Records Management System**

A sophisticated multi-agent AI system for pharmaceutical quality assurance, APQR (Annual Product Quality Review) generation, and comprehensive records management. Built with Google's Agent Development Kit (ADK) using Gemini 2.5 Pro, the system features sequential workflow execution with automatic handoffs, real-time progress tracking, and intelligent data extraction from ERP, LIMS, and DMS databases.

---

## 🏗️ System Architecture

### **Sequential Multi-Domain Workflow with Auto-Handoffs**

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER QUERY                               │
│  "Summarize complete quality documentation for Disintegrant"     │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR AGENT                            │
│  • Analyzes query and identifies required domains (LIMS/ERP/DMS)│
│  • Routes to FIRST domain (sequential execution)                │
│  • Handles Compiler handoffs for next domain routing            │
│  • Tracks completed domains via conversation history            │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      LIMS DOMAIN AGENT                           │
│  Routes to: QC Sub-Agent, Validation Sub-Agent, R&D Sub-Agent   │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LIMS QC SUB-AGENT                             │
│  • Queries COA, IPQC, stability data                            │
│  • Extracts test results from LIMS database                      │
│  • Sends data directly to Compiler Agent                         │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     COMPILER AGENT                               │
│  • Receives LIMS data                                            │
│  • Shows progress: "📊 ✅ LIMS ⏳ ERP ⏳ DMS"                    │
│  • Stores data internally                                        │
│  • AUTOMATICALLY transfers to Orchestrator:                      │
│    "LIMS data received. Need ERP and DMS. Route to next domain." │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              ORCHESTRATOR AGENT (Handoff)                        │
│  • Receives Compiler handoff                                     │
│  • Routes to NEXT domain (ERP)                                   │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      ERP DOMAIN AGENT                            │
│  Routes to: Manufacturing, Engineering, Supply Chain Sub-Agents  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                ERP SUPPLY CHAIN SUB-AGENT                        │
│  • Queries Purchase Orders, GRNs, SDS documents                  │
│  • Extracts procurement and safety data                          │
│  • Sends data directly to Compiler Agent                         │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     COMPILER AGENT                               │
│  • Receives ERP data                                             │
│  • Shows progress: "📊 ✅ LIMS ✅ ERP ⏳ DMS"                    │
│  • AUTOMATICALLY transfers to Orchestrator:                      │
│    "LIMS and ERP data received. Need DMS. Route to next domain." │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              ORCHESTRATOR AGENT (Handoff)                        │
│  • Receives Compiler handoff                                     │
│  • Routes to FINAL domain (DMS)                                  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DMS DOMAIN AGENT                            │
│  Routes to: QA, Regulatory, Management, Training Sub-Agents      │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DMS QA SUB-AGENT                              │
│  • Queries SOPs, deviations, CAPAs, change controls             │
│  • Uses semantic SOP search (62 indexed SOPs)                    │
│  • Sends data directly to Compiler Agent                         │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     COMPILER AGENT                               │
│  • Receives DMS data (ALL domains complete)                      │
│  • Shows progress: "📊 ✅ LIMS ✅ ERP ✅ DMS - All received!"   │
│  • Cross-verifies data from all 3 domains                        │
│  • Generates COMPREHENSIVE FINAL REPORT                          │
│  • STOPS HERE - no more transfers                                │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│               COMPILED RESPONSE TO USER                          │
│  • Laboratory & QC Summary (LIMS)                                │
│  • Supply Chain & Procurement Summary (ERP)                      │
│  • Regulatory & Safety Summary (DMS)                             │
│  • Cross-verification analysis                                   │
│  • Final recommendations                                         │
└─────────────────────────────────────────────────────────────────┘
```

### **Key Architectural Features:**
- ✅ **Sequential Execution:** One domain at a time (LIMS → ERP → DMS)
- ✅ **Auto-Handoffs:** Compiler automatically triggers Orchestrator for next domain
- ✅ **Real-Time Progress:** User sees live updates ("📊 ✅ LIMS ⏳ ERP ⏳ DMS")
- ✅ **No User Prompting:** System completes multi-domain queries automatically
- ✅ **Domain/Sub-Agent Structure:** Hierarchical routing for specialized queries

---

## 📁 Project Structure

```
agentic_apqr/
├── README.md                                # This file
├── requirements.txt                         # Python dependencies
├── __init__.py                             # Package initialization
│
├── agents/                                 # Agent implementations
│   ├── __init__.py
│   ├── orchestrator_agent.py              # Main orchestrator (sequential routing)
│   ├── compiler_agent.py                  # Response synthesis with auto-handoffs
│   ├── apqr_data_filler_agent.py         # APQR document generator (NEW)
│   │
│   ├── lims_domain_agent.py              # LIMS router
│   ├── erp_domain_agent.py               # ERP router
│   ├── dms_domain_agent.py               # DMS router
│   │
│   └── [lims/erp/dms]/                   # Sub-agents by domain
│       ├── qc_agent.py                   # LIMS QC
│       ├── validation_agent.py           # LIMS Validation
│       ├── rnd_agent.py                  # LIMS R&D
│       ├── manufacturing_agent.py        # ERP Manufacturing
│       ├── engineering_agent.py          # ERP Engineering
│       ├── supplychain_agent.py          # ERP Supply Chain
│       ├── qa_agent.py                   # DMS QA
│       ├── regulatory_agent.py           # DMS Regulatory
│       ├── management_agent.py           # DMS Management
│       └── training_agent.py             # DMS Training
│
├── tools/                                  # Specialized tools
│   ├── __init__.py
│   ├── tools.py                          # Domain-specific query tools
│   ├── apqr_filler_tools.py              # APQR generation tools (NEW)
│   ├── apqr_generator_from_index.py      # Real data extraction (NEW)
│   ├── document_index_builder.py         # Database indexer (NEW)
│   ├── document_renderer.py              # HTML rendering (NEW)
│   ├── sop_index_builder.py              # SOP semantic search (NEW)
│   ├── pdf_tools.py                      # PDF parsing
│   ├── docx_tools.py                     # Word document parsing
│   ├── xlsx_tools.py                     # Excel parsing
│   └── ocr_tools.py                      # OCR processing
│
├── output/                                 # Generated outputs
│   ├── apqr_drafts/                      # Generated APQR documents
│   │   ├── APQR_111125_1245.docx        # Word format
│   │   └── APQR_111125_1245.html        # HTML format
│   ├── document_index.json               # Real data index
│   ├── sop_index.json                    # SOP index (62 SOPs)
│   └── capa_extracted_data.json          # CAPA data
│
├── APQR_Segregated/                       # Data directories
│   ├── LIMS/                             # Laboratory data
│   ├── ERP/                              # Manufacturing & procurement data
│   └── DMS/                              # Document management data
│
├── assets/                                 # Test data and configs
│   └── test_questions.md                 # 65 comprehensive test cases
│
└── documentation/                          # Guides
    ├── INTEGRATION_GUIDE_DATA_FILLER.md  # APQR Filler integration
    ├── MULTI_DOMAIN_QUERY_FIX.md         # Sequential workflow guide
    └── SEMANTIC_SOP_SEARCH_GUIDE.md      # SOP search implementation
```

---

## 🎯 Key Features

### **1. Sequential Multi-Domain Workflow (NEW)**
- **No User Prompting Required:** System automatically queries all required domains
- **Real-Time Progress Tracking:** Live updates show which agents have responded
- **Automatic Handoffs:** Compiler triggers Orchestrator to route to next domain
- **Clear Completion:** System stops only when all data is collected

**Example User Experience:**
```
User: "Summarize complete quality documentation for Disintegrant"

→ Orchestrator: "Routing to LIMS domain for test results..."
→ 📊 ✅ LIMS QC Agent - Data received ⏳ ERP - Waiting... ⏳ DMS - Waiting...
→ Orchestrator: "Routing to ERP domain for procurement records..." [AUTOMATIC]
→ 📊 ✅ LIMS ✅ ERP Agent - Data received ⏳ DMS - Waiting...
→ Orchestrator: "Routing to DMS domain for regulatory documentation..." [AUTOMATIC]
→ 📊 ✅ LIMS ✅ ERP ✅ DMS Agent - Data received. All data received!
→ [COMPREHENSIVE FINAL REPORT WITH ALL 3 DOMAINS' DATA]
```

### **2. APQR Filler Agent (NEW)**
Automatically generates populated APQR (Annual Product Quality Review) documents:
- **Real Data Extraction:** No fabrication, only data from `document_index.json`
- **24 Sections:** Complete APQR structure (Product Details, Batches, Yields, Deviations, Stability, etc.)
- **HTML Rendering:** Beautiful, formatted documents for web display
- **Clickable Output:** Returns success message + HTML link (localhost:8080)
- **Strict Role:** ONLY handles APQR generation, redirects all other queries

**Usage:**
```
User: "Generate APQR document for Aspirin 325"
→ APQR Filler extracts data from LIMS, ERP, DMS
→ Generates complete 24-section APQR document
→ Returns: "✅ APQR document generated successfully"
           "📄 View document: http://localhost:8080/APQR_111125_1245.html"
```

### **3. SOP Semantic Search (NEW)**
Intelligent SOP retrieval using keywords and aliases:
- **62 Indexed SOPs** with metadata (version, department, effective date)
- **Semantic Matching:** Understands "BMR" → SOP-PROD-001, "PPE" → SOP-HSE-001
- **Keyword Aliases:** Maps common terms to technical SOP names
- **Department Grouping:** Lists all SOPs by department (Production, QA, HSE, etc.)

**Example:**
```
User: "What is the current version of the SOP for batch manufacturing?"
→ Semantic search recognizes "batch manufacturing" = BMR = SOP-PROD-001
→ Returns: "SOP-PROD-001 (Batch Manufacturing Record - BMR) - Version 2"
```

### **4. SDS Routing to ERP (CORRECTED)**
Safety Data Sheets (SDS/MSDS) are now correctly routed:
- **Previous:** DMS Regulatory (incorrect, "not found")
- **Current:** ERP Supply Chain (correct location, 28 SDS documents)
- **Automatic Detection:** Queries with "SDS", "MSDS", "safety data sheet" → ERP
- **Hazard Extraction:** Parses SDS for safety information

### **5. Orchestrator Agent**
**Sequential Routing with Auto-Handoffs:**
- Analyzes query to identify ALL required domains (LIMS, ERP, DMS)
- Routes to FIRST domain only (typically LIMS for test data)
- Waits for Compiler handoff message
- Routes to NEXT pending domain (ERP if LIMS done, DMS if ERP done)
- Priority order: LIMS → ERP → DMS

**Routing Keywords:**
- **LIMS:** assay, impurity, OOS, COA, Certificate of Analysis, stability, validation, LIMS, QC data, test results, analytical
- **ERP:** batch yield, manufacturing, MBR, BMR, equipment, calibration, supply chain, vendor, raw material, purchase order, PO, GRN, batch record, production, **SDS, MSDS, safety data sheet, material safety, hazard**
- **DMS:** deviation, CAPA, change control, OOT, audit, regulatory, training, SOP, QMS, management review, dossier, submission

**Multi-Domain Patterns:**
- "complete documentation" → LIMS + ERP + DMS
- "comprehensive", "full", "all records" → ALL domains
- "test results + procurement" → LIMS + ERP
- "test results + safety" → LIMS + ERP (SDS in ERP)

### **6. Compiler Agent**
**Synthesis with Auto-Handoffs:**
- Receives data from sub-agents (LIMS QC, ERP Supply Chain, DMS QA, etc.)
- Shows real-time progress updates after each agent responds
- **Analyzes:** Are all required domains complete?
  - **No:** Automatically calls `transfer_to_agent("orchestrator_agent", "Need [domains]. Route to next.")`
  - **Yes:** Generates comprehensive final report
- Cross-verifies data from multiple domains
- Detects discrepancies and flags contradictions
- Generates user-friendly summary with citations

**Compilation Features:**
- Deduplication of redundant information
- Prioritization by relevance
- Contradiction detection
- Citation tracking (shows which agents provided data)
- Transparency reporting for data gaps

### **7. Domain & Sub-Agents**

#### **LIMS Domain Agent**
Routes to:
- **QC Sub-Agent:** COA, IPQC, assay results, impurity testing
- **Validation Sub-Agent:** Method validation, equipment qualification
- **R&D Sub-Agent:** Stability studies, formulation data

#### **ERP Domain Agent**
Routes to:
- **Manufacturing Sub-Agent:** BMR, batch yields, production schedules
- **Engineering Sub-Agent:** Equipment calibration, maintenance, HVAC
- **Supply Chain Sub-Agent:** Purchase Orders, GRNs, vendor data, **SDS documents**

#### **DMS Domain Agent**
Routes to:
- **QA Sub-Agent:** SOPs, deviations, change controls, CAPAs
- **Regulatory Sub-Agent:** Regulatory submissions, dossiers, audits
- **Management Sub-Agent:** Management review, quality metrics
- **Training Sub-Agent:** Training records, competency assessments

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.11 or higher required
python --version

# Google ADK installed
pip install google-adk

# Install dependencies
pip install -r requirements.txt
```

### Installation

```bash
# Navigate to project directory
cd agentic_apqr

# Start ADK web interface
adk web
```

### Running the System

```bash
# Start ADK web server (default port: auto-assigned)
adk web

# Or specify port
adk web --port 8080

# Access web interface at http://localhost:<port>
```

---

## 💡 Usage Examples

### **Example 1: Comprehensive Multi-Domain Query**

```
User: "Summarize the complete quality documentation available for 
       Disintegrant including test results, procurement records, and 
       safety information."

Expected Flow:
1. Orchestrator detects "complete" + "quality documentation" → ALL 3 domains
2. Routes to LIMS → LIMS QC extracts COA data → Sends to Compiler
3. Compiler shows "📊 ✅ LIMS ⏳ ERP ⏳ DMS" → Transfers to Orchestrator
4. Orchestrator routes to ERP → ERP Supply Chain extracts PO + SDS → Sends to Compiler
5. Compiler shows "📊 ✅ LIMS ✅ ERP ⏳ DMS" → Transfers to Orchestrator
6. Orchestrator routes to DMS → DMS QA extracts regulatory docs → Sends to Compiler
7. Compiler shows "📊 ✅ LIMS ✅ ERP ✅ DMS - All received"
8. Compiler generates final comprehensive report with all 3 domains' data

Result:
✓ Laboratory & QC Summary (LIMS): COA data with test results
✓ Supply Chain Summary (ERP): Procurement records and SDS hazard info
✓ Regulatory Summary (DMS): SOPs and quality documentation
✓ Cross-verification: All data verified, no contradictions found
✓ Final recommendation provided

NO USER PROMPTING REQUIRED!
```

### **Example 2: APQR Document Generation**

```
User: "Generate APQR document for Aspirin 325mg"

Expected Flow:
1. Orchestrator detects "generate APQR" → Routes to APQR Filler Agent
2. APQR Filler queries LIMS (test results), ERP (batch data), DMS (deviations)
3. Extracts real data from document_index.json
4. Populates all 24 APQR sections
5. Generates Word document + HTML version
6. Returns clickable link

Result:
✅ APQR document generated successfully
📄 View document: http://localhost:8080/APQR_111125_1245.html

Document includes:
- Section 1: Product Details
- Section 2: Number of Batches Manufactured (4 batches)
- Section 5: API Critical Parameters
- Section 11: Yield of All Critical Stages
- Section 17: Deviation Review (with detailed CAPA data)
- Section 21: Stability Monitoring Programme Results
- ... and 18 more sections
```

### **Example 3: SOP Semantic Search**

```
User: "What is the current version of the SOP for batch manufacturing?"

Expected Flow:
1. Orchestrator detects "SOP" → Routes to DMS QA
2. DMS QA loads sop_index.json (62 SOPs)
3. Semantic search: "batch manufacturing" → Keywords: ["batch", "manufacturing", "BMR"]
4. Matches SOP-PROD-001 with alias "BMR"
5. Returns metadata

Result:
📋 SOP-PROD-001: Batch Manufacturing Record (BMR)
   - Version: 2
   - Department: Production
   - Effective Date: 2025-01-15
   - Status: Current
   - File: SOP-PROD-001.pdf
```

### **Example 4: SDS Query (Corrected Routing)**

```
User: "What are the safety hazards listed in the SDS for API?"

Expected Flow:
1. Orchestrator detects "SDS" → Routes to ERP Supply Chain (NOT DMS!)
2. ERP Supply Chain searches for SDS_API.pdf
3. Extracts hazard information
4. Returns safety data

Result:
📋 Safety Data Sheets (SDS) - Supply Chain

**Material:** Salicylic Acid (API)
- Document: SDS_API.pdf
- Type: Safety Data Sheet (SDS)
- Hazards: Causes skin irritation. Causes serious eye irritation. 
           May cause respiratory irritation...
- Precautions: Wear protective gloves/eye protection. Use in well-ventilated area.
- Path: APQR_Segregated/ERP/SupplyChain/SDS_API.pdf
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Google API Key (required for Gemini 2.5 Pro)
export GOOGLE_API_KEY="your-api-key-here"

# ADK Configuration
export ADK_LOG_LEVEL="INFO"
export ADK_PORT="8080"
```

### Agent Configuration

Edit agent instructions in `agents/*.py` files to customize:
- Routing keywords
- Tool permissions
- Response formats
- Temperature settings (currently 0.1 for consistency)

---

## 📊 Data Sources

### **APQR_Segregated Directory Structure:**

```
APQR_Segregated/
├── LIMS/
│   ├── QC/
│   │   ├── COA_*.pdf                    # Certificates of Analysis
│   │   ├── IPQC_*.xlsx                  # In-Process QC results
│   │   └── Stability_*.docx             # Stability studies
│   ├── Validation/
│   │   └── Method_Validation_*.pdf
│   └── R&D/
│       └── Formulation_*.xlsx
│
├── ERP/
│   ├── Manufacturing/
│   │   ├── BMR_*.pdf                    # Batch Manufacturing Records
│   │   └── Yield_*.xlsx                 # Batch yields
│   ├── Engineering/
│   │   ├── Calibration_*.pdf
│   │   └── Maintenance_*.xlsx
│   └── SupplyChain/
│       ├── PO_*.pdf                     # Purchase Orders
│       ├── GRN_*.xlsx                   # Goods Receipt Notes
│       └── SDS_*.pdf                    # Safety Data Sheets (28 files)
│
└── DMS/
    ├── QA/
    │   ├── Deviation_*.pdf              # 8 deviation reports
    │   ├── CAPA_*.docx                  # CAPA investigations
    │   └── Change_Control_*.pdf
    ├── Regulatory/
    │   ├── Regulatory_Submission_*.pdf
    │   └── Audit_*.docx
    └── 13. List of all the SOPs/
        └── Version-2/                   # 62 SOPs indexed
            ├── SOP-PROD-001.pdf         # BMR
            ├── SOP-HSE-001.pdf          # PPE
            ├── SOP-PKG-001.pdf          # Packaging
            └── ... (59 more SOPs)
```

### **Document Index:**

The system uses `output/document_index.json` which contains:
- **Batch Data:** Manufacturing dates, expiry dates, pack sizes, tablet counts
- **Material Specs:** COA data for all raw materials
- **Deviation Data:** 8 detailed CAPA investigations with root cause analysis
- **QC Results:** Assay, dissolution, impurity test results

This index is built by `tools/document_index_builder.py` which systematically extracts data from all PDFs, DOCXs, and XLSXs in `APQR_Segregated`.

---

## 🧪 Testing

### **Test Questions (65 Comprehensive Cases)**

Located in `assets/test_questions.md`, covering:
- Single-domain queries (20 tests)
- Multi-domain queries (15 tests)
- APQR generation (5 tests)
- SOP semantic search (10 tests)
- Cross-verification queries (15 tests)

### **Run Test Cases:**

```bash
# Navigate to the system
cd agentic_apqr

# Start ADK web interface
adk web

# Test queries manually through web interface or use test_questions.md
```

### **Example Test Cases:**

**Q1. Single Domain - LIMS:**
```
What is the assay result for API from the COA?
Expected: LIMS QC Agent → Returns 99.9% from COA_Salicylic_Acid.pdf
```

**Q9. SDS Query - ERP:**
```
What are the safety hazards listed in the SDS for API?
Expected: ERP Supply Chain Agent → Returns hazard info from SDS_API.pdf
```

**Q45. Multi-Domain - Comprehensive:**
```
Summarize complete quality documentation for Disintegrant.
Expected: Sequential routing LIMS → ERP → DMS → Comprehensive report
```

---

## 🔨 Key Implementation Details

### **1. Sequential Workflow Logic**

**Orchestrator handles TWO types of inputs:**

**Type 1: Initial User Query**
```python
# User: "Complete documentation for Disintegrant"
# Orchestrator:
#   1. Detect: "complete" + "documentation" = ALL 3 domains
#   2. Route to FIRST domain: transfer_to_agent("lims_domain_agent", query)
#   3. STOP and wait for Compiler handoff
```

**Type 2: Compiler Handoff**
```python
# Compiler: "LIMS data received. Need ERP and DMS. Route to next domain."
# Orchestrator:
#   1. Review conversation history (LIMS done, ERP pending, DMS pending)
#   2. Route to NEXT domain: transfer_to_agent("erp_domain_agent", query)
#   3. STOP and wait for Compiler handoff (or final report if last domain)
```

### **2. Compiler Auto-Trigger Logic**

```python
# Compiler receives data from LIMS QC:
#   1. Show progress: "📊 ✅ LIMS QC ⏳ ERP ⏳ DMS"
#   2. Check: Are all required domains complete? No (ERP and DMS pending)
#   3. AUTO-TRANSFER: transfer_to_agent("orchestrator_agent", handoff_message)
#   4. Orchestrator wakes up and routes to ERP

# Compiler receives data from ERP Supply Chain:
#   1. Show progress: "📊 ✅ LIMS ✅ ERP ⏳ DMS"
#   2. Check: Are all required domains complete? No (DMS pending)
#   3. AUTO-TRANSFER: transfer_to_agent("orchestrator_agent", handoff_message)
#   4. Orchestrator wakes up and routes to DMS

# Compiler receives data from DMS QA:
#   1. Show progress: "📊 ✅ LIMS ✅ ERP ✅ DMS - All received!"
#   2. Check: Are all required domains complete? Yes!
#   3. Generate comprehensive final report (NO transfer to Orchestrator)
#   4. STOP - workflow complete
```

### **3. APQR Generation Workflow**

```python
# User: "Generate APQR for Aspirin 325"
# 1. Orchestrator routes to apqr_filler
# 2. APQR Filler calls generate_apqr_from_real_data()
# 3. Loads document_index.json
# 4. Populates 24 sections with real extracted data:
#    - Section 2: Batches (from BMR data)
#    - Section 5: API Parameters (from COA data)
#    - Section 11: Yields (calculated from BMR tablet counts)
#    - Section 17: Deviations (from 8 CAPA investigation reports)
#    - etc.
# 5. Generates Word document: APQR_DDMMYY_HHMM.docx
# 6. Renders HTML version: APQR_DDMMYY_HHMM.html
# 7. Returns: "✅ APQR generated successfully\n📄 http://localhost:8080/APQR_*.html"
```

---

## 🐛 Troubleshooting

### **Issue: SDS Not Found in DMS**

**Symptom:** "No Safety Data Sheet found within DMS Regulatory Affairs records"

**Cause:** ADK still running old code before SDS routing fix

**Solution:**
```bash
# Kill ADK process
ps aux | grep "adk web"
kill <process_id>

# Restart ADK to load new routing
adk web
```

### **Issue: Compiler Waiting Indefinitely**

**Symptom:** "📊 ✅ LIMS ⏳ ERP ⏳ DMS - Waiting..." with no progress

**Cause:** Orchestrator didn't route to ERP/DMS (old parallel routing logic)

**Solution:** Already fixed in latest code. Restart ADK to load sequential workflow.

### **Issue: APQR Agent Answering Data Queries**

**Symptom:** APQR Filler responds to "What is the assay result?" queries

**Cause:** Agent not properly redirecting non-APQR queries

**Solution:** Already fixed. APQR Filler now strictly rejects data queries and redirects to Orchestrator.

---

## 📚 Documentation

### **Comprehensive Guides:**

1. **MULTI_DOMAIN_QUERY_FIX.md**
   - Problem analysis (5 critical issues)
   - Sequential workflow implementation
   - Auto-handoff design

2. **SEMANTIC_SOP_SEARCH_GUIDE.md**
   - SOP index structure (62 SOPs)
   - Semantic matching algorithm
   - Keyword and alias extraction

3. **INTEGRATION_GUIDE_DATA_FILLER.md**
   - APQR Filler integration steps
   - Tool definitions
   - Example workflows

---

## 🤝 Contributing

### **Adding a New Sub-Agent:**

1. Create `agents/[domain]/new_subagent.py`
2. Define tools in `tools/tools.py`
3. Add to domain agent's routing logic
4. Update Orchestrator routing keywords
5. Add test cases to `assets/test_questions.md`

### **Adding a New Tool:**

1. Create tool function in `tools/tools.py` or specialized tool file
2. Document parameters and return format with type hints
3. Add to relevant agent's `tools=[]` list
4. Test with sample queries

---

## 📄 License

Proprietary - Short Hills Tech Pvt Ltd

---

## 👥 Authors

**APQR Development Team**  
Short Hills Tech Pvt Ltd

---

## 📊 Statistics

- **28 Files Changed** in latest commit
- **15,099 Insertions** (new features and documentation)
- **62 SOPs Indexed** with semantic metadata
- **28 SDS Documents** in ERP Supply Chain
- **8 Deviation Reports** with detailed CAPA data
- **4 Batches** of manufacturing data indexed
- **24 APQR Sections** auto-populated
- **65 Test Questions** covering all workflows

---

**Version:** 2.0.0 (Sequential Workflow with Auto-Handoffs)  
**Status:** Production Ready  
**Last Updated:** November 11, 2025  
**Commit:** 1c34cf7

**🚀 Key Achievement:** Zero user prompting required for multi-domain queries. System automatically completes comprehensive data retrieval with real-time progress updates!
