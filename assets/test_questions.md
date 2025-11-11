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
**Expected Domain:** ERP (Supply Chain Sub-Agent)  
**Expected Result:** Hazard statements, precautionary statements from SDS_API.pdf
**Note:** SDS files are stored with procurement documents in ERP/SupplyChain

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
**Expected Domains:** LIMS (COA) + ERP Supply Chain (SDS) **[PARALLEL]**  
**Expected Result:** Combined report with assay results from LIMS and hazards from ERP/SupplyChain

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
**Expected Domains:** LIMS (All COAs) + ERP Supply Chain (All SDS) **[PARALLEL]**  
**Expected Result:** Comprehensive table with API, Binder, Filler, Disintegrant with assay results and safety hazards

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
**Expected Domains:** ERP (PO + SDS) + LIMS (COA) **[PARALLEL]**  
**Expected Result:** ✅ PO available, ✅ COA available, ✅ SDS available (all from ERP/Supply Chain and LIMS)

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
- ERP: Purchase Order, Requisition Slip, SDS with safety hazards
- DMS: SOPs, training records, regulatory documents

---

## 👥 **Category 7: Training & Personnel Queries**

### Q21. GMP Training Records
```
What GMP training records are available in the system?
```
**Expected Domain:** DMS (Training Sub-Agent)  
**Expected Result:** List of GMP training documents, dates, personnel

### Q22. Analyst Qualification
```
Show me the analyst qualification records for QC personnel.
```
**Expected Domain:** DMS (Training Sub-Agent)  
**Expected Result:** Qualification certificates, training completion dates

### Q23. Training Effectiveness
```
Has the QC team completed training on the new HPLC method?
```
**Expected Domain:** DMS (Training Sub-Agent)  
**Expected Result:** Training attendance, completion status, effectiveness checks

### Q24. Personnel Certifications
```
List all personnel certifications that are currently valid.
```
**Expected Domain:** DMS (Management Sub-Agent)  
**Expected Result:** Certification types, expiry dates, personnel names

### Q25. Training Plan Query
```
What is the annual training plan for manufacturing personnel?
```
**Expected Domain:** DMS (Training Sub-Agent)  
**Expected Result:** ⚠️ Likely "No information found" unless training plans are in DMS

---

## 📋 **Category 8: SOP & Documentation Queries**

### Q26. SOP Version Control
```
What is the current version of the SOP for batch manufacturing?
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** SOP number, version, effective date, approval status

### Q27. SOP Change History
```
Show me the change history for the analytical testing SOP.
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** Revision history, change reasons, approval dates

### Q28. Document Control
```
List all SOPs that are pending review or approval.
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** SOP numbers, review dates, approval status

### Q29. Work Instructions
```
Are there work instructions available for equipment cleaning?
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** Work instruction documents, procedures, checklists

### Q30. Master Batch Record
```
Show me the master batch record for Aspirin 325mg tablets.
```
**Expected Domain:** ERP (Manufacturing Sub-Agent)  
**Expected Result:** MBR document, batch size, process steps, IPCs

---

## 🔧 **Category 9: Equipment & Maintenance Queries**

### Q31. Equipment Calibration Status
```
What is the calibration status of all HPLC instruments?
```
**Expected Domain:** ERP (Engineering Sub-Agent)  
**Expected Result:** Equipment IDs, last calibration dates, next due dates

### Q32. Preventive Maintenance Schedule
```
Show me the preventive maintenance schedule for tablet compression machines.
```
**Expected Domain:** ERP (Engineering Sub-Agent)  
**Expected Result:** PM schedule, frequency, last completion, next due

### Q33. Equipment Qualification
```
What equipment qualification documents are available for analytical instruments?
```
**Expected Domain:** LIMS (Validation Sub-Agent)  
**Expected Result:** IQ/OQ/PQ documents, qualification dates, status

### Q34. Equipment Breakdown Records
```
Were there any equipment breakdowns or failures in the last quarter?
```
**Expected Domain:** ERP (Engineering Sub-Agent)  
**Expected Result:** Breakdown logs, root cause, corrective actions

### Q35. Instrument Usage Logs
```
Show me the usage logs for the tablet hardness tester.
```
**Expected Domain:** ERP (Engineering Sub-Agent)  
**Expected Result:** Usage dates, operators, tests performed

