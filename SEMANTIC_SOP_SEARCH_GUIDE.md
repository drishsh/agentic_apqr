# 🔍 Semantic SOP Search System

## Overview

The APQR system now includes **semantic search** for SOPs - you can ask questions using common terms like "BMR", "PPE", or "HPLC" without knowing exact SOP numbers!

---

## ✅ How It Works

### **1. Enhanced SOP Index**

Every SOP is now indexed with:
- **Aliases**: BMR, PPE, HPLC, CAPA, etc.
- **Keywords**: Extracted from title, purpose, and content
- **Full Title**: Complete SOP title for context
- **Content Summary**: First 500 chars of purpose/scope

### **2. Semantic Matching**

When you ask a question, the system:
1. Extracts search terms from your query
2. Searches all SOPs for matching aliases, keywords, titles
3. Scores each match (aliases = high priority)
4. Returns the best match(es)

---

## 📋 Example Queries

### **Query by Common Name (Not SOP Number):**

✅ **"Show me the BMR procedure"**
   - Finds: **SOP-PROD-001 v2** - "Preparation and Review of Batch Manufacturing Records"
   - Matched by: `bmr` alias

✅ **"What are the PPE requirements?"**
   - Finds: **SOP-HSE-001 v2** - "Personal Protective Equipment (PPE) Requirements"
   - Matched by: `ppe` alias

✅ **"How do I operate the HPLC?"**
   - Finds: **SOP-QC-002** - HPLC operation procedures
   - Matched by: `hplc` alias

✅ **"Show me packaging procedures"**
   - Finds: **SOP-PKG-001**, **SOP-PKG-002**, **SOP-PKG-003**, **SOP-PKG-004**
   - Matched by: `packaging` keywords

✅ **"What's the tablet compression SOP?"**
   - Finds: **SOP-PROD-003** - "Operation of Tablet Compression Machine"
   - Matched by: `tablet` alias

✅ **"Show me calibration procedures"**
   - Finds: Multiple SOPs with calibration in title/keywords
   - Matched by: `calibration` keywords

---

## 🏆 Supported Aliases

The system recognizes these common terms:

| Alias | Expands To | Example SOP |
|-------|------------|-------------|
| **bmr** | Batch Manufacturing Record | SOP-PROD-001 |
| **ppe** | Personal Protective Equipment | SOP-HSE-001 |
| **hplc** | High Performance Liquid Chromatography | SOP-QC-002 |
| **capa** | Corrective/Preventive Action | SOP-QA-007 |
| **gmp** | Good Manufacturing Practice | Multiple |
| **deviation** | Non-conformance, Discrepancy | SOP-QA-005 |
| **calibration** | Equipment Qualification | SOP-ENG-001 |
| **cleaning** | Sanitization | SOP-PROD-004 |
| **sampling** | Sample Collection | SOP-QC-001 |
| **dissolution** | Drug Release Test | SOP-QC-003 |
| **tablet** | Compression Machine | SOP-PROD-003 |
| **packaging** | Packing, Labeling | SOP-PKG-001 |
| **warehouse** | Storage, Inventory | SOP-WH-001 |
| **dispensing** | Material Weighing | SOP-PROD-002 |
| **validation** | Qualification | SOP-ENG-005 |
| **change control** | Change Management | SOP-QA-004 |
| **training** | Personnel Training | SOP-QA-002 |
| **environmental monitoring** | Cleanroom, HVAC | SOP-ENG-004 |

---

## 🎯 Real-World Test Examples

### **Scenario 1: Quality Assurance Manager**
**Question:** "Show me the current version of the BMR SOP"

**System Response:**
```
📋 SOP Query Result - Semantic Search

Query: Show me the current version of the BMR SOP

Found: SOP-PROD-001 (2 version(s))
Matched by: bmr

📄 SOP-PROD-001 - Version 2 (CURRENT)
   - Title: Preparation and Review of Batch Manufacturing Records
   - Department: Production
   - Version: 2
   - Effective Date: 18-Mar-2025
   - Aliases: bmr, ppe, capa
   - File: SOP-PROD-001.pdf

📄 SOP-PROD-001 - Version 1 (SUPERSEDED)
   - Title: Gowning and Hygiene in Manufacturing Areas
   - Department: Production
   - Version: 1
   - File: SOP-PROD-001.pdf

✅ Current Version: 2
```

