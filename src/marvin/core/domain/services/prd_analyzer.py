"""PRD analyzer domain service."""

import re
from pathlib import Path
from typing import Optional

from ..entities.prd import (
    FeatureSpecification,
    PRDDocument,
    PriorityLevel,
    Requirement,
    RequirementType,
    UserStory,
)


class PRDAnalyzer:
    """Service for analyzing PRD documents."""
    
    def __init__(self) -> None:
        """Initialize the PRD analyzer."""
        self._priority_keywords = {
            PriorityLevel.CRITICAL: ["critical", "must-have", "essential", "required"],
            PriorityLevel.HIGH: ["high", "important", "should-have"],
            PriorityLevel.MEDIUM: ["medium", "nice-to-have", "could-have"],
            PriorityLevel.LOW: ["low", "optional", "future"],
        }
    
    def analyze_document(self, content: str, metadata: Optional[dict] = None) -> PRDDocument:
        """Analyze PRD content and extract structured information."""
        prd = PRDDocument(
            title=self._extract_title(content),
            description=self._extract_description(content),
            author=metadata.get("author", "Unknown") if metadata else "Unknown",
            version=metadata.get("version", "1.0.0") if metadata else "1.0.0",
        )
        
        # Extract features
        features = self._extract_features(content)
        for feature in features:
            prd.add_feature(feature)
        
        return prd
    
    def analyze_file(self, file_path: Path) -> PRDDocument:
        """Analyze a PRD file."""
        content = file_path.read_text()
        metadata = {"author": "File Import", "version": "1.0.0"}
        return self.analyze_document(content, metadata)
    
    def _extract_title(self, content: str) -> str:
        """Extract title from PRD content."""
        lines = content.strip().split('\n')
        for line in lines:
            if line.strip().startswith('#'):
                return line.strip('#').strip()
        return "Untitled PRD"
    
    def _extract_description(self, content: str) -> str:
        """Extract description from PRD content."""
        # Look for overview or description section
        sections = re.split(r'^#+\s+', content, flags=re.MULTILINE)
        for section in sections:
            if any(word in section.lower()[:50] for word in ['overview', 'description', 'introduction']):
                return section.strip().split('\n', 1)[1].strip() if '\n' in section else section.strip()
        return "No description provided"
    
    def _extract_features(self, content: str) -> list[FeatureSpecification]:
        """Extract features from PRD content."""
        features = []
        
        # Simple pattern matching for features
        feature_sections = re.findall(
            r'(?:###+\s*Feature[:\s]+|###+\s*)(.+?)(?=\n##|$)',
            content,
            re.DOTALL | re.MULTILINE
        )
        
        for i, section in enumerate(feature_sections):
            feature = self._parse_feature_section(section, i)
            if feature:
                features.append(feature)
        
        return features
    
    def _parse_feature_section(self, section: str, index: int) -> Optional[FeatureSpecification]:
        """Parse a feature section."""
        lines = section.strip().split('\n')
        if not lines:
            return None
        
        title = lines[0].strip()
        description = '\n'.join(lines[1:]).strip()
        
        feature = FeatureSpecification(
            name=title,
            description=description,
            priority=self._detect_priority(section),
        )
        
        # Extract user stories
        stories = self._extract_user_stories(section)
        for story in stories:
            feature.add_user_story(story)
        
        # Extract requirements
        requirements = self._extract_requirements(section)
        for req in requirements:
            feature.add_requirement(req)
        
        return feature
    
    def _detect_priority(self, text: str) -> PriorityLevel:
        """Detect priority level from text."""
        text_lower = text.lower()
        
        for priority, keywords in self._priority_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return priority
        
        return PriorityLevel.MEDIUM
    
    def _extract_user_stories(self, section: str) -> list[UserStory]:
        """Extract user stories from a section."""
        stories = []
        
        # Pattern for "As a... I want... so that..."
        pattern = r"[Aa]s\s+a\s+(.+?),?\s*[Ii]\s+want\s+(?:to\s+)?(.+?)\s+so\s+that\s+(.+?)(?:\.|$)"
        matches = re.findall(pattern, section, re.MULTILINE)
        
        for persona, goal, benefit in matches:
            story = UserStory(
                persona=persona.strip(),
                goal=goal.strip(),
                benefit=benefit.strip()
            )
            stories.append(story)
        
        return stories
    
    def _extract_requirements(self, section: str) -> list[Requirement]:
        """Extract requirements from a section."""
        requirements = []
        
        # Look for bullet points or numbered lists
        req_pattern = r'(?:^|\n)\s*[-*•]\s+(.+?)(?=\n\s*[-*•]|$)'
        matches = re.findall(req_pattern, section, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            req = Requirement(
                description=match.strip(),
                type=self._detect_requirement_type(match),
                priority=self._detect_priority(match)
            )
            requirements.append(req)
        
        return requirements
    
    def _detect_requirement_type(self, text: str) -> RequirementType:
        """Detect requirement type from text."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['performance', 'scalability', 'security', 'reliability']):
            return RequirementType.NON_FUNCTIONAL
        elif any(word in text_lower for word in ['technical', 'architecture', 'technology']):
            return RequirementType.TECHNICAL
        elif any(word in text_lower for word in ['business', 'revenue', 'cost', 'roi']):
            return RequirementType.BUSINESS
        elif any(word in text_lower for word in ['ui', 'ux', 'design', 'interface']):
            return RequirementType.USER_EXPERIENCE
        else:
            return RequirementType.FUNCTIONAL
