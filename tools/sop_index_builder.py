"""
SOP Index Builder
Systematically parses all SOPs in DMS directory and builds a searchable index.
Similar to document_index_builder.py but specialized for SOP documents.

Author: APQR System
Created: 2025-01-11
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Import existing tools
try:
    from .pdf_tools import extract_text_from_pdf, extract_tables_from_pdf
    from .word_tools import extract_text_from_docx, extract_tables_from_docx
except ImportError:
    from pdf_tools import extract_text_from_pdf, extract_tables_from_pdf
    from word_tools import extract_text_from_docx, extract_tables_from_docx

class SOPIndexBuilder:
    """Builds a comprehensive index of all SOPs in the DMS directory."""
    
    def __init__(self, dms_path: Path):
        self.dms_path = Path(dms_path)
        self.sop_index = {
            "metadata": {
                "indexed_at": datetime.now().isoformat(),
                "total_sops": 0,
                "dms_path": str(dms_path)
            },
            "sops": {}
        }
    
    def extract_version_from_path(self, file_path: Path) -> Optional[str]:
        """Extract version number from folder path structure."""
        path_str = str(file_path)
        
        # Pattern 1: Version-2, Version-3, etc.
        match = re.search(r'/Version[_-](\d+(?:\.\d+)?)', path_str, re.IGNORECASE)
        if match:
            return match.group(1)
        
        # Pattern 2: v2, v3, v2.0, etc.
        match = re.search(r'/v(\d+(?:\.\d+)?)', path_str, re.IGNORECASE)
        if match:
            return match.group(1)
        
        return None
    
    def extract_sop_metadata(self, file_path: Path) -> Dict[str, Any]:
        """Extract comprehensive metadata from an SOP document."""
        metadata = {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "sop_number": None,
            "version": None,
            "title": None,
            "full_title": None,  # Complete extracted title
            "department": None,
            "effective_date": None,
            "revision_date": None,
            "approved_by": None,
            "reviewed_by": None,
            "prepared_by": None,
            "purpose": None,
            "scope": None,
            "sections": [],
            "keywords": [],  # Extracted keywords for semantic search
            "aliases": [],   # Alternative names (BMR, PPE, etc.)
            "content_summary": None  # First 500 chars of content
        }
        
        # Extract version from path first
        metadata["version"] = self.extract_version_from_path(file_path)
        
        # Extract SOP number from filename
        # Patterns: SOP-PROD-001, SOP_MFG_002, SOP-QC-003
        match = re.search(r'SOP[_-]([A-Z]+)[_-](\d+)', file_path.name, re.IGNORECASE)
        if match:
            dept_code = match.group(1)
            number = match.group(2)
            metadata["sop_number"] = f"SOP-{dept_code.upper()}-{number}"
            
            # Map department codes
            dept_mapping = {
                "PROD": "Production",
                "MFG": "Manufacturing",
                "QC": "Quality Control",
                "QA": "Quality Assurance",
                "PKG": "Packaging",
                "WHS": "Warehouse",
                "ENG": "Engineering",
                "REG": "Regulatory Affairs"
            }
            metadata["department"] = dept_mapping.get(dept_code.upper(), dept_code.upper())
        
        # Parse document content
        try:
            if file_path.suffix.lower() == '.pdf':
                text = extract_text_from_pdf(str(file_path))
                tables = extract_tables_from_pdf(str(file_path))
            elif file_path.suffix.lower() in ['.docx', '.doc']:
                text = extract_text_from_docx(str(file_path))
                tables = extract_tables_from_docx(str(file_path))
            else:
                return metadata
            
            # Extract title (usually in first few lines)
            lines = text.split('\n')[:30]
            full_text_lower = text.lower()
            
            # Try to find the actual title (look for "Title:" or similar)
            title_match = re.search(r'Title[:\s]+([^\n]{10,150})', text, re.IGNORECASE)
            if title_match:
                metadata["full_title"] = title_match.group(1).strip()
                metadata["title"] = title_match.group(1).strip()[:100]  # Truncate for display
            
            # If no explicit title, extract from content
            if not metadata["title"]:
                for line in lines:
                    line = line.strip()
                    if len(line) > 15 and not line.startswith('SOP') and not 'Version' in line and not 'Document Type' in line:
                        # Look for title-like patterns
                        if any(keyword in line.lower() for keyword in ['procedure', 'operation', 'manufacturing', 'testing', 'control', 'management', 'dispensing', 'handling', 'maintenance', 'calibration', 'safety']):
                            metadata["title"] = line[:100]
                            metadata["full_title"] = line
                            break
            
            # Extract keywords from content (common terms for semantic search)
            keywords = set()
            
            # Add department-specific keywords
            if metadata["department"]:
                keywords.add(metadata["department"].lower())
            
            # Extract keywords from title
            if metadata["title"]:
                title_words = re.findall(r'\b[a-z]{4,}\b', metadata["title"].lower())
                keywords.update(title_words)
            
            # Extract keywords from purpose
            if metadata["purpose"]:
                purpose_words = re.findall(r'\b[a-z]{4,}\b', metadata["purpose"].lower())
                keywords.update(purpose_words[:10])  # Limit to 10 most relevant
            
            # Common acronyms and aliases mapping
            alias_mapping = {
                'bmr': ['batch manufacturing record', 'batch record', 'manufacturing record'],
                'ppe': ['personal protective equipment', 'safety equipment', 'protective gear'],
                'hplc': ['high performance liquid chromatography', 'chromatography'],
                'capa': ['corrective action', 'preventive action'],
                'sop': ['standard operating procedure', 'procedure'],
                'gmp': ['good manufacturing practice'],
                'deviation': ['non-conformance', 'discrepancy'],
                'calibration': ['equipment qualification', 'instrument verification'],
                'cleaning': ['sanitization', 'housekeeping'],
                'sampling': ['sample collection', 'specimen collection'],
                'dissolution': ['drug release', 'dissolution test'],
                'tablet': ['compression', 'tablet press', 'compression machine'],
                'packaging': ['packing', 'labeling', 'packaging materials'],
                'warehouse': ['storage', 'inventory', 'receiving'],
                'dispensing': ['material dispensing', 'weighing', 'raw material'],
                'validation': ['qualification', 'verification'],
                'change control': ['change management', 'modification'],
                'training': ['personnel training', 'operator training'],
                'environmental monitoring': ['cleanroom', 'hvac', 'air quality']
            }
            
            # Check which aliases apply to this SOP
            for acronym, full_terms in alias_mapping.items():
                if acronym in full_text_lower:
                    metadata["aliases"].append(acronym)
                    keywords.add(acronym)
                for term in full_terms:
                    if term in full_text_lower:
                        metadata["aliases"].append(acronym)
                        keywords.add(acronym)
                        break
            
            # Store unique keywords
            metadata["keywords"] = sorted(list(keywords))
            
            # Extract content summary (first 500 chars of actual content)
            # Skip headers and go straight to purpose/scope
            content_start = text.find('Purpose')
            if content_start == -1:
                content_start = text.find('Scope')
            if content_start == -1:
                content_start = 200  # Skip first 200 chars of headers
            
            metadata["content_summary"] = text[content_start:content_start+500].strip()
            
            # Extract version from content if not found in path
            if not metadata["version"]:
                version_match = re.search(r'Version[:\s]+(\d+(?:\.\d+)?)', text, re.IGNORECASE)
                if version_match:
                    metadata["version"] = version_match.group(1)
            
            # Extract effective date
            effective_match = re.search(r'Effective Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text, re.IGNORECASE)
            if effective_match:
                metadata["effective_date"] = effective_match.group(1)
            
            # Extract revision date
            revision_match = re.search(r'Revision Date[:\s]+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text, re.IGNORECASE)
            if revision_match:
                metadata["revision_date"] = revision_match.group(1)
            
            # Extract approvers from text
            approved_match = re.search(r'Approved By[:\s]+([A-Za-z\s\.]+)', text, re.IGNORECASE)
            if approved_match:
                metadata["approved_by"] = approved_match.group(1).strip()
            
            reviewed_match = re.search(r'Reviewed By[:\s]+([A-Za-z\s\.]+)', text, re.IGNORECASE)
            if reviewed_match:
                metadata["reviewed_by"] = reviewed_match.group(1).strip()
            
            prepared_match = re.search(r'Prepared By[:\s]+([A-Za-z\s\.]+)', text, re.IGNORECASE)
            if prepared_match:
                metadata["prepared_by"] = prepared_match.group(1).strip()
            
            # Extract purpose
            purpose_match = re.search(r'Purpose[:\s]+(.+?)(?:\n\n|\nScope)', text, re.IGNORECASE | re.DOTALL)
            if purpose_match:
                metadata["purpose"] = purpose_match.group(1).strip()[:500]  # Limit length
            
            # Extract scope
            scope_match = re.search(r'Scope[:\s]+(.+?)(?:\n\n|\nResponsibilities)', text, re.IGNORECASE | re.DOTALL)
            if scope_match:
                metadata["scope"] = scope_match.group(1).strip()[:500]  # Limit length
            
            # Extract section headings
            section_pattern = r'^(\d+\.)\s+([A-Z][A-Za-z\s]+)'
            for line in lines:
                match = re.match(section_pattern, line.strip())
                if match:
                    metadata["sections"].append({
                        "number": match.group(1),
                        "title": match.group(2).strip()
                    })
        
        except Exception as e:
            print(f"⚠️ Error parsing {file_path.name}: {e}")
        
        return metadata
    
    def build_index(self) -> Dict[str, Any]:
        """Build comprehensive SOP index by traversing all SOP directories."""
        print("=" * 80)
        print("🔍 BUILDING SOP INDEX")
        print("=" * 80)
        
        # Find all SOP directories
        sop_directories = [
            self.dms_path / "13. List of all the SOPs",
            self.dms_path / "SOPs",
            self.dms_path / "Standard Operating Procedures"
        ]
        
        sop_files = []
        for sop_dir in sop_directories:
            if sop_dir.exists():
                print(f"\n📁 Scanning directory: {sop_dir.name}")
                # Recursively find all PDF and DOCX files
                sop_files.extend(list(sop_dir.rglob("*.pdf")))
                sop_files.extend(list(sop_dir.rglob("*.docx")))
                sop_files.extend(list(sop_dir.rglob("*.doc")))
        
        print(f"\n✅ Found {len(sop_files)} SOP documents")
        
        # Process each SOP
        for idx, sop_file in enumerate(sop_files, 1):
            print(f"\n[{idx}/{len(sop_files)}] Processing: {sop_file.name}")
            
            metadata = self.extract_sop_metadata(sop_file)
            
            # Use SOP number as key, or filename if SOP number not found
            sop_key = metadata["sop_number"] or sop_file.stem
            
            # If SOP already exists, store as different version
            if sop_key in self.sop_index["sops"]:
                version = metadata["version"] or "unknown"
                sop_key = f"{sop_key}_v{version}"
            
            self.sop_index["sops"][sop_key] = metadata
            
            print(f"  ✓ SOP Number: {metadata['sop_number']}")
            print(f"  ✓ Version: {metadata['version']}")
            print(f"  ✓ Department: {metadata['department']}")
            print(f"  ✓ Title: {metadata['title'][:60] if metadata['title'] else 'Not found'}...")
            if metadata['aliases']:
                print(f"  ✓ Aliases: {', '.join(metadata['aliases'][:5])}")
            if metadata['keywords']:
                print(f"  ✓ Keywords: {', '.join(list(metadata['keywords'])[:8])}")
        
        # Update metadata
        self.sop_index["metadata"]["total_sops"] = len(self.sop_index["sops"])
        
        return self.sop_index
    
    def save_index(self, output_path: Path):
        """Save the SOP index to a JSON file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.sop_index, f, indent=2, ensure_ascii=False)
        
        print("\n" + "=" * 80)
        print(f"✅ SOP INDEX SAVED: {output_path}")
        print("=" * 80)
        print(f"📊 Total SOPs indexed: {self.sop_index['metadata']['total_sops']}")
        print(f"📅 Indexed at: {self.sop_index['metadata']['indexed_at']}")


def build_sop_index():
    """Main function to build the SOP index."""
    # Define paths
    dms_path = Path(__file__).parent.parent / "APQR_Segregated" / "DMS"
    output_path = Path(__file__).parent.parent / "output" / "sop_index.json"
    
    # Build index
    builder = SOPIndexBuilder(dms_path)
    index = builder.build_index()
    builder.save_index(output_path)
    
    return index


if __name__ == "__main__":
    build_sop_index()

