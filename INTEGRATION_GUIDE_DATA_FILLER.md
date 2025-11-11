# APQR Data Filler Agent - Integration Guide

## Overview

This guide explains how the APQR Data Filler Agent integrates with your existing agentic APQR system.

---

## Architecture Integration

### System Architecture (Updated)

```
                        ┌─────────────────────┐
                        │                     │
                        │  Orchestrator Agent │
                        │   (Entry Point)     │
                        │                     │
                        └──────────┬──────────┘
                                   │
                ┌──────────────────┼──────────────────┬───────────────────┐
                │                  │                  │                   │
                ▼                  ▼                  ▼                   ▼
        ┌──────────────┐   ┌──────────────┐  ┌──────────────┐  ┌────────────────┐
        │              │   │              │  │              │  │                │
        │  LIMS Agent  │   │  ERP Agent   │  │  DMS Agent   │  │ Data Filler    │ ◄── NEW
        │              │   │              │  │              │  │ Agent          │
        │              │   │              │  │              │  │                │
        └──────┬───────┘   └──────┬───────┘  └──────┬───────┘  └────────┬───────┘
               │                  │                  │                   │
      ┌────────┼────────┐  ┌──────┼──────┐   ┌──────┼──────┐           │
      ▼        ▼        ▼  ▼      ▼      ▼   ▼      ▼      ▼           │
    ┌───┐   ┌───┐   ┌───┐┌───┐ ┌───┐ ┌───┐┌───┐ ┌───┐ ┌───┐           │
    │QC │   │Val│   │R&D││Mfg│ │Eng│ │SC ││QA │ │Reg│ │Mgmt│           │
    └─┬─┘   └─┬─┘   └─┬─┘└─┬─┘ └─┬─┘ └─┬─┘└─┬─┘ └─┬─┘ └─┬─┘           │
      │       │       │    │     │     │    │     │     │               │
      └───────┴───────┴────┴─────┴─────┴────┴─────┴─────┴───────────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │                     │
                        │  Compiler Agent     │
                        │  (Final Output)     │
                        │                     │
                        └─────────────────────┘
                                   │
                                   ▼
                              [End User]
```

### Key Integration Points

1. **Orchestrator → Data Filler Agent**
   - Direct routing for APQR generation requests
   - Keywords: "fill APQR", "generate APQR", "populate APQR"

2. **Data Filler Agent → Domain Agents**
   - Queries ERP, LIMS, DMS agents in parallel
   - Aggregates data from all domains

3. **Data Filler Agent → Compiler Agent**
   - Sends complete draft package
   - Includes completion report and CSV files

---

## Files Added/Modified

### New Files Created

1. **Agent File**
   ```
   agents/apqr_data_filler_agent.py
   ```
   - Main agent definition
   - Instructions and behavior
   - Tool assignments

2. **Tools File**
   ```
   tools/apqr_filler_tools.py
   ```
   - `get_available_batches()` - Batch scanning
   - `extract_section_data()` - Data extraction coordination
   - `fill_apqr_template()` - Template population
   - `mark_missing_data()` - Missing data notation
   - `generate_trend_csv()` - CSV generation
   - `create_completion_report()` - Completion tracking
   - `generate_partial_doc()` - Document generation
   - `export_apqr_draft()` - Export functionality

3. **Documentation**
   ```
   agents/APQR_DATA_FILLER_AGENT_README.md
   ```
   - Comprehensive agent documentation
   - Usage examples
   - Integration details

4. **Examples**
   ```
   examples/apqr_data_filler_example.py
   ```
   - 7 complete usage examples
   - End-to-end workflow demonstration

5. **Integration Guide**
   ```
   INTEGRATION_GUIDE_DATA_FILLER.md
   ```
   - This file

### Modified Files

1. **tools/__init__.py**
   - Added imports for APQR filler tools
   - Updated `__all__` exports

2. **agents/orchestrator_agent.py**
   - Added import for Data Filler Agent
   - Added to sub_agents list
   - Updated instructions with routing keywords
   - Added special routing section for APQR generation

---

## How It Works

### Workflow: User Query to APQR Draft

**Step 1: User Query**
```
User: "Fill APQR for Aspirin batches ASP-25-001 through ASP-25-004"
```

**Step 2: Orchestrator Routing**
```python
# Orchestrator detects keywords: "fill APQR"
# Routes to Data Filler Agent
transfer_to_agent("apqr_data_filler_agent", query_context)
```

