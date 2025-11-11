"""
APQR Data Filler Agent - Usage Examples
Demonstrates how to use the Data Filler Agent to automatically populate APQR templates.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentic_apqr.tools import (
    get_available_batches,
    extract_section_data,
    generate_trend_csv,
    create_completion_report,
    generate_partial_doc,
    # Domain query tools
    query_erp_manufacturing,
    query_lims_qc,
    query_dms_qa
)


def example_1_scan_available_batches():
    """
    Example 1: Scan for available batches in the system
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Scanning for Available Batches")
    print("="*80)
    
    batch_info = get_available_batches(product_name="Aspirin")
    
    print(f"\n✅ Product: {batch_info.get('product')}")
    print(f"✅ Total Batches Found: {batch_info.get('total_batches')}")
    print(f"✅ Batches: {', '.join(batch_info.get('batches_found', []))}")
    print(f"✅ Complete Batches: {batch_info.get('complete_batches')}")
    print(f"✅ Partial Batches: {batch_info.get('partial_batches')}")
    
    print("\n📊 Batch Details:")
    for batch_num, details in batch_info.get('batch_details', {}).items():
        print(f"\n  {batch_num}:")
        print(f"    Period: {details.get('period')}")
        print(f"    ERP Data: {'✅' if details.get('erp_data_available') else '❌'}")
        print(f"    LIMS Data: {'✅' if details.get('lims_data_available') else '❌'}")
        print(f"    DMS Data: {'✅' if details.get('dms_data_available') else '❌'}")
        print(f"    Completeness: {details.get('completeness')}")
    
    return batch_info


def example_2_extract_manufacturing_data():
    """
    Example 2: Extract manufacturing data from ERP
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Extracting Manufacturing Data")
    print("="*80)
    
    section_data = extract_section_data(
        section_name="Batch Manufacturing Records",
        domain="ERP",
        query="Retrieve BMR and yield data for batches ASP-25-001 to ASP-25-004",
        domain_agent_tool=query_erp_manufacturing
    )
    
    print(f"\n✅ Section: {section_data.get('section_name')}")
    print(f"✅ Domain: {section_data.get('domain')}")
    print(f"✅ Status: {section_data.get('status')}")
    print(f"✅ Extraction Time: {section_data.get('extraction_timestamp')}")
    
    if section_data.get('source_files'):
        print(f"\n📄 Source Files:")
        for file in section_data.get('source_files', [])[:5]:  # Show first 5
            print(f"  - {file}")
    
    return section_data


def example_3_extract_qc_data():
    """
    Example 3: Extract QC test results from LIMS
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Extracting QC Test Results")
    print("="*80)
    
    section_data = extract_section_data(
        section_name="QC Test Results & COA",
        domain="LIMS",
        query="Retrieve COA and assay results for batches ASP-25-001 to ASP-25-004",
        domain_agent_tool=query_lims_qc
    )
    
    print(f"\n✅ Section: {section_data.get('section_name')}")
    print(f"✅ Domain: {section_data.get('domain')}")
    print(f"✅ Status: {section_data.get('status')}")
    
    data = section_data.get('data', {})
    if data.get('documents'):
        print(f"\n📄 Documents Found: {data.get('document_count', 0)}")
        print(f"📄 Document Types:")
        for doc in data.get('documents', [])[:3]:  # Show first 3
            print(f"  - {doc.get('filename')} (Batch: {doc.get('batch', 'Unknown')})")
    
    return section_data


