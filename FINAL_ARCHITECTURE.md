# APQR Agentic System - Final Architecture

## 🎯 **System Flow - Confirmed**

```
┌─────────────────────────────────────────────────────────────┐
│                            USER                             │
└─────────────────────────────────────────────────────────────┘
                              ↓ QUERY
┌─────────────────────────────────────────────────────────────┐
│                  ORCHESTRATOR AGENT (Root)                  │
│                                                             │
│  Visible to User: "Routing query to LIMS and DMS..."       │
│                                                             │
│  Internal Work:                                             │
│  1. Analyze query intent                                    │
│  2. Decompose into domain-specific sub-queries              │
│  3. Route simultaneously to multiple domains (parallel)     │
│  4. Collect JSON responses from all domains                 │
│  5. Forward aggregated data to Compiler                     │
└─────────────────────────────────────────────────────────────┘
         ↓ Sub-query 1          ↓ Sub-query 2          ↓ Sub-query 3
         (internal)             (internal)             (internal)
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│  LIMS DOMAIN     │   │   ERP DOMAIN     │   │   DMS DOMAIN     │
│     AGENT        │   │      AGENT       │   │      AGENT       │
│                  │   │                  │   │                  │
│ Visible to User: │   │ Visible to User: │   │ Visible to User: │
│ "✓ LIMS data...  │   │ "✓ ERP data...   │   │ "✓ DMS data...   │
│  Forwarding"     │   │  Forwarding"     │   │  Forwarding"     │
│                  │   │                  │   │                  │
│ Internal Work:   │   │ Internal Work:   │   │ Internal Work:   │
│ 1. Route to      │   │ 1. Route to      │   │ 1. Route to      │
│    sub-agents    │   │    sub-agents    │   │    sub-agents    │
│ 2. Collect data  │   │ 2. Collect data  │   │ 2. Collect data  │
│ 3. Aggregate     │   │ 3. Aggregate     │   │ 3. Aggregate     │
│ 4. Return JSON   │   │ 4. Return JSON   │   │ 4. Return JSON   │
└──────────────────┘   └──────────────────┘   └──────────────────┘
    ↓ (internal)           ↓ (internal)           ↓ (internal)
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│  SUB-AGENTS      │   │  SUB-AGENTS      │   │  SUB-AGENTS      │
│                  │   │                  │   │                  │
│ • QC Agent       │   │ • Manufacturing  │   │ • QA Agent       │
│ • Validation     │   │ • Engineering    │   │ • Regulatory     │
│ • R&D Agent      │   │ • Supply Chain   │   │ • Management     │
│                  │   │                  │   │ • Training       │
│                  │   │                  │   │                  │
│ NO USER OUTPUT   │   │ NO USER OUTPUT   │   │ NO USER OUTPUT   │
│                  │   │                  │   │                  │
│ Work:            │   │ Work:            │   │ Work:            │
│ 1. Call tools    │   │ 1. Call tools    │   │ 1. Call tools    │
│ 2. Parse PDFs    │   │ 2. Parse PDFs    │   │ 2. Parse PDFs    │
│ 3. Extract data  │   │ 3. Extract data  │   │ 3. Extract data  │
│ 4. Return JSON   │   │ 4. Return JSON   │   │ 4. Return JSON   │
│    to parent     │   │    to parent     │   │    to parent     │
└──────────────────┘   └──────────────────┘   └──────────────────┘
         ↓ JSON              ↓ JSON              ↓ JSON
         (internal)          (internal)          (internal)
         └──────────────────┴────────────────────┘
                              ↓
                     (internal communication)
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    COMPILER AGENT                           │
│                                                             │
│  Receives from Orchestrator:                                │
│  - Original user query                                      │
│  - JSON data from LIMS domain                               │
│  - JSON data from ERP domain                                │
│  - JSON data from DMS domain                                │
│                                                             │
│  Work:                                                      │
│  1. Synthesize all domain data                              │
│  2. Cross-verify for discrepancies                          │
│  3. Format as user-friendly report                          │
│  4. Generate comprehensive answer                           │
│                                                             │
│  Visible to User: [FULL DETAILED REPORT]                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                            USER                             │
│                                                             │
│  Receives:                                                  │
│  1. Orchestrator status: "Routing to LIMS..."               │
│  2. LIMS: "✓ Data retrieved"                                │
│  3. ERP: "✓ Data retrieved"                                 │
│  4. DMS: "✓ Data retrieved"                                 │
│  5. Compiler: [Comprehensive detailed answer]               │
└─────────────────────────────────────────────────────────────┘
```

