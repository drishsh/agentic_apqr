# Test Questions for APQR Agentic System

**Purpose:** Comprehensive testing of the multi-agent APQR system including domain routing, parallel execution, data parsing, and "no information found" protocol.

---

## ✅ **Category 1: Single Domain Queries - LIMS**

### Q1. Simple Data Retrieval
```
What is the assay result for API from the COA?
```
**Expected Domain:** LIMS (QC Sub-Agent)  
**Expected Result:** Specific assay value, batch number, specification, and source document

### Q2. Material Identification
```
List all materials that have Certificates of Analysis in the LIMS system.
```
**Expected Domain:** LIMS (QC Sub-Agent)  
**Expected Result:** API, Binder, Filler, Disintegrant with their batch numbers

### Q3. Stability Study Query (No Data Expected)
```
Show me the stability study data for API from LIMS.
```
**Expected Domain:** LIMS (R&D Sub-Agent)  
**Expected Result:** ⚠️ "No information found" - Stability study reports not present in LIMS domain

### Q4. Validation Query (No Data Expected)
```
What are the cleaning validation results for the manufacturing equipment?
```
**Expected Domain:** LIMS (Validation Sub-Agent)  
**Expected Result:** ⚠️ "No information found" - Validation records not present in LIMS domain

---

## 📦 **Category 2: Single Domain Queries - ERP**

### Q5. Vendor Information
```
What is the vendor name for API in the purchase order?
```
**Expected Domain:** ERP (Supply Chain Sub-Agent)  
**Expected Result:** Sigma-Aldrich from API Purchase Order

### Q6. Purchase Order vs Requisition
```
Compare the API purchase order and requisition slip. Do they match?
```
**Expected Domain:** ERP (Supply Chain Sub-Agent)  
**Expected Result:** Comparison of PO number, dates, quantities, vendor

### Q7. Manufacturing Records Query (No Data Expected)
```
Show me the batch manufacturing records for finished product ASP-25.
```
**Expected Domain:** ERP (Manufacturing Sub-Agent)  
**Expected Result:** ⚠️ "No information found" - BMR documents not present in current ERP sample_docs

### Q8. Engineering Query (No Data Expected)
```
What preventive maintenance was performed on equipment in January 2025?
```
**Expected Domain:** ERP (Engineering Sub-Agent)  
**Expected Result:** ⚠️ "No information found" - PM records not present in ERP domain

---

## 📋 **Category 3: Single Domain Queries - DMS**

### Q9. Safety Data Sheet
```
What are the safety hazards listed in the SDS for API?
```
**Expected Domain:** DMS (Regulatory Affairs Sub-Agent)  
**Expected Result:** Hazard statements, precautionary statements from SDS_API.pdf