def example_4_extract_deviation_data():
    """
    Example 4: Extract deviation and CAPA data from DMS
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Extracting Deviation & CAPA Data")
    print("="*80)
    
    section_data = extract_section_data(
        section_name="Deviations & CAPA",
        domain="DMS",
        query="Retrieve all deviations, OOS, and CAPA for batches ASP-25-001 to ASP-25-004",
        domain_agent_tool=query_dms_qa
    )
    
    print(f"\n✅ Section: {section_data.get('section_name')}")
    print(f"✅ Domain: {section_data.get('domain')}")
    print(f"✅ Status: {section_data.get('status')}")
    
    return section_data


def example_5_generate_trend_csvs():
    """
    Example 5: Generate trend CSV files for graph generation
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Generating Trend CSV Files")
    print("="*80)
    
    # Sample yield data for 4 batches
    yield_data = [
        {
            "batch_number": "ASP-25-001",
            "period": "Jan-Feb 2024",
            "theoretical_yield": 1000,
            "actual_yield": 985,
            "yield_percentage": 98.5,
            "status": "In Spec"
        },
        {
            "batch_number": "ASP-25-002",
            "period": "Feb-Mar 2024",
            "theoretical_yield": 1000,
            "actual_yield": 987,
            "yield_percentage": 98.7,
            "status": "In Spec"
        },
        {
            "batch_number": "ASP-25-003",
            "period": "Mar-Apr 2024",
            "theoretical_yield": 1000,
            "actual_yield": 983,
            "yield_percentage": 98.3,
            "status": "In Spec"
        },
        {
            "batch_number": "ASP-25-004",
            "period": "Apr-May 2024",
            "theoretical_yield": 1000,
            "actual_yield": 988,
            "yield_percentage": 98.8,
            "status": "In Spec"
        }
    ]
    
    result = generate_trend_csv(
        data_type="yield",
        batch_data=yield_data,
        output_filename="yield_trend_data.csv"
    )
    
    print(f"\n✅ CSV Generation Status: {result.get('status')}")
    print(f"✅ Data Type: {result.get('data_type')}")
    print(f"✅ Records: {result.get('records_count')}")
    print(f"✅ Output Path: {result.get('output_path')}")
    
    # Sample assay data
    assay_data = [
        {
            "batch_number": "ASP-25-001",
            "period": "Jan-Feb 2024",
            "assay_result": 99.5,
            "spec_min": 98.0,
            "spec_max": 102.0,
            "status": "Pass"
        },
        {
            "batch_number": "ASP-25-002",
            "period": "Feb-Mar 2024",
            "assay_result": 99.8,
            "spec_min": 98.0,
            "spec_max": 102.0,
            "status": "Pass"
        },
        {
            "batch_number": "ASP-25-003",
            "period": "Mar-Apr 2024",
            "assay_result": 99.2,
            "spec_min": 98.0,
            "spec_max": 102.0,
            "status": "Pass"
        },
        {
            "batch_number": "ASP-25-004",
            "period": "Apr-May 2024",
            "assay_result": 99.6,
            "spec_min": 98.0,
            "spec_max": 102.0,
            "status": "Pass"
        }
    ]
    
    result2 = generate_trend_csv(
        data_type="assay",
        batch_data=assay_data,
        output_filename="qc_assay_trend_data.csv"
    )
    
    print(f"\n✅ CSV Generation Status: {result2.get('status')}")
    print(f"✅ Data Type: {result2.get('data_type')}")
    print(f"✅ Records: {result2.get('records_count')}")
    print(f"✅ Output Path: {result2.get('output_path')}")
    
    return result, result2


def example_6_create_completion_report():
    """
    Example 6: Create a section completion report
    """
    print("\n" + "="*80)
    print("EXAMPLE 6: Creating Section Completion Report")
    print("="*80)
    
    # Sample sections status
    sections_status = {
        "Header & Product Details": {
            "status": "success",
            "domain": "ERP"
        },
        "Batch Manufacturing Records": {
            "status": "success",
            "domain": "ERP"
        },
        "Yield Reconciliation": {
            "status": "success",
            "domain": "ERP"
        },
        "QC Test Results": {
            "status": "success",
            "domain": "LIMS"
        },
        "Stability Data - 24 month": {
            "status": "no_information_found",
            "domain": "LIMS",
            "message": "24-month stability data not available"
        },
        "Deviations & CAPA": {
            "status": "success",
            "domain": "DMS"
        },
        "Training Records": {
            "status": "success",
            "domain": "DMS"
        },
        "Audit Report Q2": {
            "status": "no_information_found",
            "domain": "DMS",
            "message": "Q2 audit report not found"
        }
    }
    
    report = create_completion_report(sections_status)
    
    print(f"\n✅ Completion Percentage: {report.get('completion_percentage')}%")
    print(f"✅ Data Quality Score: {report.get('data_quality_score')}")
    print(f"✅ Total Sections: {report.get('total_sections')}")
    print(f"✅ Completed Sections: {report.get('completed_sections_count')}")
    print(f"✅ Incomplete Sections: {report.get('incomplete_sections_count')}")
    
    print(f"\n📊 Complete Sections:")
    for section in report.get('complete_sections', []):
        print(f"  ✅ {section}")
    
    print(f"\n⚠️ Incomplete Sections:")
    for section in report.get('incomplete_sections', []):
        print(f"  ⚠️ {section}")
    
    print(f"\n❌ Missing Data Items:")
    for item in report.get('missing_data_items', []):
        print(f"  - {item.get('section')}: {item.get('reason')} (Domain: {item.get('domain')})")
    
    return report