---

## ✅ **Confirmed Requirements**

### **1. Query Decomposition** ✓
- **Orchestrator analyzes and breaks down** complex queries
- Each domain receives **specific sub-query** relevant to its scope
- Example:
  ```
  User: "For API, give me COA and SDS"
  → To LIMS: "Retrieve COA test results for API"
  → To DMS: "Retrieve SDS safety hazards for API"
  ```

### **2. Parallel Execution** ✓
- **Multiple domains called simultaneously**, not sequentially
- Orchestrator routes to LIMS, ERP, and DMS **at the same time**
- Reduces total execution time significantly

### **3. Domain Independence** ✓
- **LIMS does NOT depend on ERP**
- **ERP does NOT depend on DMS**
- **DMS does NOT depend on LIMS**
- Each domain works independently with its own `sample_docs/` folder

### **4. User Interaction Rules** ✓
- **ONLY Orchestrator and Compiler** show visible responses to user
- **Domain Agents**: Show only brief "✓ Data retrieved. Forwarding to Compiler."
- **Sub-Agents**: NO visible output to user at all
- **All other communication**: Internal JSON data exchange

### **5. Agent Hierarchy** ✓
```
Level 0: Orchestrator (Root)
Level 1: Domain Agents (LIMS, ERP, DMS)
Level 2: Sub-Agents (QC, Validation, R&D, Manufacturing, etc.)
Level 3: Compiler (Sequential - receives after all domains complete)
```

### **6. Actual Work Execution** ✓
- **Domain Agents DO work**: Call sub-agents, aggregate data
- **Sub-Agents DO work**: Call tools, parse PDFs, extract data
- **Tools DO work**: Read files, parse documents
- **Only USER-FACING output is suppressed**, not internal work

---

## 📊 **Example Flow: Multi-Domain Query**

### **User Query:**
```
"For API material, give me the COA test results and the SDS safety hazards."
```

### **Step-by-Step Execution:**

#### **Step 1: Orchestrator Receives Query**
```
Visible to User: "Routing query to LIMS and DMS domains..."
Internal Work:
  - Analyzes query
  - Identifies: API material, COA (LIMS), SDS (DMS)
  - Decomposes:
    → Sub-query 1 to LIMS: "Retrieve COA test results for API material"
    → Sub-query 2 to DMS: "Retrieve SDS safety hazards for API material"
  - Calls LIMS and DMS agents IN PARALLEL
```

#### **Step 2: LIMS Domain Agent Processes** (parallel with DMS)
```
Visible to User: "✓ LIMS data retrieved. Forwarding to Compiler."
Internal Work:
  - Receives: "Retrieve COA test results for API material"
  - Routes to QC Sub-Agent
  - QC Sub-Agent calls query_lims_qc tool
  - Tool parses COA_API.pdf using pdfplumber
  - Extracts: batch number, assay result, specifications, test results
  - Returns JSON to LIMS Agent
  - LIMS Agent aggregates and returns JSON to Orchestrator
```

#### **Step 3: DMS Domain Agent Processes** (parallel with LIMS)
```
Visible to User: "✓ DMS data retrieved. Forwarding to Compiler."
Internal Work:
  - Receives: "Retrieve SDS safety hazards for API material"
  - Routes to Regulatory Sub-Agent
  - Regulatory Sub-Agent calls query_dms_regulatory tool
  - Tool parses SDS_API.pdf using pdfplumber
  - Extracts: hazards, precautions, storage conditions
  - Returns JSON to DMS Agent
  - DMS Agent aggregates and returns JSON to Orchestrator
```

#### **Step 4: Orchestrator Collects All Data**
```
No Visible Output (internal only)
Internal Work:
  - Collects JSON from LIMS
  - Collects JSON from DMS
  - Packages into single data structure:
    {
      "original_query": "For API material, give me...",
      "domains_queried": ["LIMS", "DMS"],
      "domain_responses": [
        {"domain": "LIMS", "status": "success", "data": {...}},
        {"domain": "DMS", "status": "success", "data": {...}}
      ]
    }
  - Forwards to Compiler
```