**Step 3: Data Filler Agent Execution**
```python
# 3.1: Identify batches
batch_info = get_available_batches("Aspirin")
# → Found: ASP-25-001, ASP-25-002, ASP-25-003, ASP-25-004

# 3.2: Query domain agents (PARALLEL)
manufacturing_data = extract_section_data(
    "Batch Manufacturing Records", "ERP",
    "Retrieve BMR for batches", query_erp_manufacturing
)

qc_data = extract_section_data(
    "QC Test Results", "LIMS",
    "Retrieve COA for batches", query_lims_qc
)

deviation_data = extract_section_data(
    "Deviations & CAPA", "DMS",
    "Retrieve deviations", query_dms_qa
)

# 3.3: Aggregate all section data
all_section_data = {
    "Manufacturing": manufacturing_data,
    "QC Results": qc_data,
    "Deviations": deviation_data,
    ...
}

# 3.4: Generate trend CSVs
generate_trend_csv("yield", yield_data, "yield_trend.csv")
generate_trend_csv("assay", assay_data, "assay_trend.csv")

# 3.5: Create completion report
completion_report = create_completion_report(sections_status)
# → 85.3% complete

# 3.6: Generate partial document
draft_result = generate_partial_doc(
    template_path, all_section_data, "Aspirin", batches
)
# → APQR_Draft_Aspirin_Partial_20241110.docx

# 3.7: Transfer to Compiler
transfer_to_agent("compiler_agent", {
    "draft_path": draft_result["output_path"],
    "completion_report": completion_report,
    "csv_files": ["yield_trend.csv", "assay_trend.csv"],
    "batches": batches
})
```

**Step 4: User Response**
```
Data Filler Agent: ✓ APQR data extraction complete. 85% sections filled. 
                    Draft generated. Forwarding to Compiler for final review.
```

**Step 5: Compiler Agent**
```
Compiler Agent: [Receives draft package]
                [Performs final formatting]
                [Generates comprehensive user report]
                [Presents final APQR to user]
```

---

## Configuration

### Required Environment

No additional environment variables required. The agent uses existing:
- `APQR_Segregated/` directory structure
- Domain agent tools (ERP, LIMS, DMS)
- Document processing tools (Word, Excel, PDF)

### Output Directory

The agent creates outputs in:
```
output/apqr_drafts/
├── APQR_Draft_Aspirin_Partial_20241110.docx
├── completion_report_20241110_143022.json
├── yield_trend_data.csv
├── qc_assay_trend_data.csv
└── deviation_trend_data.csv
```

This directory is automatically created if it doesn't exist.

---

## Usage Patterns

### Pattern 1: Generate APQR for All Available Batches

**User Query:**
```
Fill APQR for Aspirin with all available batches
```

**Agent Behavior:**
- Scans for all batches in system
- Extracts data for all batches found
- Generates complete APQR draft

### Pattern 2: Generate APQR for Specific Batches

**User Query:**
```
Generate APQR draft for batches ASP-25-001 and ASP-25-002 only
```

**Agent Behavior:**
- Validates specified batch numbers
- Extracts data for those batches only
- Marks multi-batch sections as "Partial Data"

### Pattern 3: Re-generate APQR with Updated Data

**User Query:**
```
Regenerate APQR for Aspirin batches 1-4
```

**Agent Behavior:**
- Re-scans all data sources
- Updates existing draft
- Flags any changes from previous version

---

## Testing the Integration

### Quick Test

```bash
cd /path/to/agentic_apqr
python examples/apqr_data_filler_example.py
```

This will run 7 examples demonstrating all agent capabilities.

### Full System Test

```python
from agentic_apqr.agents.orchestrator_agent import orchestrator_agent

# Test query
response = orchestrator_agent.generate_content(
    "Fill APQR for Aspirin batches ASP-25-001 through ASP-25-004"
)

print(response.text)
# Expected: "Routing to APQR Data Filler Agent..."
# Then: "✓ APQR data extraction complete. 85% sections filled. ..."
```

---

## Troubleshooting

### Issue 1: Agent Not Routing to Data Filler

**Symptom:** Orchestrator routes to individual domain agents instead of Data Filler

**Solution:**
- Ensure query contains keywords: "fill APQR", "generate APQR", "populate APQR"
- Check orchestrator_agent.py imports Data Filler Agent
- Verify Data Filler Agent in orchestrator's sub_agents list

### Issue 2: Data Extraction Returns "No Information Found"

**Symptom:** Completion report shows 0% or very low completion