### **Scenario 2: HSE Officer**
**Question:** "What are the PPE requirements?"

**System Response:**
```
📋 SOP Query Result - Semantic Search

Query: What are the PPE requirements?

Found: SOP-HSE-001
Matched by: ppe

📄 SOP-HSE-001 - Version 2
   - Title: Personal Protective Equipment (PPE) Requirements
   - Department: HSE
   - Version: 2
   - Effective Date: 22-Mar-2025
   - Aliases: ppe, capa, sop
   - Purpose: This SOP defines the requirements for selection, use, 
              maintenance, and disposal of personal protective equipment...
```

### **Scenario 3: QC Analyst**
**Question:** "Show me all HPLC-related SOPs"

**System Response:**
```
📋 SOP Query Results - Semantic Search

Query: Show me all HPLC-related SOPs

Found 3 matching SOP(s):

📄 SOP-QC-002 (v1)
   - High Performance Liquid Chromatography (HPLC) Operation
   - Department: Quality Control
   - Matches: hplc

📄 SOP-QC-006 (v1)
   - HPLC Method Validation and Transfer
   - Department: Quality Control
   - Matches: hplc

📄 SOP-ENG-002 (v1)
   - HPLC Calibration and Maintenance
   - Department: Engineering
   - Matches: hplc, calibration
```

---

## 🔄 Rebuilding the Index

If new SOPs are added or updated, rebuild the index:

```bash
cd /path/to/agentic_apqr/tools
python3 sop_index_builder.py
```

This will:
- Scan all SOP directories
- Extract metadata, aliases, keywords
- Save updated `output/sop_index.json`

---

## 📊 Index Statistics

**Current Index:**
- **Total SOPs:** 62 documents
- **Departments:** 8 (Production, QC, QA, Packaging, Engineering, Warehouse, HSE, Regulatory)
- **Versions Tracked:** Version 1 and Version 2 for 6 key SOPs
- **Aliases Mapped:** 19 common terms
- **Keywords Extracted:** ~500 unique terms

---

## 🚀 Integration with Agents

### **Orchestrator Routing:**
Keywords that trigger SOP routing:
- "sop", "procedure", "bmr", "ppe", "hplc"
- "batch", "safety", "equipment", "manufacturing"
- "packaging", "warehouse", "calibration", "cleaning"

### **DMS QA Agent:**
Receives SOP queries and:
1. Loads `output/sop_index.json`
2. Performs semantic matching
3. Returns detailed SOP information

### **Compiler Agent:**
Receives results and formats for user display

---

## 💡 Tips for Users

1. **Use common terms:** "BMR" instead of "SOP-PROD-001"
2. **Be specific:** "packaging procedures" vs "show me all SOPs"
3. **Version awareness:** System automatically shows latest version
4. **Multiple matches:** If multiple SOPs match, system shows list
5. **Direct links:** File paths are provided for easy document access

---

## 🎉 Benefits

✅ **No memorization:** Don't need to remember SOP numbers  
✅ **Natural language:** Ask in plain English  
✅ **Version tracking:** Always get the current version  
✅ **Comprehensive:** Searches titles, aliases, keywords, content  
✅ **Fast:** Pre-indexed for instant results  

---

## 📝 Example Test Session

```
User: "Show me the BMR procedure"
→ System finds SOP-PROD-001 v2 (Batch Manufacturing Records)

User: "What about PPE requirements?"
→ System finds SOP-HSE-001 v2 (Personal Protective Equipment)

User: "How do I calibrate the HPLC?"
→ System finds SOP-ENG-002 (HPLC Calibration)

User: "Show me all packaging SOPs"
→ System lists SOP-PKG-001, SOP-PKG-002, SOP-PKG-003, SOP-PKG-004

User: "What's the version of SOP-PROD-001?"
→ System shows Version 2 (current) and Version 1 (superseded)
```

---

## ✨ Future Enhancements

Potential improvements:
- [ ] Full-text search within SOP content
- [ ] Search by effective date range
- [ ] Filter by department
- [ ] Suggest related SOPs
- [ ] Track SOP usage frequency
- [ ] Auto-notify on version updates

---

**Last Updated:** 2025-11-11  
**Index Version:** 2.0  
**Total SOPs:** 62  

