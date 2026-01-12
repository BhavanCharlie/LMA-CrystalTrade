"""
Evidence Log System
Unified system for tracking citations and evidence across all features
"""
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid


class EvidenceLogService:
    def __init__(self):
        pass

    async def log_evidence(
        self,
        analysis_id: str,
        document_id: str,
        document_name: str,
        extraction_text: str,
        extraction_confidence: float,
        feature_type: str,
        feature_id: str,
        page_number: Optional[int] = None,
        section: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Log evidence with citation"""
        evidence_id = str(uuid.uuid4())
        
        return {
            "id": evidence_id,
            "analysis_id": analysis_id,
            "document_id": document_id,
            "document_name": document_name,
            "page_number": page_number,
            "section": section,
            "extraction_text": extraction_text,
            "extraction_confidence": extraction_confidence,
            "feature_type": feature_type,
            "feature_id": feature_id,
            "created_at": datetime.utcnow().isoformat(),
        }

    async def get_evidence_for_feature(
        self, feature_type: str, feature_id: str, evidence_logs: List[Dict]
    ) -> List[Dict]:
        """Get evidence for a specific feature"""
        return [
            log
            for log in evidence_logs
            if log.get("feature_type") == feature_type and log.get("feature_id") == feature_id
        ]

    def format_citation(self, evidence: Dict) -> str:
        """Format evidence as citation string"""
        parts = []
        
        if evidence.get("document_name"):
            parts.append(f"Document: {evidence.get('document_name')}")
        
        if evidence.get("page_number"):
            parts.append(f"Page {evidence.get('page_number')}")
        
        if evidence.get("section"):
            parts.append(f"Section: {evidence.get('section')}")
        
        confidence = evidence.get("extraction_confidence", 0.0)
        if confidence < 0.8:
            parts.append(f"(Confidence: {confidence*100:.0f}%)")
        
        return " | ".join(parts) if parts else "Citation not available"

    async def create_evidence_links(
        self, analysis_id: str, document_id: str, document_name: str, evidence_data: List[Dict]
    ) -> List[Dict]:
        """Create evidence links from evidence data"""
        evidence_links = []
        
        for evidence in evidence_data:
            link = await self.log_evidence(
                analysis_id=analysis_id,
                document_id=document_id,
                document_name=document_name,
                extraction_text=evidence.get("text", ""),
                extraction_confidence=evidence.get("confidence", 0.8),
                feature_type=evidence.get("feature_type", "general"),
                feature_id=evidence.get("feature_id", ""),
                page_number=evidence.get("page_number"),
                section=evidence.get("section"),
            )
            evidence_links.append(link)
        
        return evidence_links