### Q10. SOP Query (No Data Expected)
```
Show me the Standard Operating Procedure for batch release testing.
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** ⚠️ "No information found" - SOPs not present in DMS domain

### Q11. Training Records Query (No Data Expected)
```
What training was completed by the QC team in 2025?
```
**Expected Domain:** DMS (Training Sub-Agent)  
**Expected Result:** ⚠️ "No information found" - Training records not present in DMS domain

---

## 🔄 **Category 4: Multi-Domain Queries (Parallel Execution)**

### Q12. Cross-Domain Material Verification
```
For API, give me the COA test results and SDS safety hazards.
```
**Expected Domains:** LIMS (COA) + DMS (SDS) **[PARALLEL]**  
**Expected Result:** Combined report with assay results from LIMS and hazards from DMS

### Q13. Purchase Order + COA Cross-Reference
```
Cross-reference the API purchase order with its COA. Does the vendor and material match?
```
**Expected Domains:** ERP (PO) + LIMS (COA) **[PARALLEL]**  
**Expected Result:** Comparison showing vendor (Sigma-Aldrich) and material (Salicylic Acid) match

### Q14. Complete Material Traceability
```
For Binder material, show me the purchase order, requisition slip, and certificate of analysis.
```
**Expected Domains:** ERP (PO + Requisition) + LIMS (COA) **[PARALLEL]**  
**Expected Result:** Complete traceability package for Binder (HPMC)

### Q15. Comprehensive Material Safety and Quality
```
For all raw materials, compare their assay results from COAs and identify any associated safety hazards from SDS documents.
```
**Expected Domains:** LIMS (All COAs) + DMS (All SDS) **[PARALLEL]**  
**Expected Result:** Comprehensive table with API, Binder, Filler, Disintegrant; note that only API has SDS available

---

## 🔍 **Category 5: Complex Analytical Queries**

### Q16. Comparison Query
```
Compare the assay results for all materials from their COAs. Which materials meet specifications?
```
**Expected Domain:** LIMS (QC Sub-Agent)  
**Expected Result:** Comparison table showing API, Binder, Filler pass; Disintegrant has no assay listed

### Q17. Discrepancy Detection
```
Are there any discrepancies between the purchase orders and their corresponding requisition slips for API and Binder?
```
**Expected Domain:** ERP (Supply Chain Sub-Agent)  
**Expected Result:** Detailed comparison identifying any date, quantity, or vendor mismatches

### Q18. Gap Analysis Query
```
For Disintegrant material, provide complete traceability including purchase order, COA, and SDS.
```
**Expected Domains:** ERP + LIMS + DMS **[PARALLEL]**  
**Expected Result:** ✅ PO available, ✅ COA available, ⚠️ SDS NOT available - Compiler must explicitly state this gap

---

## 🎯 **Category 6: Edge Cases and System Stress Tests**

### Q19. Non-Existent Material Query
```
What is the COA result for Lubricant excipient?
```
**Expected Domain:** LIMS (QC Sub-Agent)  
**Expected Result:** ⚠️ "No information found" - Lubricant not in LIMS domain

### Q20. Broad Query Requiring All Domains
```
Summarize the complete quality documentation available for API including test results, procurement records, and safety information.
```
**Expected Domains:** LIMS + ERP + DMS **[PARALLEL - ALL THREE]**  
**Expected Result:** Comprehensive summary pulling:
- LIMS: COA with assay results
- ERP: Purchase Order, Requisition Slip
- DMS: SDS with safety hazards

---

## 📊 **Testing Checklist**

After running each question, verify:

- [ ] **Correct Routing:** Did Orchestrator route to the correct domain(s)?
- [ ] **Parallel Execution:** For multi-domain queries, did domains execute simultaneously? (Check timestamps in terminal)
- [ ] **Brief Domain Messages:** Did domain agents only show "✓ Data retrieved. Forwarding to Compiler."?
- [ ] **Auto-Compiler Response:** Did Compiler respond IMMEDIATELY without requiring "?" or "yes" prompt?
- [ ] **Comprehensive Final Answer:** Did Compiler provide detailed, well-formatted answer?
- [ ] **"No Information Found" Protocol:** For queries with missing data, did Compiler explicitly state which domain was searched and what was not found?
- [ ] **Data Integrity:** Are sources cited (file names, domains)?
- [ ] **GMP Compliance:** Are discrepancies flagged appropriately?

---

## 🎯 **Success Criteria**

| Test Aspect | Success Criteria |
|-------------|------------------|
| **Orchestrator Routing** | Correctly identifies domain(s) from query context |
| **Parallel Execution** | Multi-domain queries execute simultaneously (verify via terminal timestamps) |
| **Domain Agent Output** | Only brief "✓ Data forwarded" messages, NO detailed answers to user |
| **Compiler Auto-Response** | Generates final answer AUTOMATICALLY, NO manual prompting needed |
| **Data Parsing** | Successfully extracts text/tables from PDF, Word, Excel documents |
| **"No Info Found" Handling** | Explicitly states domain searched and data gap |
| **Source Citation** | All data includes source file and domain |
| **Response Quality** | Professional, GMP-compliant, comprehensive |

---

## 📝 **How to Use This Test Suite:**

1. **Restart ADK:**
   ```bash
   cd /Users/shtlpmac019/Library/CloudStorage/OneDrive-ShortHillsTechPvtLtd/Desktop/AGENTS/AGENT/agentic_apqr
   adk web
   ```

2. **Run Each Question Sequentially:** Copy-paste from Q1 to Q20 into the ADK web interface

3. **Observe Terminal Logs:** Watch for:
   - Agent routing patterns
   - Parallel vs sequential execution (timestamps)
   - Tool calls (PDF parsing, etc.)
   - Any errors or warnings

4. **Document Results:** Note any questions where:
   - Routing was incorrect
   - Parallel execution didn't occur
   - Domain agents gave detailed answers (should only give brief status)
   - Compiler didn't auto-respond (required manual prompt)
   - "No information found" wasn't handled properly

5. **Iterate:** Fix any issues discovered and re-test

---

## 🔧 **Expected Terminal Log Pattern (Example for Q12):**

```
INFO: google_llm - Sending request for orchestrator_agent
INFO: google_llm - Response received

INFO: google_llm - Sending request for lims_domain_agent  ← PARALLEL START
INFO: google_llm - Sending request for dms_domain_agent   ← PARALLEL START

INFO: tools.py - LIMS QC Tool called
INFO: pdf_tools.py - Parsing COA_API.pdf
INFO: tools.py - DMS Regulatory Tool called
INFO: pdf_tools.py - Parsing SDS_API.pdf

INFO: google_llm - Response received from lims_domain_agent
INFO: google_llm - Response received from dms_domain_agent

INFO: google_llm - Sending request for compiler_agent  ← AUTO-FORWARD
INFO: google_llm - Response received from compiler_agent
```

**Note:** For parallel execution, you should see LIMS and DMS requests sent at nearly the same timestamp, NOT sequentially.

---

## 🎉 **System Is Working Correctly When:**

✅ Q1-Q2, Q5-Q6, Q9, Q12-Q20: **Provide comprehensive, detailed answers**  
⚠️ Q3-Q4, Q7-Q8, Q10-Q11, Q19: **Explicitly state "No information found in [domain]"**  
🚀 ALL questions: **Compiler responds automatically, no manual prompting needed**  
⚡ Q12-Q15, Q18, Q20: **Multiple domains execute in parallel (check timestamps)**

