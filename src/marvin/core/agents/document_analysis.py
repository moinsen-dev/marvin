"""Agent for analyzing Product Requirements Documents (PRDs)."""

import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from marvin.core.agents.base import Agent
from marvin.core.domain.models import PRD, Feature, FeatureStatus


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

        # Extract metadata
        title = self._extract_title(content)
        version = self._extract_version(content)
        author = self._extract_author(content)
        description = self._extract_description(content)

        # Create PRD
        created_at = kwargs.get("created_at", datetime.now())
        updated_at = kwargs.get("updated_at", datetime.now())

        prd = PRD(
            id=Path(document_path).stem,
            title=title,
            description=description,
            author=author,
            created_at=created_at,
            updated_at=updated_at,
            version=version,
        )

        # Extract features
        features = self._extract_features(content)

        self.logger.info(
            f"Markdown analysis complete: {prd.title} with {len(features)} features"
        )
        return prd, features

    def _extract_title(self, content: str) -> str:
        """Extract title from markdown content."""
        # Try multiple patterns for title
        patterns = [
            r"^#\s+Product Requirements Document:\s*(.+)$",
            r"^#\s+PRD:\s*(.+)$",
            r"^#\s+(.+?)(?:\s*\n|$)",  # Any H1 heading
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.MULTILINE)
            if match:
                title = match.group(1).strip()
                # Remove trailing colons
                if title.endswith(":"):
                    title = title[:-1].strip()
                return title

        return "Unknown PRD"

    def _extract_version(self, content: str) -> str:
        """Extract version from markdown content."""
        match = re.search(r"Version:\s*(\S+)", content, re.IGNORECASE)
        return match.group(1) if match else "0.0.0"

    def _extract_author(self, content: str) -> str:
        """Extract author from markdown content."""
        match = re.search(r"Author:\s*(.+?)(?:\n|$)", content, re.IGNORECASE)
        return match.group(1).strip() if match else "Unknown"

    def _extract_description(self, content: str) -> str:
        """Extract description from overview/summary section."""
        # Look for overview or executive summary sections
        patterns = [
            r"##\s+(?:Executive\s+)?Overview\s*\n+((?:(?!^#).*\n)*)",
            r"##\s+Executive\s+Summary\s*\n+((?:(?!^#).*\n)*)",
            r"##\s+(?:Project\s+)?Description\s*\n+((?:(?!^#).*\n)*)",
        ]

        for pattern in patterns:
            match = re.search(pattern, content, re.MULTILINE | re.IGNORECASE)
            if match:
                desc_text = match.group(1).strip()
                # Clean up the description
                desc_lines = [
                    line.strip() for line in desc_text.split("\n") if line.strip()
                ]
                return " ".join(desc_lines)

        return ""

    def _extract_features(self, content: str) -> list[Feature]:
        """Extract features from markdown content."""
        features: list[Feature] = []

        # Find features section
        features_match = re.search(
            r"##\s+Features?\s*\n(.*?)(?=^##\s|\Z)",
            content,
            re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )

        if not features_match:
            self.logger.debug("No features section found in content")
            return features

        features_content = features_match.group(1)
        self.logger.debug(f"Found features section with {len(features_content)} chars")

        # Extract individual features (### headings only, not #### or deeper)
        # More flexible pattern to catch different feature formats
        # Only capture ### headings (exactly 3 #s)
        feature_pattern = (
            r"^###\s+((?:Feature\s*\d+:?\s*)?(?:\d+\.\s*)?)?(.+?)\n(.*?)(?=^###\s|\Z)"
        )
        feature_matches = list(
            re.finditer(feature_pattern, features_content, re.MULTILINE | re.DOTALL)
        )

        self.logger.debug(f"Found {len(feature_matches)} feature matches")

        for i, match in enumerate(feature_matches):
            # Group 1: optional prefix (e.g., "Feature 1:", "1.")
            # Group 2: feature name
            # Group 3: feature content
            prefix = match.group(1) or ""
            raw_name = match.group(2).strip()

            # Check if we have a "Feature X:" pattern to remove
            if prefix and "feature" in prefix.lower():
                # Just use the name part after "Feature X:"
                feature_name = raw_name
            else:
                # Keep the prefix (like "1. ")
                feature_name = (prefix + raw_name).strip()

            # Remove trailing colons from feature name
            if feature_name.endswith(":"):
                feature_name = feature_name[:-1].strip()

            feature_content = match.group(3).strip()
            self.logger.debug(
                f"Feature content for '{feature_name}': {feature_content[:100]}..."
            )

            # Generate feature ID from name
            feature_id = self._generate_feature_id(feature_name, i)

            # Extract description (first paragraph or sentences before any subsection)
            desc_lines: list[str] = []
            for line in feature_content.split("\n"):
                line = line.strip()
                if not line:
                    if desc_lines:  # Stop at first empty line after content
                        break
                    continue
                if line.startswith(("**", "####", "-", "*")) or (
                    line.endswith(":") and len(line) < 30
                ):
                    break
                desc_lines.append(line)
            description = " ".join(desc_lines)

            # Extract requirements
            self.logger.debug(
                f"Extracting requirements from: {feature_content[:100]}..."
            )
            requirements = self._extract_requirements(feature_content)

            # Extract dependencies
            dependencies = self._extract_dependencies(feature_content)

            # Extract priority
            priority = self._extract_priority(feature_content)

            # Create feature
            feature = Feature(
                id=feature_id,
                name=feature_name,
                description=description,
                requirements=requirements,
                dependencies=dependencies,
                priority=priority,
                status=FeatureStatus.PROPOSED,
            )

            features.append(feature)

        return features

    def _generate_feature_id(self, feature_name: str, index: int) -> str:
        """Generate a unique feature ID from the feature name."""
        # Create slug from feature name
        slug = feature_name.lower()
        slug = re.sub(r"[^a-z0-9\s-]", "", slug)
        slug = re.sub(r"\s+", "_", slug)
        slug = slug.strip("_")

        # Add index to ensure uniqueness
        return f"{slug}_{index:02d}"

    def _extract_requirements(self, feature_content: str) -> list[str]:
        """Extract requirements from feature content."""
        requirements = []

        # Look for requirements section
        req_match = re.search(
            r"\*\*Requirements?:\*\*\s*\n(.*?)(?=\*\*|\n\n|$)",
            feature_content,
            re.DOTALL | re.IGNORECASE,
        )

        if req_match:
            req_text = req_match.group(1)
            self.logger.debug(f"Found requirements text: {req_text[:50]}...")
            # Extract bullet points
            req_pattern = r"[-*]\s+(?:REQ-\d+(?:\.\d+)?:\s+)?(.+?)(?=\n[-*]|\n\n|$)"
            for match in re.finditer(req_pattern, req_text, re.MULTILINE):
                req_item = match.group(1).strip()
                requirements.append(req_item)
                self.logger.debug(f"Extracted requirement: {req_item}")

        # Also check for numbered requirements in subsections (#### headings)
        subsection_pattern = r"####\s+\d+\.\d+\s+(.+?)\n(.*?)\*\*Requirements?:\*\*\s*\n(.*?)(?=####|\*\*|###|\Z)"
        for match in re.finditer(
            subsection_pattern, feature_content, re.DOTALL | re.IGNORECASE
        ):
            subsection_reqs = match.group(3)
            self.logger.debug(
                f"Found subsection requirements: {subsection_reqs[:50]}..."
            )
            req_pattern = r"[-*]\s+(?:REQ-\d+(?:\.\d+)?:\s+)?(.+?)(?=\n[-*]|\n\n|$)"
            for req_match in re.finditer(req_pattern, subsection_reqs, re.MULTILINE):
                req_item = req_match.group(1).strip()
                requirements.append(req_item)
                self.logger.debug(f"Extracted subsection requirement: {req_item}")

        return requirements

    def _extract_dependencies(self, feature_content: str) -> list[str]:
        """Extract dependencies from feature content."""
        dependencies = []

        # Look for dependencies line
        dep_match = re.search(
            r"\*\*Dependencies?:\*\*\s*(.+?)(?=\n|$)", feature_content, re.IGNORECASE
        )

        if dep_match:
            dep_text = dep_match.group(1).strip()
            # Split by comma and clean up
            deps = [d.strip() for d in dep_text.split(",")]
            dependencies = [d for d in deps if d and d.lower() != "none"]

        return dependencies

    def _extract_priority(self, feature_content: str) -> int:
        """Extract priority from feature content."""
        # Look for priority indication
        priority_match = re.search(
            r"\*\*Priority:\*\*\s*(.+?)(?=\n|$)", feature_content, re.IGNORECASE
        )

        if priority_match:
            priority_text = priority_match.group(1).strip().lower()

            # Map priority text to numbers
            if "high" in priority_text or "p0" in priority_text:
                return 0
            elif "medium" in priority_text or "p1" in priority_text:
                return 1
            elif "low" in priority_text or "p2" in priority_text:
                return 2

        return 0  # Default to high priority

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
        # This would use PyPDF2 or pdfplumber
        self.logger.warning("PDF document analysis is not yet implemented")
        raise NotImplementedError("PDF document analysis is not yet implemented")
