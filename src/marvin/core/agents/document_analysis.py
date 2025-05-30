"""Agent for analyzing Product Requirements Documents (PRDs)."""

import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import frontmatter
    from markdown_it import MarkdownIt
    from mdit_py_plugins.front_matter import front_matter_plugin
    from mdit_py_plugins.tasklists import tasklists_plugin
    ENHANCED_PARSING_AVAILABLE = True
except ImportError:
    ENHANCED_PARSING_AVAILABLE = False

from marvin.core.agents.base import Agent
from marvin.core.domain.models import PRD, Feature, FeatureStatus, UserStory


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

        # Use enhanced parsing if available
        if ENHANCED_PARSING_AVAILABLE:
            return self._analyze_markdown_enhanced(content, document_path, **kwargs)
        else:
            # Fall back to basic parsing
            return self._analyze_markdown_basic(content, document_path, **kwargs)

    def _analyze_markdown_enhanced(self, content: str, document_path: str, **kwargs: Any) -> tuple[PRD, list[Feature]]:
        """Enhanced markdown analysis with frontmatter, tables, and advanced parsing."""
        try:
            # Parse frontmatter
            post = frontmatter.loads(content)
            frontmatter_data = post.metadata
            markdown_content = post.content

            # Initialize markdown parser with plugins
            md = MarkdownIt("commonmark", {"breaks": True, "html": True})
            md.use(front_matter_plugin)
            md.use(tasklists_plugin)

            # Parse markdown into tokens
            tokens = md.parse(markdown_content)

            # Extract metadata with enhanced support
            metadata = self._extract_enhanced_metadata(frontmatter_data, markdown_content)
            title = metadata.get('title') or self._extract_title(markdown_content)
            version = metadata.get('version') or self._extract_version(markdown_content)
            author = metadata.get('author') or self._extract_author(markdown_content)
            description = self._extract_description(markdown_content)

            # Create PRD with metadata
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
                metadata=metadata,
            )

            # Extract features with enhanced parsing
            features = self._extract_features_enhanced(tokens, markdown_content)

            # Generate dependency graph
            prd.dependency_graph = self._generate_dependency_graph(features)

            self.logger.info(
                f"Enhanced markdown analysis complete: {prd.title} with {len(features)} features"
            )
            return prd, features

        except Exception as e:
            self.logger.warning(f"Enhanced parsing failed, falling back to basic: {e}")
            return self._analyze_markdown_basic(content, document_path, **kwargs)

    def _analyze_markdown_basic(self, content: str, document_path: str, **kwargs: Any) -> tuple[PRD, list[Feature]]:
        """Basic markdown analysis (original implementation)."""
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
                title=feature_name,
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

    def _extract_enhanced_metadata(self, frontmatter_data: dict[str, Any], content: str) -> dict[str, Any]:
        """Extract metadata from frontmatter and content."""
        metadata = frontmatter_data.copy()

        # Extract additional metadata from content if not in frontmatter
        if 'title' not in metadata:
            metadata['title'] = self._extract_title(content)
        if 'version' not in metadata:
            metadata['version'] = self._extract_version(content)
        if 'author' not in metadata:
            metadata['author'] = self._extract_author(content)

        return metadata

    def _extract_features_enhanced(self, tokens: list, content: str) -> list[Feature]:
        """Extract features using enhanced parsing with tokens and advanced patterns."""
        features = []

        # First try to extract from tables
        table_features = self._extract_features_from_tables(content)
        features.extend(table_features)

        # Then extract from sections if no table features found
        if not table_features:
            section_features = self._extract_features_from_sections(content)
            features.extend(section_features)

        return features

    def _extract_features_from_tables(self, content: str) -> list[Feature]:
        """Extract features from markdown tables."""
        features = []

        # Find tables with feature information
        table_pattern = r'\|[^|]*Feature[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^\n]*\n\|[-|\s]*\|\n((?:\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^\n]*\n)*)'

        # Alternative pattern for requirement matrices
        simple_table_pattern = r'\|\s*Feature[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^\n]*\n\|[-:\s|]*\n((?:\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^|]*\|[^\n]*\n)*)'

        for pattern in [table_pattern, simple_table_pattern]:
            matches = re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE)

            for match in matches:
                table_content = match.group(1) if match.groups() else match.group(0)
                rows = table_content.strip().split('\n')

                for i, row in enumerate(rows):
                    if row.strip().startswith('|'):
                        cells = [cell.strip() for cell in row.split('|')[1:-1]]  # Remove empty first and last

                        if len(cells) >= 6:  # Feature table format
                            feature_id = cells[0].strip()
                            feature_name = cells[1].strip()
                            priority = cells[2].strip()
                            effort = cells[3].strip()
                            dependencies_str = cells[5].strip() if len(cells) > 5 else ""

                            if feature_name and feature_name != 'Feature Name':
                                dependencies = []
                                if dependencies_str and dependencies_str.lower() not in ['none', '']:
                                    dependencies = [dep.strip() for dep in dependencies_str.split(',')]

                                feature = Feature(
                                    id=feature_id or self._generate_feature_id(feature_name, i),
                                    title=feature_name,
                                    description="Feature extracted from requirements matrix",
                                    priority=priority,
                                    effort=effort,
                                    dependencies=dependencies,
                                    status=FeatureStatus.PROPOSED,
                                )
                                features.append(feature)

        return features

    def _extract_features_from_sections(self, content: str) -> list[Feature]:
        """Extract features from markdown sections with enhanced parsing."""
        features: list[Feature] = []

        # First, find the Features section
        features_match = re.search(
            r"##\s+(?:\d+\.\s*)?Features?\s*\n(.*?)(?=^##\s|\Z)",
            content,
            re.MULTILINE | re.DOTALL | re.IGNORECASE,
        )

        if not features_match:
            self.logger.debug("No features section found in content")
            return features

        features_content = features_match.group(1)

        # Enhanced pattern to capture feature subsections within the Features section
        # Look for ### headings (feature level) within the Features section
        feature_pattern = r'(?:^|\n)###\s+(?:\d+\.?\d*\s+)?([^#\n]+?)(?:\s*\n|$)(.*?)(?=\n###\s|\n##\s|\Z)'

        matches = re.finditer(feature_pattern, features_content, re.MULTILINE | re.DOTALL)

        for i, match in enumerate(matches):
            raw_title = match.group(1).strip()
            feature_content = match.group(2).strip()

            # Clean up feature title - remove prefixes like "Feature 1:", "1.", etc.
            feature_title = raw_title

            # Remove "Feature X:" prefix
            feature_title = re.sub(r'^Feature\s*\d*:\s*', '', feature_title, flags=re.IGNORECASE)

            # Remove numbered prefix like "1.", "2.1", etc.
            feature_title = re.sub(r'^\d+\.?\d*\s+', '', feature_title)

            feature_title = feature_title.strip()

            # Skip if this looks like a non-feature section (shouldn't happen in Features section but just in case)
            if any(keyword in feature_title.lower() for keyword in
                   ['overview', 'introduction', 'background', 'conclusion', 'appendix']):
                continue

            # Extract priority and effort from title or content
            priority_str = self._extract_priority_from_text(f"{feature_title}\n{feature_content}")
            # Convert string priority to integer for backward compatibility
            priority = self._convert_priority_to_int(priority_str)
            effort = self._extract_effort_from_text(f"{feature_title}\n{feature_content}")

            # Extract description
            description = self._extract_feature_description(feature_content)

            # Extract user stories
            user_stories = self._extract_user_stories(feature_content)

            # Extract acceptance criteria
            acceptance_criteria = self._extract_acceptance_criteria(feature_content)

            # Extract definition of done
            definition_of_done = self._extract_definition_of_done(feature_content)

            # Extract requirements
            requirements = self._extract_requirements(feature_content)

            # Extract dependencies
            dependencies = self._extract_dependencies_enhanced(feature_content)

            # Create feature with enhanced data
            feature = Feature(
                id=self._generate_feature_id(feature_title, i),
                title=feature_title,
                description=description,
                priority=priority,  # Already converted to int for compatibility
                effort=effort,
                requirements=requirements,
                dependencies=dependencies,
                user_stories=user_stories,
                acceptance_criteria=acceptance_criteria,
                definition_of_done=definition_of_done,
                status=FeatureStatus.PROPOSED,
            )

            features.append(feature)

        return features

    def _extract_priority_from_text(self, text: str) -> str:
        """Extract priority from text using various patterns."""
        # Priority patterns
        priority_patterns = [
            r'\*\*Priority\*\*:\s*(\w+)',
            r'Priority:\s*(\w+)',
            r'\*\*(\w+)\s+priority\*\*',
            r'(\w+)\s+priority',
            r'priority\s*[:\-]\s*(\w+)',
        ]

        for pattern in priority_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                priority = match.group(1).strip().title()
                if priority in ['High', 'Medium', 'Low', 'Critical', 'Must', 'Should', 'Could']:
                    return priority

        # Natural language priority detection
        text_lower = text.lower()
        if any(word in text_lower for word in ['critical', 'must have', 'high priority']):
            return 'High'
        elif any(word in text_lower for word in ['should have', 'medium priority']):
            return 'Medium'
        elif any(word in text_lower for word in ['could have', 'low priority', 'nice to have']):
            return 'Low'

        return 'Medium'  # Default

    def _convert_priority_to_int(self, priority_str: str) -> int:
        """Convert string priority to integer for backward compatibility."""
        priority_map = {
            'High': 0,
            'Critical': 0,
            'Must Have': 0,
            'Must': 0,
            'Medium': 1,
            'Should Have': 1,
            'Should': 1,
            'Low': 2,
            'Could Have': 2,
            'Could': 2
        }
        return priority_map.get(priority_str, 0)  # Default to high (0)

    def _extract_effort_from_text(self, text: str) -> str | None:
        """Extract effort estimation from text."""
        effort_patterns = [
            r'\*\*Effort\*\*:\s*(\d+\s*(?:SP|story points?|weeks?|days?))',
            r'Effort:\s*(\d+\s*(?:SP|story points?|weeks?|days?))',
            r'(\d+)\s*story\s*points?',
            r'(\d+)\s*SP\b',
            r'(\d+)\s*weeks?',
            r'(\d+)\s*days?',
        ]

        for pattern in effort_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return None

    def _extract_feature_description(self, content: str) -> str:
        """Extract feature description from content."""
        # Look for description section
        desc_patterns = [
            r'(?:^|\n)#+\s*Description\s*\n(.*?)(?=\n#+|\n\*\*|\Z)',
            r'(?:^|\n)\*\*Description\*\*[:\s]*\n(.*?)(?=\n\*\*|\n#+|\Z)',
        ]

        for pattern in desc_patterns:
            match = re.search(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()

        # Fall back to first paragraph
        paragraphs = content.split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip() and not paragraph.strip().startswith('#'):
                return paragraph.strip()

        return "Feature description not available"

    def _extract_user_stories(self, content: str) -> list[UserStory]:
        """Extract user stories from content in multiple formats."""
        user_stories = []

        # Pattern for "As a ... I want ... so that ..." format
        as_a_pattern = r'(?:^|\n)[\s*-]*As\s+(?:a|an)\s+([^,]+),\s*I\s+want\s+([^,]+),?\s*so\s+that\s+(.+?)(?=\n|$)'

        matches = re.finditer(as_a_pattern, content, re.MULTILINE | re.IGNORECASE)
        for match in matches:
            actor = match.group(1).strip()
            action = match.group(2).strip()
            benefit = match.group(3).strip()

            user_stories.append(UserStory(
                story=match.group(0).strip(),
                format="as_a_user",
                actor=actor,
                action=action,
                benefit=benefit
            ))

        # Pattern for "Given ... When ... Then ..." format
        gwt_pattern = r'(?:^|\n)[\s*-]*Given\s+([^,]+),?\s*When\s+([^,]+),?\s*Then\s+(.+?)(?=\n|$)'

        matches = re.finditer(gwt_pattern, content, re.MULTILINE | re.IGNORECASE)
        for match in matches:
            user_stories.append(UserStory(
                story=match.group(0).strip(),
                format="given_when_then"
            ))

        # Pattern for simple user stories
        simple_pattern = r'(?:^|\n)[\s*-]+(User|System|Admin).+?(?=\n|$)'

        matches = re.finditer(simple_pattern, content, re.MULTILINE | re.IGNORECASE)
        for match in matches:
            story_text = match.group(0).strip()
            if not any(existing.story == story_text for existing in user_stories):
                user_stories.append(UserStory(
                    story=story_text,
                    format="simple"
                ))

        return user_stories

    def _extract_acceptance_criteria(self, content: str) -> list[str]:
        """Extract acceptance criteria from content."""
        criteria = []

        # Look for acceptance criteria section
        ac_pattern = r'(?:^|\n)#+\s*Acceptance\s+Criteria\s*\n(.*?)(?=\n#+|\n\*\*|\Z)'

        match = re.search(ac_pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        if match:
            ac_content = match.group(1).strip()

            # Extract numbered or bulleted criteria
            criteria_lines = re.findall(r'(?:^|\n)[\s]*(?:\d+\.|\-|\*)\s*(.+?)(?=\n|$)', ac_content, re.MULTILINE)
            criteria.extend([line.strip() for line in criteria_lines if line.strip()])

        return criteria

    def _extract_definition_of_done(self, content: str) -> list[str]:
        """Extract definition of done from content."""
        dod_items = []

        # Look for definition of done section
        dod_pattern = r'(?:^|\n)#+\s*Definition\s+of\s+Done\s*\n(.*?)(?=\n#+|\n\*\*|\Z)'

        match = re.search(dod_pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        if match:
            dod_content = match.group(1).strip()

            # Extract checklist items
            dod_lines = re.findall(r'(?:^|\n)[\s]*(?:-\s*\[\s*\]|\-|\*)\s*(.+?)(?=\n|$)', dod_content, re.MULTILINE)
            dod_items.extend([line.strip() for line in dod_lines if line.strip()])

        return dod_items

    def _extract_dependencies_enhanced(self, content: str) -> list[str]:
        """Extract dependencies with enhanced parsing."""
        dependencies = []

        # Look for dependencies section
        dep_patterns = [
            r'(?:^|\n)#+\s*Dependencies\s*\n(.*?)(?=\n#+|\n\*\*|\Z)',
            r'(?:^|\n)\*\*Dependencies\*\*[:\s]*\n?(.*?)(?=\n\*\*|\n#+|\Z)',
            r'\*\*Dependencies\*\*:\s*(.+?)(?=\n|$)',
            r'Dependencies:\s*(.+?)(?=\n|$)',
        ]

        for pattern in dep_patterns:
            match = re.search(pattern, content, re.MULTILINE | re.DOTALL | re.IGNORECASE)
            if match:
                dep_content = match.group(1).strip()

                # Extract dependency references
                if dep_content.lower() == 'none':
                    continue

                # Check if it's a simple comma-separated list (inline format)
                if ',' in dep_content and '\n' not in dep_content.strip():
                    # Handle comma-separated inline dependencies
                    inline_deps = [dep.strip() for dep in dep_content.split(',')]
                    for dep in inline_deps:
                        if dep and dep.lower() != 'none':
                            # Remove parenthetical references like "(2.1)"
                            clean_dep = re.sub(r'\s*\([^)]*\)\s*', '', dep)
                            clean_dep = ' '.join(clean_dep.split())
                            if clean_dep:
                                dependencies.append(clean_dep)
                else:
                    # Parse bullet point format
                    dep_lines = re.findall(r'(?:^|\n)[\s]*(?:\-|\*)\s*(.+?)(?=\n|$)', dep_content, re.MULTILINE)
                    for line in dep_lines:
                        if line.strip():
                            # Clean up the line and extract the main dependency name
                            clean_line = line.strip()
                            # Remove bullet point prefixes that might have been missed
                            clean_line = re.sub(r'^[\-\*\+]\s*', '', clean_line)
                            # Remove parenthetical references like "(2.1)"
                            clean_line = re.sub(r'\s*\([^)]*\)\s*', '', clean_line)
                            # Remove extra whitespace
                            clean_line = ' '.join(clean_line.split())
                            if clean_line and clean_line.lower() != 'none':
                                dependencies.append(clean_line)

                # Don't extract inline references for enhanced parsing - they're already included above
                # inline_deps = re.findall(r'([A-Z]+-\d+|\d+\.\d+)', dep_content)
                # dependencies.extend(inline_deps)

        return list(set(dependencies))  # Remove duplicates

    def _generate_dependency_graph(self, features: list[Feature]) -> dict[str, list[str]]:
        """Generate dependency graph from features."""
        graph: dict[str, list[str]] = {}

        for feature in features:
            feature_id = feature.id
            graph[feature_id] = []

            for dependency in feature.dependencies:
                # Find the feature ID for this dependency
                for dep_feature in features:
                    if (dependency.lower() in dep_feature.title.lower() or
                        dependency == dep_feature.id):
                        graph[feature_id].append(dep_feature.id)
                        break

        return graph
