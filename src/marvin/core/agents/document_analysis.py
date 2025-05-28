"""Agent for analyzing Product Requirements Documents (PRDs)."""

import os
import re
import time
from pathlib import Path
from typing import Any

from marvin.core.agents.base import Agent
from marvin.core.domain.models import PRD, Feature


class DocumentAnalysisAgent(Agent):
    """Agent for analyzing PRDs and extracting features and requirements."""

    def __init__(
        self, name: str = "document_analysis", config: dict[str, Any] | None = None
    ):
        """Initializes the DocumentAnalysisAgent.

        Args:
            name: Name of the agent
            config: Configuration of the agent
        """
        super().__init__(name, config)

    async def execute(
        self, document_path: str, **kwargs: Any
    ) -> tuple[PRD, list[Feature]]:
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
        self.logger.info(f"Starting document analysis for: {document_path}")

        if not os.path.exists(document_path):
            self.logger.error(f"Document not found: {document_path}")
            raise FileNotFoundError(f"Document not found: {document_path}")

        # Determine file type
        file_ext = Path(document_path).suffix.lower()
        self.logger.debug(f"Detected document format: {file_ext}")

        start_time = time.time()
        try:
            if file_ext == ".md":
                self.logger.info("Processing Markdown document")
                result = await self._analyze_markdown(document_path, **kwargs)
            elif file_ext in [".docx", ".doc"]:
                self.logger.info("Processing Word document")
                result = await self._analyze_word(document_path, **kwargs)
            elif file_ext == ".pdf":
                self.logger.info("Processing PDF document")
                result = await self._analyze_pdf(document_path, **kwargs)
            else:
                error_msg = f"Unsupported document format: {file_ext}. Supported formats: .md, .docx, .doc, .pdf"
                self.logger.error(error_msg)
                raise ValueError(error_msg)

            elapsed_time = time.time() - start_time
            prd, features = result
            self.logger.info(f"Document analysis completed in {elapsed_time:.2f}s")
            self.logger.debug(
                f"Extracted PRD: {prd.title} with {len(features)} features"
            )

            for i, feature in enumerate(features):
                self.logger.debug(
                    f"Feature {i + 1}: {feature.name} with {len(feature.requirements)} requirements"
                )

            return result
        except Exception as e:
            elapsed_time = time.time() - start_time
            self.logger.error(
                f"Error analyzing document after {elapsed_time:.2f}s: {str(e)}"
            )
            raise

    async def _analyze_markdown(
        self, document_path: str, **kwargs: Any
    ) -> tuple[PRD, list[Feature]]:
        """Analyzes a Markdown PRD.

        Args:
            document_path: Path to the Markdown document
            **kwargs: Additional parameters

        Returns:
            Tuple of PRD and extracted features
        """
        self.logger.debug(f"Reading Markdown content from {document_path}")

        # Read document
        try:
            with open(document_path, encoding="utf-8") as f:
                content = f.read()
            self.logger.debug(f"Read {len(content)} bytes from document")
        except Exception as e:
            self.logger.error(f"Error reading Markdown file: {str(e)}")
            raise

        # Extract metadata (simplified)
        title = "Unknown PRD"
        version = "1.0"
        author = "Unknown"

        # Use first heading as title, if available
        title_match = re.search(r"^# (.+)$", content, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
            self.logger.debug(f"Extracted title: {title}")
        else:
            self.logger.warning("No title found in document, using default")

        # Simple feature extraction example
        # In the complete implementation, we would use Google ADK here
        features = []
        self.logger.debug("Extracting feature blocks")
        feature_blocks = re.findall(
            r"^## (.+?)$(.*?)(?=^## |\Z)", content, re.MULTILINE | re.DOTALL
        )
        self.logger.debug(f"Found {len(feature_blocks)} feature blocks")

        for i, (feature_title, feature_content) in enumerate(feature_blocks):
            if (
                "overview" in feature_title.lower()
                or "übersicht" in feature_title.lower()
            ):
                self.logger.debug(f"Skipping overview section: {feature_title}")
                continue  # Skip overview chapter

            self.logger.debug(f"Processing feature: {feature_title}")
            feature = Feature(
                id=f"feature_{i:02d}",
                name=feature_title.strip(),
                description=feature_content.strip(),
                requirements=[],
                dependencies=[],
            )

            # Extract requirements
            req_matches = re.findall(r"^\s*[-*]\s*(.+)$", feature_content, re.MULTILINE)
            feature.requirements = [req.strip() for req in req_matches]
            self.logger.debug(
                f"Extracted {len(feature.requirements)} requirements for {feature.name}"
            )

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

        self.logger.info(
            f"Markdown analysis complete: {prd.title} with {len(features)} features"
        )
        return prd, features

    async def _analyze_word(
        self, document_path: str, **kwargs: Any
    ) -> tuple[PRD, list[Feature]]:
        """Analyzes a Word PRD.

        Args:
            document_path: Path to the Word document
            **kwargs: Additional parameters

        Returns:
            Tuple of PRD and extracted features
        """
        # Implementation for Word documents
        # This would use python-docx or other libraries
        self.logger.warning("Word document analysis is not yet implemented")
        raise NotImplementedError("Word document analysis is not yet implemented")

    async def _analyze_pdf(
        self, document_path: str, **kwargs: Any
    ) -> tuple[PRD, list[Feature]]:
        """Analyzes a PDF PRD.

        Args:
            document_path: Path to the PDF document
            **kwargs: Additional parameters

        Returns:
            Tuple of PRD and extracted features
        """
        # Implementation for PDF documents
        # This would use PyPDF2, pdfplumber, or other libraries
        self.logger.warning("PDF document analysis is not yet implemented")
        raise NotImplementedError("PDF document analysis is not yet implemented")