---

## ⚠️ **Category 10: Deviation & CAPA Queries**

### Q36. Open Deviations
```
List all open deviations in the system.
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** Deviation IDs, dates, status, assigned investigators

### Q37. Deviation by Type
```
Show me all deviations classified as "Major" or "Critical".
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** Major/Critical deviations, impact assessment, CAPAs

### Q38. CAPA Effectiveness
```
What CAPAs have been implemented and verified for effectiveness?
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** CAPA IDs, corrective actions, verification dates, status

### Q39. Recurring Deviations
```
Are there any recurring deviations related to batch yield?
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** Deviation trend analysis, root causes, patterns

### Q40. Deviation Investigation
```
Show me the investigation report for deviation DEV-2025-001.
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** Investigation details, root cause, CAPA, closure

---

## 📊 **Category 11: Batch Record & Manufacturing Queries**

### Q41. Batch Yield Analysis
```
What are the batch yields for all Aspirin batches manufactured this year?
```
**Expected Domain:** ERP (Manufacturing Sub-Agent)  
**Expected Result:** Batch numbers, theoretical vs actual yields, yield %

### Q42. In-Process Controls
```
Show me the in-process control results for batch ASP-25-001.
```
**Expected Domain:** LIMS (QC Sub-Agent)  
**Expected Result:** IPC parameters, results, specifications, pass/fail

### Q43. Batch Genealogy
```
Provide the batch genealogy for finished product batch ASP-25-002.
```
**Expected Domain:** ERP (Manufacturing Sub-Agent) + LIMS (QC)  
**Expected Result:** Raw material batches, manufacturing dates, test results

### Q44. Manufacturing Exceptions
```
Were there any manufacturing exceptions or deviations during batch production?
```
**Expected Domain:** ERP (Manufacturing) + DMS (QA)  
**Expected Result:** Exception reports, deviations, impact assessments

### Q45. Batch Release Status
```
What is the release status of batch ASP-25-003?
```
**Expected Domain:** LIMS (QC Sub-Agent)  
**Expected Result:** Release date, QA approval, COA status

---

## 🧪 **Category 12: Raw Material & Supplier Queries**

### Q46. Raw Material Specifications
```
What are the specifications for the API raw material?
```
**Expected Domain:** LIMS (QC Sub-Agent)  
**Expected Result:** Specifications from COA, test parameters, acceptance criteria

### Q47. Supplier Audit Status
```
Show me the audit status of all approved suppliers.
```
**Expected Domain:** DMS (Regulatory Sub-Agent)  
**Expected Result:** Supplier names, last audit dates, audit findings

### Q48. Material Expiry Dates
```
Are there any raw materials approaching expiry?
```
**Expected Domain:** ERP (Supply Chain Sub-Agent)  
**Expected Result:** Material names, batch numbers, expiry dates

### Q49. Incoming Material Inspection
```
Show me the incoming inspection records for Binder material.
```
**Expected Domain:** ERP (Supply Chain) + LIMS (QC)  
**Expected Result:** Inspection results, receipt dates, acceptance status

### Q50. Alternative Suppliers
```
What alternative suppliers are approved for API sourcing?
```
**Expected Domain:** ERP (Supply Chain Sub-Agent)  
**Expected Result:** Approved supplier list, qualification status

---

## 🌡️ **Category 13: Environmental & Facility Queries**

### Q51. Cleanroom Monitoring
```
Show me the environmental monitoring data for the manufacturing cleanroom.
```
**Expected Domain:** LIMS (Validation Sub-Agent)  
**Expected Result:** Temperature, humidity, particle counts, compliance

### Q52. HVAC Qualification
```
What is the qualification status of the HVAC system?
```
**Expected Domain:** LIMS (Validation Sub-Agent)  
**Expected Result:** Qualification documents, last review, next due

### Q53. Water System Testing
```
Show me the latest water system testing results.
```
**Expected Domain:** LIMS (QC Sub-Agent)  
**Expected Result:** Water quality tests, microbial limits, chemical parameters

### Q54. Compressed Air Quality
```
What are the compressed air quality test results?
```
**Expected Domain:** LIMS (QC Sub-Agent)  
**Expected Result:** Oil content, dew point, particle count, microbial test

### Q55. Facility Cleaning Records
```
Show me the facility cleaning and sanitization records.
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** Cleaning schedules, completion records, verification

