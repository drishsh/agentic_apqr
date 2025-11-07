"""
APQR Compiler Agent
Synthesizes responses from multiple sub-agents into a coherent, user-friendly answer.
"""

import logging
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CompilationResult:
    """Result of the compilation process."""
    summary: str
    details: List[Dict[str, Any]]
    citations: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


class Compiler:
    """
    Compiler Agent that synthesizes responses from multiple sub-agents.
    
    Responsibilities:
    1. Accept original user query
    2. Accept list of responses from sub-agents (LIMS, ERP, DMS)
    3. Perform synthesis:
       - Deduplicate common information
       - Prioritize most relevant information
       - Check for contradictions
       - Combine information from multiple sources
    4. Produce a friendly, concise answer with citations
    5. Expose compile(query, responses) -> {summary: str, details: list}
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the compiler.
        
        Args:
            config: Optional configuration dictionary for compilation settings
        """
        self.config = config or {}
        self.max_summary_length = self.config.get("max_summary_length", 500)
        self.enable_contradiction_detection = self.config.get("enable_contradiction_detection", True)
        logger.info("Compiler Agent initialized")
    
    def compile(self, query: str, responses: List[Dict[str, Any]]) -> CompilationResult:
        """
        Main compilation method.
        
        Args:
            query: Original user query
            responses: List of response dictionaries from sub-agents
                      Each response should have format:
                      {
                          "agent": "LIMS/ERP/DMS",
                          "results": [...]
                      }
        
        Returns:
            CompilationResult object with summary, details, and citations
        """
        logger.info("Starting compilation for query: %s", query)
        logger.info("Compiling responses from %d agents", len(responses))
        
        # Step 1: Deduplicate responses
        deduplicated = self._deduplicate_responses(responses)
        
        # Step 2: Prioritize information
        prioritized = self._prioritize_responses(deduplicated, query)
        
        # Step 3: Check for contradictions
        if self.enable_contradiction_detection:
            contradictions = self._detect_contradictions(prioritized)
            if contradictions:
                logger.warning("Detected %d contradictions in responses", len(contradictions))
        else:
            contradictions = []
        
        # Step 4: Generate summary
        summary = self._generate_summary(prioritized, query, contradictions)
        
        # Step 5: Extract citations
        citations = self._extract_citations(prioritized)
        
        # Step 6: Prepare detailed results
        details = self._prepare_details(prioritized, contradictions)
        
        result = CompilationResult(
            summary=summary,
            details=details,
            citations=citations,
            metadata={
                "query": query,
                "agents_consulted": len(responses),
                "total_results": sum(len(r.get("results", [])) for r in responses),
                "contradictions_found": len(contradictions)
            }
        )
        
        logger.info("Compilation complete. Summary length: %d chars", len(summary))
        return result
    
    def _deduplicate_responses(self, responses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove duplicate information from responses.
        
        Args:
            responses: List of response dictionaries
            
        Returns:
            Deduplicated list of responses
        """
        deduplicated = []
        seen_content: Set[str] = set()
        
        for response in responses:
            agent = response.get("agent", "Unknown")
            results = response.get("results", [])
            
            unique_results = []
            for result in results:
                # Create a content hash for deduplication
                content_key = self._create_content_key(result)
                if content_key not in seen_content:
                    seen_content.add(content_key)
                    unique_results.append(result)
                else:
                    logger.debug("Duplicate content detected from %s", agent)
            
            if unique_results:
                deduplicated.append({
                    "agent": agent,
                    "results": unique_results
                })
        
        logger.info("Deduplication: %d -> %d unique results", 
                   sum(len(r.get("results", [])) for r in responses),
                   sum(len(r.get("results", [])) for r in deduplicated))
        return deduplicated
    
    def _create_content_key(self, result: Dict[str, Any]) -> str:
        """
        Create a unique key for a result to enable deduplication.
        
        Args:
            result: Result dictionary
            
        Returns:
            String key representing the content
        """
        key_parts = []
        
        if isinstance(result, dict):
            for key in sorted(result.keys()):
                if key not in ["timestamp", "id", "metadata"]:
                    key_parts.append(f"{key}:{result[key]}")
        else:
            key_parts.append(str(result))
        
        return "|".join(key_parts)
    
    def _prioritize_responses(self, responses: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """
        Prioritize responses based on relevance to query.
        
        Args:
            responses: List of deduplicated responses
            query: Original user query
            
        Returns:
            Prioritized list of responses
        """
        query_keywords = set(query.lower().split())
        
        scored_responses = []
        for response in responses:
            agent = response.get("agent", "Unknown")
            results = response.get("results", [])
            
            # Calculate relevance score for each result
            scored_results = []
            for result in results:
                score = self._calculate_relevance_score(result, query_keywords)
                scored_results.append((score, result))
            
            # Sort results by relevance score (descending)
            scored_results.sort(key=lambda x: x[0], reverse=True)
            
            scored_responses.append({
                "agent": agent,
                "results": [r[1] for r in scored_results],
                "relevance_scores": [r[0] for r in scored_results]
            })
        
        # Sort agents by their highest relevance score
        scored_responses.sort(
            key=lambda x: max(x["relevance_scores"]) if x["relevance_scores"] else 0,
            reverse=True
        )
        
        logger.info("Prioritization complete")
        return scored_responses
    
    def _calculate_relevance_score(self, result: Dict[str, Any], query_keywords: Set[str]) -> float:
        """
        Calculate relevance score for a result based on query keywords.
        
        Args:
            result: Result dictionary
            query_keywords: Set of keywords from the query
            
        Returns:
            Relevance score (0-1)
        """
        if not isinstance(result, dict):
            result_text = str(result).lower()
        else:
            result_text = " ".join(str(v).lower() for v in result.values())
        
        result_words = set(result_text.split())
        
        # Calculate overlap between query and result
        overlap = len(query_keywords.intersection(result_words))
        
        if len(query_keywords) == 0:
            return 0.0
        
        return overlap / len(query_keywords)
    
    def _detect_contradictions(self, responses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect contradictions between responses from different agents.
        
        Args:
            responses: List of prioritized responses
            
        Returns:
            List of detected contradictions
        """
        contradictions = []
        
        # TODO: Implement sophisticated contradiction detection
        # For now, this is a placeholder that could be extended with:
        # - Semantic similarity to find related statements
        # - Logical reasoning to identify conflicting information
        # - Temporal inconsistencies
        # - Numerical discrepancies
        
        # Simple heuristic: Check for conflicting values in common fields
        field_values = defaultdict(list)
        
        for response in responses:
            agent = response.get("agent", "Unknown")
            results = response.get("results", [])
            
            for result in results:
                if isinstance(result, dict):
                    for key, value in result.items():
                        field_values[key].append({
                            "agent": agent,
                            "value": value
                        })
        
        # Check for contradictions in each field
        for field, values in field_values.items():
            if len(values) > 1:
                unique_values = set(str(v["value"]) for v in values)
                if len(unique_values) > 1:
                    contradictions.append({
                        "field": field,
                        "conflicting_values": values,
                        "severity": "medium"
                    })
        
        return contradictions
    
    def _generate_summary(self, responses: List[Dict[str, Any]], query: str, 
                         contradictions: List[Dict[str, Any]]) -> str:
        """
        Generate a concise summary of the compiled information.
        
        Args:
            responses: List of prioritized responses
            query: Original user query
            contradictions: List of detected contradictions
            
        Returns:
            Summary string
        """
        summary_parts = []
        
        # Introduction
        agent_names = [r.get("agent", "Unknown") for r in responses]
        summary_parts.append(
            f"Based on information from {', '.join(agent_names)} systems:"
        )
        
        # Add key findings from each agent
        for response in responses[:3]:  # Limit to top 3 agents for conciseness
            agent = response.get("agent", "Unknown")
            results = response.get("results", [])
            
            if results:
                first_result = results[0]
                if isinstance(first_result, dict):
                    result_summary = self._format_result_summary(first_result)
                    summary_parts.append(f"• {agent}: {result_summary}")
        
        # Add contradiction warning if any
        if contradictions:
            summary_parts.append(
                f"\n⚠️ Note: {len(contradictions)} potential contradiction(s) detected. "
                "Please review the detailed results."
            )
        
        summary = "\n".join(summary_parts)
        
        # Truncate if too long
        if len(summary) > self.max_summary_length:
            summary = summary[:self.max_summary_length - 3] + "..."
        
        return summary
    
    def _format_result_summary(self, result: Dict[str, Any]) -> str:
        """Format a result dictionary into a readable summary string."""
        important_fields = ["description", "summary", "title", "status", "value", "result"]
        
        for field in important_fields:
            if field in result:
                return str(result[field])
        
        if result:
            first_key = list(result.keys())[0]
            return f"{first_key}: {result[first_key]}"
        
        return "No details available"
    
    def _extract_citations(self, responses: List[Dict[str, Any]]) -> List[str]:
        """Extract citations showing which agents provided information."""
        citations = []
        
        for response in responses:
            agent = response.get("agent", "Unknown")
            results = response.get("results", [])
            
            if results:
                citations.append(f"{agent} Agent ({len(results)} result(s))")
        
        return citations
    
    def _prepare_details(self, responses: List[Dict[str, Any]], 
                        contradictions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prepare detailed results for output."""
        details = []
        
        # Add all results from each agent
        for response in responses:
            agent = response.get("agent", "Unknown")
            results = response.get("results", [])
            relevance_scores = response.get("relevance_scores", [])
            
            for idx, result in enumerate(results):
                detail = {
                    "source_agent": agent,
                    "content": result,
                    "relevance_score": relevance_scores[idx] if idx < len(relevance_scores) else 0.0
                }
                details.append(detail)
        
        # Add contradictions as separate entries if any
        if contradictions:
            details.append({
                "source_agent": "Compiler",
                "content": {
                    "type": "contradictions",
                    "items": contradictions
                },
                "relevance_score": 1.0
            })
        
        return details


# Factory function
def create_compiler(config: Optional[Dict[str, Any]] = None) -> Compiler:
    """
    Factory function to create a Compiler instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Compiler instance
    """
    return Compiler(config)


# Alias for backward compatibility
CompilerAgent = Compiler


# Main entry point for testing
if __name__ == "__main__":
    import json
    
    # Example usage
    compiler = create_compiler()
    
    # Mock responses from sub-agents
    mock_responses = [
        {
            "agent": "LIMS",
            "results": [
                {
                    "lot_number": "LOT-12345",
                    "test": "Assay",
                    "result": "98.5%",
                    "specification": "95.0-105.0%",
                    "status": "PASS"
                },
                {
                    "lot_number": "LOT-12345",
                    "test": "Dissolution",
                    "result": "92%",
                    "specification": "≥85%",
                    "status": "PASS"
                }
            ]
        },
        {
            "agent": "ERP",
            "results": [
                {
                    "batch_number": "BATCH-12345",
                    "manufacturing_date": "2024-01-15",
                    "status": "Released",
                    "grn_number": "GRN-2024-001"
                }
            ]
        },
        {
            "agent": "DMS",
            "results": [
                {
                    "document_id": "SOP-QC-001",
                    "title": "Quality Control Testing Procedure",
                    "version": "2.0",
                    "status": "Active"
                }
            ]
        }
    ]
    
    # Test compilation
    query = "What are the test results for LOT-12345?"
    result = compiler.compile(query, mock_responses)
    
    print("="*80)
    print("COMPILATION RESULT")
    print("="*80)
    print("\nSUMMARY:")
    print(result.summary)
    print("\nCITATIONS:")
    for citation in result.citations:
        print(f"  - {citation}")
    print(f"\nDETAILS ({len(result.details)} items):")
    print(json.dumps(result.details, indent=2))
    print("\nMETADATA:")
    print(json.dumps(result.metadata, indent=2))

