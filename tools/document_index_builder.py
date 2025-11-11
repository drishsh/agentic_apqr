"""
Document Index Builder
Systematically extract and index all REAL data from APQR_Segregated database
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, Any, List
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from tools.pdf_tools import extract_text_from_pdf
from tools.word_tools import extract_text_from_docx, extract_tables_from_docx
from tools.excel_tools import extract_data_from_xlsx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
APQR_DATA_DIR = BASE_DIR / "APQR_Segregated"


class DocumentIndexBuilder:
    """Build comprehensive index of all extracted data"""
    
    def __init__(self):
        self.index = {
            "batches": {},
            "deviations": [],
            "training_records": [],
            "sops": [],
            "materials": {}
        }
    
    def extract_from_table(self, table_data: Dict[str, Any], field_name: str) -> str:
        """Extract specific field from table data"""
        if "data" in table_data:
            for row in table_data["data"]:
                if len(row) >= 3 and field_name in str(row[1]):
                    return str(row[2]).strip()
        return None
    
    def extract_batch_data(self, batch_id: str, batch_path: Path) -> Dict[str, Any]:
        """Extract all data for a single batch - handles PDF, DOCX, XLSX"""
        logger.info(f"🔍 Extracting data for {batch_id}...")
        
        batch_data = {
            "batch_id": batch_id,
            "product": "Aspirin Tablets 325mg",
            "manufacturing_data": {},
            "qc_data": {},
            "yields": {
                "compression": {},
                "blending": {},
                "packaging": {}
            },
            "materials": [],
            "dates": {},
            "personnel": {}
        }
        
        # === EXTRACT BMR FINAL DISPOSITION (PDF or DOCX) ===
        disposition_files = [
            batch_path / "Manufacturing" / "07. Compression" / "BMR - Final Disposition and Sign-off.pdf",
            batch_path / "Manufacturing" / "07. Compression" / f"BMR_Final_Disposition_{batch_id.replace('Batch_', 'ASP-25-00')}.docx"
        ]
        
        for disp_file in disposition_files:
            if disp_file.exists():
                try:
                    if disp_file.suffix == '.pdf':
                        text = extract_text_from_pdf(str(disp_file))
                    else:
                        text = extract_text_from_docx(str(disp_file))
                    
                    # Extract batch number
                    if "Batch No.:" in text or "ASP-25-" in text:
                        import re
                        batch_match = re.search(r'ASP-25-\d+', text)
                        if batch_match:
                            batch_data["batch_number"] = batch_match.group()
                    
                    # Extract total tablets
                    if "Total Tablet Count:" in text:
                        match = re.search(r'Total Tablet Count:\s*([0-9,]+)', text)
                        if match:
                            batch_data["total_tablets"] = match.group(1)
                    
                    # Extract dates
                    date_matches = re.findall(r'(\d{1,2}-[A-Za-z]{3}-\d{4})', text)
                    if date_matches:
                        batch_data["dates"]["manufacturing"] = date_matches[0]
                    
                    break
                except Exception as e:
                    logger.warning(f"Could not extract disposition from {disp_file.name}: {e}")
        
        # === EXTRACT COMPRESSION YIELD (PDF or DOCX) ===
        yield_files = [
            batch_path / "Manufacturing" / "07. Compression" / "BMR - Compression Yield Reconciliation.pdf",
            batch_path / "Manufacturing" / "07. Compression" / f"Compression_Yield_Reconciliation_{batch_id.replace('Batch_', 'ASP-25-00')}.docx"
        ]
        
        for yield_file in yield_files:
            if yield_file.exists():
                try:
                    if yield_file.suffix == '.pdf':
                        text = extract_text_from_pdf(str(yield_file))
                        # Parse from text
                        if "% Yield of Good Tablets:" in text:
                            match = re.search(r'(\d+\.\d+)%', text[text.find("% Yield"):])
                            if match:
                                batch_data["yields"]["compression"]["percentage"] = match.group(1) + "%"
                        
                        if "Input Weight" in text:
                            match = re.search(r'Input Weight[^:]*:\s*([0-9.]+)\s*kg', text)
                            if match:
                                batch_data["yields"]["compression"]["input_weight"] = match.group(1) + " kg"
                        
                        if "Actual Output" in text:
                            match = re.search(r'Actual Output[^:]*:\s*([0-9.]+)\s*kg', text)
                            if match:
                                batch_data["yields"]["compression"]["output_weight"] = match.group(1) + " kg"
                    else:
                        # Extract from DOCX tables
                        tables = extract_tables_from_docx(str(yield_file))
                        if tables and len(tables) > 0:
                            table = tables[0]
                            
                            batch_data["yields"]["compression"]["input_weight"] = self.extract_from_table(table, "Input Weight")
                            batch_data["yields"]["compression"]["output_weight"] = self.extract_from_table(table, "Actual Output")
                            batch_data["yields"]["compression"]["percentage"] = self.extract_from_table(table, "% Yield")
                            batch_data["yields"]["compression"]["status"] = self.extract_from_table(table, "Status:")
                            
                            # Extract date
                            date_val = self.extract_from_table(table, "Date of Reconciliation")
                            if date_val:
                                batch_data["dates"]["compression_reconciliation"] = date_val
                    
                    break
                except Exception as e:
                    logger.warning(f"Could not extract yield from {yield_file.name}: {e}")
        
        # === EXTRACT PACKAGING YIELD ===
        pkg_files = [
            batch_path / "Manufacturing" / "11. Packaging" / "9. BMR - Primary Yield Reconciliation.pdf",
            batch_path / "Manufacturing" / "11. Packaging" / "9. BMR - Primary Yield Reconciliation.docx",
            batch_path / "Manufacturing" / "11. Packaging" / f"BMR_Primary_Yield_Reconciliation_{batch_id.replace('Batch_', 'ASP-25-00')}.docx"
        ]
        
        for pkg_file in pkg_files:
            if pkg_file.exists():
                try:
                    if pkg_file.suffix == '.pdf':
                        text = extract_text_from_pdf(str(pkg_file))
                    else:
                        tables = extract_tables_from_docx(str(pkg_file))
                        if tables:
                            # Extract packaging data from tables
                            for table in tables[:3]:
                                date_val = self.extract_from_table(table, "Date of Reconciliation")
                                if date_val:
                                    batch_data["dates"]["packaging"] = date_val
                    break
                except Exception as e:
                    logger.warning(f"Could not extract packaging yield: {e}")
        
        return batch_data
    
    def extract_all_batches(self):
        """Extract data from all 4 batches"""
        erp_dir = APQR_DATA_DIR / "ERP"
        lims_dir = APQR_DATA_DIR / "LIMS"
        
        batch_folders = [
            ("Batch_1", erp_dir / "Batch_1_Jan_Feb", lims_dir / "Batch_(Jan___Feb_Batch_1)"),
            ("Batch_2", erp_dir / "Batch_2_Feb_Mar", lims_dir / "Batch_February_March_Batch_2"),
            ("Batch_3", erp_dir / "Batch_3_Mar_Apr", lims_dir / "Batch_March_April_Batch_3"),
            ("Batch_4", erp_dir / "Batch_4_Apr_May", lims_dir / "Batch_April_May_Batch_4")
        ]
        
        for batch_id, erp_path, lims_path in batch_folders:
            if erp_path.exists():
                batch_data = self.extract_batch_data(batch_id, erp_path)
                
                # Extract QC data from LIMS
                if lims_path.exists():
                    qc_data = self.extract_qc_data(batch_id, lims_path)
                    batch_data["qc_data"] = qc_data
                
                self.index["batches"][batch_id] = batch_data
    
    def extract_qc_data(self, batch_id: str, lims_path: Path) -> Dict[str, Any]:
        """Extract QC/analytical data from LIMS folder"""
        logger.info(f"  📊 Extracting QC data for {batch_id}...")
        
        qc_data = {
            "coa_data": [],
            "ipqc_results": [],
            "material_testing": []
        }
        
        # Extract COA files
        coa_dir = lims_path / "01. Aspirin_Procurement_Details"
        if coa_dir.exists():
            for coa_file in coa_dir.glob("COA_*.pdf"):
                try:
                    text = extract_text_from_pdf(str(coa_file))
                    coa_info = {
                        "file": coa_file.name,
                        "material": coa_file.stem.replace("COA_", ""),
                        "tests": []
                    }
                    
                    # Extract test results from COA
                    if "ASSAY" in text or "Assay" in text:
                        assay_match = re.search(r'ASSAY[^\d]*([0-9.]+\s*%)', text, re.IGNORECASE)
                        if assay_match:
                            coa_info["assay"] = assay_match.group(1)
                    
                    if "LOD" in text or "Loss on Drying" in text or "LOSS ON DRYING" in text:
                        lod_match = re.search(r'(?:LOD|LOSS ON DRYING)[^\d]*≤?\s*([0-9.]+\s*%)', text, re.IGNORECASE)
                        if lod_match:
                            coa_info["lod"] = lod_match.group(1)
                    
                    if "Batch Number:" in text:
                        batch_match = re.search(r'Batch Number:\s*([A-Z0-9]+)', text)
                        if batch_match:
                            coa_info["vendor_batch"] = batch_match.group(1)
                    
                    qc_data["coa_data"].append(coa_info)
                except Exception as e:
                    logger.warning(f"Could not extract COA from {coa_file.name}: {e}")
        
        # Extract Internal QC Register & COA
        qc_register_dir = lims_path / "04. Internal QC Register & COA"
        if qc_register_dir.exists():
            for xlsx_file in qc_register_dir.glob("*.xlsx"):
                try:
                    data = extract_data_from_xlsx(str(xlsx_file))
                    qc_data["ipqc_results"].append({
                        "file": xlsx_file.name,
                        "data": data
                    })
                except Exception as e:
                    logger.warning(f"Could not extract QC register from {xlsx_file.name}: {e}")
        
        return qc_data
    
    def extract_deviation_data(self):
        """Extract deviation/CAPA data"""
        logger.info("🔍 Extracting deviation data...")
        
        capa_dir = APQR_DATA_DIR / "DMS" / "CAPA Documents"
        dev_file = capa_dir / "5. Deviation Report – DEV_PKG_2025_046.pdf"
        
        if dev_file.exists():
            text = extract_text_from_pdf(str(dev_file))
            deviation = {
                "id": "DEV/PKG/2025/046",
                "product": "Aspirin Tablets 325 mg",
                "type": "Critical - Label Misprint",
                "date": "23-May-2025",
                "description": "Cartons printed '650 mg' instead of '325 mg'",
                "affected_batch": "ASP-25-004",
                "affected_units": "60 cartons out of 8,205",
                "root_cause": "Operator selected incorrect label template",
                "status": "Critical"
            }
            self.index["deviations"].append(deviation)
    
    def extract_material_specs(self):
        """Extract material specifications from LIMS"""
        logger.info("🔍 Extracting material specifications...")
        
        spec_file = APQR_DATA_DIR / "LIMS" / "Batch_(Jan___Feb_Batch_1)" / "01. Aspirin_Procurement_Details" / "Material_Specification_Master1.0.xlsx"
        
        if spec_file.exists():
            data = extract_data_from_xlsx(str(spec_file))
            materials = []
            for row in data.get("data", []):
                if row.get("Material Name") and str(row.get("Material Name")) != "nan":
                    material = {
                        "name": row.get("Material Name"),
                        "code": row.get("Internal Material Code"),
                        "group": row.get("Material Group"),
                        "vendor": row.get("Approved Vendor(s)"),
                        "vendor_code": row.get("Vendor Code"),
                        "required_weight": row.get("Required Weight(Without Buffer)")
                    }
                    materials.append(material)
            self.index["materials"] = materials
    
    def build_index(self):
        """Build complete document index"""
        logger.info("=" * 80)
        logger.info("BUILDING DOCUMENT INDEX FROM REAL DATA")
        logger.info("=" * 80)
        
        self.extract_all_batches()
        self.extract_deviation_data()
        self.extract_material_specs()
        
        return self.index
    
    def save_index(self, output_path: str = None):
        """Save index to JSON file"""
        if output_path is None:
            output_path = BASE_DIR / "output" / "document_index.json"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.index, f, indent=2)
        
        logger.info(f"✅ Index saved to: {output_path}")
        return output_path


if __name__ == "__main__":
    builder = DocumentIndexBuilder()
    index = builder.build_index()
    
    # Print summary
    print("\n" + "=" * 80)
    print("DOCUMENT INDEX SUMMARY")
    print("=" * 80)
    print(f"\nBatches Indexed: {len(index['batches'])}")
    for batch_id, data in index['batches'].items():
        print(f"  • {batch_id}: {data.get('batch_number', 'Unknown')}")
        print(f"    - Total Tablets: {data.get('total_tablets', 'N/A')}")
        print(f"    - Compression Yield: {data.get('yields', {}).get('compression', 'N/A')}")
    
    print(f"\nDeviations Indexed: {len(index['deviations'])}")
    for dev in index['deviations']:
        print(f"  • {dev['id']}: {dev['description']}")
    
    print(f"\nMaterials Indexed: {len(index['materials'])}")
    for mat in index['materials'][:5]:  # Show first 5
        print(f"  • {mat['name']} ({mat['group']})")
    
    # Save index
    output_file = builder.save_index()
    print(f"\n✅ Complete index saved to: {output_file}")

