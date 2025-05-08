"""Agent zur Analyse von Produktanforderungsdokumenten (PRDs)."""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from marvin.core.agents.base import Agent
from marvin.core.domain.models import Feature, PRD


class DocumentAnalysisAgent(Agent):
    """Agent zur Analyse von PRDs und Extraktion von Features und Anforderungen."""
    
    def __init__(self, name: str = "document_analysis", config: Optional[Dict[str, Any]] = None):
        """Initialisiert den DocumentAnalysisAgent.
        
        Args:
            name: Name des Agenten
            config: Konfiguration des Agenten
        """
        super().__init__(name, config)
    
    async def execute(
        self, document_path: str, **kwargs: Any
    ) -> Tuple[PRD, List[Feature]]:
        """Analysiert ein PRD und extrahiert Features und Anforderungen.
        
        Args:
            document_path: Pfad zum PRD-Dokument
            **kwargs: Weitere Parameter
            
        Returns:
            Tuple aus PRD und extrahierten Features
        
        Raises:
            FileNotFoundError: Wenn das Dokument nicht gefunden wurde
            ValueError: Wenn das Dokument kein unterstütztes Format hat
        """
        if not os.path.exists(document_path):
            raise FileNotFoundError(f"Dokument nicht gefunden: {document_path}")
        
        # Dateityp bestimmen
        file_ext = Path(document_path).suffix.lower()
        
        if file_ext == ".md":
            return await self._analyze_markdown(document_path, **kwargs)
        elif file_ext in [".docx", ".doc"]:
            return await self._analyze_word(document_path, **kwargs)
        elif file_ext == ".pdf":
            return await self._analyze_pdf(document_path, **kwargs)
        else:
            raise ValueError(
                f"Nicht unterstütztes Dokumentformat: {file_ext}. "
                "Unterstützte Formate: .md, .docx, .doc, .pdf"
            )
    
    async def _analyze_markdown(
        self, document_path: str, **kwargs: Any
    ) -> Tuple[PRD, List[Feature]]:
        """Analysiert ein Markdown-PRD.
        
        Args:
            document_path: Pfad zum Markdown-Dokument
            **kwargs: Weitere Parameter
            
        Returns:
            Tuple aus PRD und extrahierten Features
        """
        # Hier würde die eigentliche Analyse mit Google ADK stattfinden
        # Für jetzt implementieren wir einen einfachen Platzhalter
        
        # Dokument lesen
        with open(document_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Metadaten extrahieren (vereinfacht)
        title = "Unbekanntes PRD"
        version = "1.0"
        author = "Unbekannt"
        
        # Erste Überschrift als Titel verwenden, falls vorhanden
        import re
        title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
        
        # Einfaches Feature-Extraktionsbeispiel
        # In der vollständigen Implementierung würden wir hier Google ADK verwenden
        features = []
        feature_blocks = re.findall(
            r"^## (.+?)$(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL
        )
        
        for i, (feature_title, feature_content) in enumerate(feature_blocks):
            if "overview" in feature_title.lower() or "übersicht" in feature_title.lower():
                continue  # Übersichtskapitel überspringen
            
            feature = Feature(
                id=f"feature_{i:02d}",
                name=feature_title.strip(),
                description=feature_content.strip(),
                requirements=[],
                dependencies=[],
            )
            
            # Anforderungen extrahieren
            req_matches = re.findall(
                r"^\s*[-*]\s*(.+)$", feature_content, re.MULTILINE
            )
            feature.requirements = [req.strip() for req in req_matches]
            
            features.append(feature)
        
        prd = PRD(
            id=os.path.basename(document_path).split(".")[0],
            title=title,
            description="",  # Hier könnte eine Zusammenfassung stehen
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
        """Analysiert ein Word-PRD.
        
        Args:
            document_path: Pfad zum Word-Dokument
            **kwargs: Weitere Parameter
            
        Returns:
            Tuple aus PRD und extrahierten Features
        """
        # Implementierung für Word-Dokumente
        # Dies würde python-docx oder andere Bibliotheken verwenden
        raise NotImplementedError("Word-Dokument-Analyse ist noch nicht implementiert")
    
    async def _analyze_pdf(
        self, document_path: str, **kwargs: Any
    ) -> Tuple[PRD, List[Feature]]:
        """Analysiert ein PDF-PRD.
        
        Args:
            document_path: Pfad zum PDF-Dokument
            **kwargs: Weitere Parameter
            
        Returns:
            Tuple aus PRD und extrahierten Features
        """
        # Implementierung für PDF-Dokumente
        # Dies würde PyPDF2, pdfplumber oder andere Bibliotheken verwenden
        raise NotImplementedError("PDF-Dokument-Analyse ist noch nicht implementiert")