**Solution:**
- Verify APQR_Segregated/ directory structure is correct
- Check batch folder naming (Batch_1_Jan_Feb, Batch_2_Feb_Mar, etc.)
- Ensure documents exist in Manufacturing/, SupplyChain/, QC/ folders
- Check database_metadata/*_INDEX.txt files are populated

### Issue 3: Template Population Fails

**Symptom:** Error generating partial document

**Solution:**
- Verify APQR template path is correct
- Check template has proper section headers
- Ensure docx library is installed: `pip install python-docx`
- Verify output directory has write permissions

### Issue 4: CSV Generation Fails

**Symptom:** Trend CSV files not created

**Solution:**
- Verify output/apqr_drafts/ directory exists and is writable
- Check batch data structure matches expected format
- Ensure csv module is available (standard library)

---

## Performance Considerations

### Expected Performance

| Operation | Expected Time | Notes |
|-----------|---------------|-------|
| Batch Scanning | < 1 second | Scans 4 batch folders |
| ERP Data Extraction | 2-5 seconds | Per batch |
| LIMS Data Extraction | 3-8 seconds | Per batch (COA parsing) |
| DMS Data Extraction | 2-4 seconds | Shared across batches |
| CSV Generation | < 1 second | Per CSV file |
| Document Generation | 5-10 seconds | Full APQR draft |
| **Total (4 batches)** | **< 2 minutes** | End-to-end |

### Optimization Tips

1. **Parallel Queries**
   - Domain agents are queried in parallel
   - Reduces total time vs. sequential queries

2. **Caching**
   - Consider caching extracted data
   - Reuse for multiple APQR generations

3. **Incremental Updates**
   - Only re-extract data for changed batches
   - Merge with existing draft

---

## Security & Compliance

### GMP Compliance

✅ **Attributable:** All data citations include source file paths  
✅ **Legible:** Clear formatting and structured output  
✅ **Contemporaneous:** Extraction timestamps recorded  
✅ **Original:** Source data preserved, not modified  
✅ **Accurate:** Data validation and conflict detection  

### Audit Trail

The agent generates:
- Data extraction log (all queries executed)
- Section completion report (data availability)
- CSV exports (trend data for analysis)
- Document metadata (generation timestamp, batches, completion %)

All outputs are traceable and auditable.

---

## API Reference

### Key Functions

#### `get_available_batches(product_name: str) -> Dict`
Scans for available batch folders and returns batch metadata.

**Returns:**
```python
{
    "product": "Aspirin",
    "batches_found": ["ASP-25-001", "ASP-25-002", ...],
    "batch_details": {
        "ASP-25-001": {
            "batch_number": "ASP-25-001",
            "period": "Jan-Feb 2024",
            "erp_data_available": true,
            "lims_data_available": true,
            "dms_data_available": true,
            "completeness": "complete"
        }
    },
    "total_batches": 4,
    "complete_batches": 4
}
```

#### `extract_section_data(section_name, domain, query, tool) -> Dict`
Extracts data for a specific APQR section from a domain agent.

**Returns:**
```python
{
    "section_name": "Batch Manufacturing Records",
    "domain": "ERP",
    "status": "success",
    "data": {...},
    "extraction_timestamp": "2024-11-10T14:30:22",
    "source_files": ["BMR_ASP-25-001.pdf", ...]
}
```

#### `generate_trend_csv(data_type, batch_data, filename) -> Dict`
Generates CSV files for trend analysis.

**Returns:**
```python
{
    "status": "success",
    "data_type": "yield",
    "output_path": "/path/to/yield_trend_data.csv",
    "records_count": 4
}
```

#### `create_completion_report(sections_status) -> Dict`
Creates a comprehensive section completion report.

**Returns:**
```python
{
    "completion_percentage": 85.3,
    "complete_sections": [...],
    "incomplete_sections": [...],
    "missing_data_items": [...],
    "data_quality_score": 90.1
}
```

---

## Future Enhancements

### Phase 2 (Planned)
- [ ] PDF export for APQR drafts
- [ ] Automatic graph generation from CSV data
- [ ] Smart data reconciliation (conflict resolution AI)
- [ ] Multi-product support (beyond Aspirin)
- [ ] Real-time progress tracking (streaming updates)

### Phase 3 (Roadmap)
- [ ] Machine learning for data extraction accuracy
- [ ] Predictive data gap detection
- [ ] Automated data quality scoring
- [ ] Integration with external ERP/LIMS systems
- [ ] Natural language query interface enhancement

---

## Support

**Documentation:** See `APQR_DATA_FILLER_AGENT_README.md` for detailed documentation  
**Examples:** See `examples/apqr_data_filler_example.py` for usage examples  
**Issues:** Log in project issue tracker with tag `agent:data-filler`

---

## Changelog

### Version 1.0.0 (November 10, 2024)
- ✅ Initial release
- ✅ Full integration with existing system
- ✅ Support for 4 batches (ASP-25-001 to ASP-25-004)
- ✅ Parallel data extraction from all domains
- ✅ CSV trend generation
- ✅ Completion reporting
- ✅ Comprehensive documentation

---

**End of Integration Guide**

