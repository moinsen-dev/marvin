"""Agent for analyzing Product Requirements Documents (PRDs)."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from marvin.core.agents.base import Agent
from marvin.core.domain.models import Feature, PRD


class DocumentAnalysisAgent(Agent):
    """Agent for analyzing PRDs and extracting features and requirements."""
    
    def __init__(self, name: str = "document_analysis", config: Optional[Dict[str, Any]] = None):
        """Initializes the DocumentAnalysisAgent.
        
        Args:
            name: Name of the agent
            config: Configuration of the agent
        """
        super().__init__(name, config)
    
    async def execute(
        self, document_path: str, **kwargs: Any
    ) -> Tuple[PRD, List[Feature]]:
        """Analyzes a PRD and extracts features and requirements.
        
        Args:
            document_path: Path to the PRD document
            **kwargs: Additional parameters
            
        Returns:
            Tuple of PRD and extracted features
        
        Raises:
            FileNotFoundError: If the document was not found
            ValueError: If the document does not have a supported format
        """
        if not os.path.exists(document_path):
            raise FileNotFoundError(f"Document not found: {document_path}")
        
        # Determine file type
        file_ext = Path(document_path).suffix.lower()
        
        if file_ext == ".md":
            return await self._analyze_markdown(document_path, **kwargs)
        elif file_ext in [".docx", ".doc"]:
            return await self._analyze_word(document_path, **kwargs)
        elif file_ext == ".pdf":
            return await self._analyze_pdf(document_path, **kwargs)
        else:
            raise ValueError(
                f"Unsupported document format: {file_ext}. "
                "Supported formats: .md, .docx, .doc, .pdf"
            )
    
    async def _analyze_markdown(
        self, document_path: str, **kwargs: Any
    ) -> Tuple[PRD, List[Feature]]:
        """Analyzes a Markdown PRD.
        
        Args:
            document_path: Path to the Markdown document
            **kwargs: Additional parameters
            
        Returns:
            Tuple of PRD and extracted features
        """
        # Here the actual analysis would take place with Google ADK
        # For now, we implement a simple placeholder
        
        # Read document
        with open(document_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract metadata (simplified)
        title = "Unknown PRD"
        version = "1.0"
        author = "Unknown"
        
        # Use first heading as title, if available
        import re
        title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
        
        # Simple feature extraction example
        # In the complete implementation, we would use Google ADK here
        features = []
        feature_blocks = re.findall(
            r"^## (.+?)$(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL
        )
        
        for i, (feature_title, feature_content) in enumerate(feature_blocks):
            if "overview" in feature_title.lower() or "übersicht" in feature_title.lower():
                continue  # Skip overview chapter
            
            feature = Feature(
                id=f"feature_{i:02d}",
                name=feature_title.strip(),
                description=feature_content.strip(),
                requirements=[],
                dependencies=[],
            )
            
            # Extract requirements
            req_matches = re.findall(
                r"^\s*[-*]\s*(.+)$", feature_content, re.MULTILINE
            )
            feature.requirements = [req.strip() for req in req_matches]
            
            features.append(feature)
        
        prd = PRD(
            id=os.path.basename(document_path).split(".")[0],
            title=title,
            description="",  # Here could be a summary
            author=author,
            created_at=kwargs.get("created_at"),
            updated_at=kwargs.get("updated_at"),
            version=version,
            features=features,
        )
        
        return prd, features
    
    async def _analyze_word(
        self, document_path: str, **kwargs: Any
    ) -> Tuple[PRD, List[Feature]]:
        """Analyzes a Word PRD.
        
        Args:
            document_path: Path to the Word document
            **kwargs: Additional parameters
            
        Returns:
            Tuple of PRD and extracted features
        """
        # Implementation for Word documents
        # This would use python-docx or other libraries
        raise NotImplementedError("Word document analysis is not yet implemented")
    
    async def _analyze_pdf(
        self, document_path: str, **kwargs: Any
    ) -> Tuple[PRD, List[Feature]]:
        """Analyzes a PDF PRD.
        
        Args:
            document_path: Path to the PDF document
            **kwargs: Additional parameters
            
        Returns:
            Tuple of PRD and extracted features
        """
        # Implementation for PDF documents
        # This would use PyPDF2, pdfplumber, or other libraries
        raise NotImplementedError("PDF document analysis is not yet implemented")