def example_7_full_workflow():
    """
    Example 7: Complete end-to-end workflow for APQR generation
    """
    print("\n" + "="*80)
    print("EXAMPLE 7: Complete End-to-End APQR Generation Workflow")
    print("="*80)
    
    # Step 1: Scan for batches
    print("\n[Step 1/6] Scanning for available batches...")
    batch_info = get_available_batches("Aspirin")
    batches = batch_info.get('batches_found', [])
    print(f"✅ Found {len(batches)} batches: {', '.join(batches)}")
    
    # Step 2: Extract data from all domains
    print("\n[Step 2/6] Extracting data from domain agents...")
    
    all_section_data = {}
    
    # ERP data
    print("  → Querying ERP Manufacturing...")
    all_section_data["Manufacturing"] = extract_section_data(
        "Batch Manufacturing Records", "ERP",
        f"Retrieve BMR for batches {', '.join(batches)}",
        query_erp_manufacturing
    )
    
    # LIMS data
    print("  → Querying LIMS QC...")
    all_section_data["QC Results"] = extract_section_data(
        "QC Test Results", "LIMS",
        f"Retrieve COA for batches {', '.join(batches)}",
        query_lims_qc
    )
    
    # DMS data
    print("  → Querying DMS QA...")
    all_section_data["Deviations"] = extract_section_data(
        "Deviations & CAPA", "DMS",
        f"Retrieve deviations for batches {', '.join(batches)}",
        query_dms_qa
    )
    
    print(f"✅ Extracted data for {len(all_section_data)} sections")
    
    # Step 3: Generate trend CSVs
    print("\n[Step 3/6] Generating trend CSV files...")
    yield_data = [
        {"batch_number": b, "period": f"Period {i+1}", "yield_percentage": 98.5 + i*0.1}
        for i, b in enumerate(batches)
    ]
    csv_result = generate_trend_csv("yield", yield_data, "yield_trend_example.csv")
    print(f"✅ Generated: {csv_result.get('output_path')}")
    
    # Step 4: Create completion report
    print("\n[Step 4/6] Creating completion report...")
    sections_status = {
        section: {"status": data.get("status"), "domain": data.get("domain")}
        for section, data in all_section_data.items()
    }
    report = create_completion_report(sections_status)
    print(f"✅ Completion: {report.get('completion_percentage')}%")
    
    # Step 5: Generate partial document (simulated)
    print("\n[Step 5/6] Generating partial APQR document...")
    print(f"✅ Would generate: APQR_Draft_Aspirin_Partial_[Date].docx")
    print(f"✅ Sections filled: {report.get('completed_sections_count')}")
    print(f"✅ Sections marked missing: {report.get('incomplete_sections_count')}")
    
    # Step 6: Ready to transfer to Compiler
    print("\n[Step 6/6] Ready to transfer to Compiler Agent")
    print(f"✅ Package prepared with:")
    print(f"  - APQR draft document")
    print(f"  - Completion report ({report.get('completion_percentage')}% complete)")
    print(f"  - {len(yield_data)} CSV trend files")
    print(f"  - Data extraction logs")
    
    print("\n" + "="*80)
    print("✅ END-TO-END WORKFLOW COMPLETE")
    print("="*80)
    
    return {
        "batches": batches,
        "section_data": all_section_data,
        "completion_report": report,
        "status": "success"
    }


def main():
    """
    Run all examples
    """
    print("\n" + "="*80)
    print("APQR DATA FILLER AGENT - USAGE EXAMPLES")
    print("="*80)
    
    try:
        # Run examples
        example_1_scan_available_batches()
        example_2_extract_manufacturing_data()
        example_3_extract_qc_data()
        example_4_extract_deviation_data()
        example_5_generate_trend_csvs()
        example_6_create_completion_report()
        example_7_full_workflow()
        
        print("\n" + "="*80)
        print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