---

## 📑 **Category 14: Regulatory & Compliance Queries**

### Q56. Regulatory Submissions
```
What regulatory submissions have been filed for this product?
```
**Expected Domain:** DMS (Regulatory Sub-Agent)  
**Expected Result:** Submission types, dates, regulatory authorities, status

### Q57. Audit Findings
```
Show me the findings from the last GMP audit.
```
**Expected Domain:** DMS (Regulatory Sub-Agent)  
**Expected Result:** Audit observations, CAPA actions, closure status

### Q58. Regulatory Changes
```
Are there any recent regulatory changes impacting manufacturing?
```
**Expected Domain:** DMS (Regulatory Sub-Agent)  
**Expected Result:** Regulatory updates, impact assessment, implementation plan

### Q59. Product Complaints
```
List all product complaints received in the last 6 months.
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** Complaint IDs, customer details, investigation status

### Q60. Recall Readiness
```
Show me the recall procedure and mock recall results.
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** Recall SOP, mock recall reports, effectiveness

---

## 🔄 **Category 15: Change Control Queries**

### Q61. Open Change Controls
```
What change controls are currently open and pending approval?
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** Change control numbers, descriptions, approval status

### Q62. Change Impact Assessment
```
Show me the impact assessment for change control CC-2025-005.
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** Impact on product, process, validation, stability

### Q63. Change History
```
What changes were made to the manufacturing process in the last year?
```
**Expected Domain:** DMS (QA Sub-Agent)  
**Expected Result:** Change controls, implementation dates, effectiveness

### Q64. Equipment Changes
```
Were there any changes to analytical equipment or methods?
```
**Expected Domain:** LIMS (Validation) + DMS (QA)  
**Expected Result:** Equipment modifications, method updates, validation status

### Q65. Vendor Changes
```
Show me any changes to approved vendors or suppliers.
```
**Expected Domain:** ERP (Supply Chain Sub-Agent)  
**Expected Result:** Vendor changes, qualification status, approval dates

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

2. **Run Questions by Category:** 
   - **Quick Smoke Test:** Q1-Q5 (basic routing)
   - **Core Functionality:** Q1-Q20 (original test suite)
   - **Extended Testing:** Q21-Q65 (comprehensive domain coverage)
   - **Full Regression:** All 65 questions

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

### **Testing Priorities:**

- **P0 (Critical):** Q1-Q5, Q12-Q15, Q20 - Core routing and multi-domain queries
- **P1 (High):** Q6-Q11, Q16-Q19 - Single domain edge cases
- **P2 (Medium):** Q21-Q45 - Extended functionality (training, SOP, equipment)
- **P3 (Low):** Q46-Q65 - Comprehensive coverage (regulatory, change control)

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

✅ **Data-Rich Queries:** Q1-Q2, Q5-Q6, Q9, Q12-Q18, Q20-Q24, Q26-Q65  
   → **Provide comprehensive, detailed answers with source citations**  

⚠️ **"No Info" Queries:** Q3-Q4, Q7-Q8, Q10-Q11, Q19, Q25  
   → **Explicitly state "No information found in [domain]"**  

🚀 **ALL 65 Questions:**  
   → **Compiler responds automatically, no manual prompting needed**  

⚡ **Multi-Domain Queries:** Q12-Q15, Q18, Q20, Q43-Q44, Q49, Q64  
   → **Multiple domains execute in parallel (verify via timestamps)**

📊 **Domain Coverage Summary:**
- **LIMS Queries:** Q1-Q4, Q16, Q33, Q42, Q45-Q46, Q51-Q54
- **ERP Queries:** Q5-Q9, Q30-Q32, Q34-Q35, Q41, Q48, Q50, Q65
- **DMS Queries:** Q10-Q11, Q21-Q29, Q36-Q40, Q47, Q55-Q63
- **Multi-Domain:** Q12-Q15, Q18, Q20, Q43-Q44, Q49, Q64

**Note:** SDS queries (Q9, Q12, Q15, Q18, Q20) are routed to ERP Supply Chain where SDS files are stored with procurement documents.