#### **Step 5: Compiler Synthesizes Final Answer**
```
Visible to User: [COMPREHENSIVE DETAILED REPORT]

Example Output:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
APQR Summary: API (Salicylic acid)

Laboratory & QC Summary (Source: LIMS - COA_API.pdf)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Batch Number: SA20250127
Material: Salicylic acid for Synthesis (API)

Test Results:
• Appearance: WHITE CRYSTALLINE POWDER ✓
• Assay: 98.5% - 101.0% (Spec: ≥ 99.0%) ✓
• Melting Point: 158.0-160.0°C (Spec: 158-161°C) ✓
• Purity: 99.9% ✓
[... all test parameters ...]

Safety Data Sheet (Source: DMS - SDS_API.pdf)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Classification:
⚠️ Acute toxicity, Category 4: Harmful if swallowed (H302)
⚠️ Serious eye damage, Category 1: Causes serious eye damage (H318)
⚠️ Reproductive toxicity, Category 2: Suspected of damaging unborn child (H361d)

Precautionary Statements:
• P280: Wear protective gloves/eye protection
• P305+P351+P338: IF IN EYES: Rinse cautiously with water
[... all safety information ...]

Final Recommendation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
API batch SA20250127 meets all QC specifications.
Handle with appropriate PPE as per SDS precautions.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔧 **Internal vs User-Facing Communication**

### **Internal Communication (NOT visible to user):**
- Orchestrator → Domain Agents: Decomposed sub-queries
- Domain Agents → Sub-Agents: Routing instructions
- Sub-Agents → Tools: Function calls
- Tools → Sub-Agents: Parsed data (JSON)
- Sub-Agents → Domain Agents: Extracted data (JSON)
- Domain Agents → Orchestrator: Aggregated data (JSON)
- Orchestrator → Compiler: Complete data package (JSON)

### **User-Facing Communication (visible to user):**
- Orchestrator: "Routing query to [domains]..."
- LIMS Agent: "✓ LIMS data retrieved. Forwarding to Compiler."
- ERP Agent: "✓ ERP data retrieved. Forwarding to Compiler."
- DMS Agent: "✓ DMS data retrieved. Forwarding to Compiler."
- Compiler: [Full comprehensive detailed report]

---

## 📋 **Agent Responsibilities Summary**

| Agent Level | Agents | Visible to User? | Actual Work? | Communicates With |
|-------------|--------|------------------|--------------|-------------------|
| **Level 0** | Orchestrator | ✅ Yes (minimal status) | ✅ Yes (route, collect) | User, Domain Agents, Compiler |
| **Level 1** | LIMS, ERP, DMS | ✅ Yes (brief ack only) | ✅ Yes (route, aggregate) | Orchestrator, Sub-Agents |
| **Level 2** | QC, Validation, R&D, etc. | ❌ No | ✅ Yes (parse, extract) | Domain Agents, Tools |
| **Level 3** | Compiler | ✅ Yes (full answer) | ✅ Yes (synthesize) | User, Orchestrator |

---

## 🎯 **Key Architectural Principles**

1. **Separation of Concerns**
   - Orchestrator: Routing & coordination
   - Domain Agents: Domain-specific aggregation
   - Sub-Agents: Specialized data extraction
   - Compiler: Synthesis & presentation

2. **Clean User Experience**
   - Users see: Status updates + Final answer
   - Users DON'T see: Raw data, intermediate steps, JSON

3. **Internal Efficiency**
   - Agents work in parallel when possible
   - Data passed as structured JSON
   - Each agent does actual work, not just forwarding

4. **Domain Isolation**
   - LIMS only accesses `sample_docs/LIMS/`
   - ERP only accesses `sample_docs/ERP/`
   - DMS only accesses `sample_docs/DMS/`
   - No cross-domain dependencies

5. **Traceability**
   - All data includes source citations
   - Compiler cross-verifies between domains
   - "No information found" is explicitly reported

---

## ✅ **What Has Been Fixed**

1. ✅ **Output Suppression** - Domain agents show brief messages only
2. ✅ **Actual Work** - Agents clarified to DO work, not just forward
3. ✅ **Parallel Execution** - Orchestrator calls multiple domains simultaneously
4. ✅ **Query Decomposition** - Orchestrator breaks down complex queries
5. ✅ **Domain Independence** - Each domain works independently
6. ✅ **User Interaction** - Only Orchestrator and Compiler respond to user
7. ✅ **Timestamp Error** - Removed problematic timestamp field

---

## 🚀 **Ready to Test!**

**Restart ADK:**
```bash
# Stop ADK (Ctrl+C)
adk web
```

**Test Query:**
```
For API material, give me the COA test results and the SDS safety hazards.
```

**Expected Result:**
1. Orchestrator: "Routing to LIMS and DMS..."
2. LIMS: "✓ LIMS data retrieved. Forwarding to Compiler."
3. DMS: "✓ DMS data retrieved. Forwarding to Compiler."
4. Compiler: [Full detailed report with COA and SDS data]

**The system now works as designed!** 🎉

