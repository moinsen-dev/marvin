"""Codebase scanner domain service."""

from pathlib import Path
from typing import Any

from ..entities.codebase import (
    CodebaseAnalysis,
    Component,
    ComponentGraph,
    ComponentType,
    Technology,
    TechnologyCategory,
    TechnologyStack,
)


class CodebaseScanner:
    """Service for scanning and analyzing codebases."""
    
    def __init__(self) -> None:
        """Initialize the codebase scanner."""
        self.relevant_extensions = {
            ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".cpp", ".c",
            ".cs", ".go", ".rs", ".rb", ".php", ".dart", ".swift", ".kt",
            ".yaml", ".yml", ".json", ".toml", ".xml", ".md", ".txt",
        }
    
    def collect_files(self, root_path: Path, max_files: int = 100) -> dict[str, str]:
        """Collect relevant files from the codebase."""
        files = {}
        count = 0
        
        for file_path in root_path.rglob("*"):
            if count >= max_files:
                break
            
            if file_path.is_file() and file_path.suffix in self.relevant_extensions:
                # Skip common directories
                if any(part in file_path.parts for part in [".git", "node_modules", ".venv", "__pycache__"]):
                    continue
                
                try:
                    relative_path = file_path.relative_to(root_path)
                    files[str(relative_path)] = file_path.read_text(errors="ignore")
                    count += 1
                except Exception:
                    continue
        
        return files
    
    def analyze_from_ai_result(self, root_path: Path, ai_analysis: dict[str, Any]) -> CodebaseAnalysis:
        """Build CodebaseAnalysis from AI analysis result."""
        analysis = CodebaseAnalysis(root_path=root_path)
        
        # Build technology stack
        stack = TechnologyStack()
        
        # Primary language
        if lang_info := ai_analysis.get("primary_language"):
            stack.primary_language = Technology(
                name=lang_info.get("name", "Unknown"),
                version=lang_info.get("version"),
                category=TechnologyCategory.LANGUAGE,
            )
        
        # Frameworks
        for fw in ai_analysis.get("frameworks", []):
            tech = Technology(
                name=fw.get("name", ""),
                version=fw.get("version"),
                category=TechnologyCategory.FRAMEWORK,
            )
            stack.add_technology(tech)
        
        # Libraries
        for lib in ai_analysis.get("libraries", []):
            tech = Technology(
                name=lib.get("name", ""),
                version=lib.get("version"),
                category=TechnologyCategory.LIBRARY,
            )
            stack.add_technology(tech)
        
        analysis.technology_stack = stack
        analysis.architecture_patterns = ai_analysis.get("architecture_patterns", [])
        
        # Components
        for comp_data in ai_analysis.get("components", []):
            component = Component(
                name=comp_data.get("name", ""),
                path=Path(comp_data.get("path", "")),
                type=ComponentType(comp_data.get("type", "file")),
                description=comp_data.get("description"),
            )
            analysis.add_component(component)
        
        return analysis
