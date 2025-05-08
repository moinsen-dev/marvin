"""Agent for analyzing codebases."""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from marvin.core.agents.base import Agent
from marvin.core.domain.models import Codebase, Component, Technology


class CodebaseAnalysisAgent(Agent):
    """Agent for analyzing codebases and extracting architecture and technologies."""
    
    def __init__(self, name: str = "codebase_analysis", config: Optional[Dict[str, Any]] = None):
        """Initializes the CodebaseAnalysisAgent.
        
        Args:
            name: Name of the agent
            config: Configuration of the agent
        """
        super().__init__(name, config)
        self.known_languages = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".html": "HTML",
            ".css": "CSS",
            ".scss": "SCSS",
            ".java": "Java",
            ".kt": "Kotlin",
            ".c": "C",
            ".cpp": "C++",
            ".cs": "C#",
            ".go": "Go",
            ".rb": "Ruby",
            ".php": "PHP",
            ".swift": "Swift",
            ".dart": "Dart",
            ".rs": "Rust",
        }
        
        self.framework_indicators = {
            "react": "React",
            "angular": "Angular",
            "vue": "Vue.js",
            "django": "Django",
            "flask": "Flask",
            "fastapi": "FastAPI",
            "express": "Express.js",
            "spring": "Spring",
            "laravel": "Laravel",
            "symfony": "Symfony",
            "flutter": "Flutter",
            "tailwind": "Tailwind CSS",
            "bootstrap": "Bootstrap",
        }
        
        self.database_indicators = {
            "sqlite": "SQLite",
            "postgresql": "PostgreSQL",
            "mysql": "MySQL",
            "mongodb": "MongoDB",
            "redis": "Redis",
            "firestore": "Firestore",
            "dynamodb": "DynamoDB",
        }
        
        self.architecture_patterns = {
            "mvc": "Model-View-Controller",
            "mvvm": "Model-View-ViewModel",
            "clean": "Clean Architecture",
            "hexagonal": "Hexagonal Architecture",
            "microservice": "Microservice Architecture",
            "layered": "Layered Architecture",
            "repository": "Repository Pattern",
            "factory": "Factory Pattern",
            "singleton": "Singleton Pattern",
            "observer": "Observer Pattern",
            "strategy": "Strategy Pattern",
        }
    
    async def execute(
        self, codebase_path: str, **kwargs: Any
    ) -> Codebase:
        """Analyzes a codebase and extracts architecture and technologies.
        
        Args:
            codebase_path: Path to the codebase
            **kwargs: Additional parameters
            
        Returns:
            Analyzed codebase
            
        Raises:
            FileNotFoundError: If the codebase was not found
        """
        if not os.path.exists(codebase_path):
            raise FileNotFoundError(f"Codebase not found: {codebase_path}")
        
        # Create codebase model
        codebase = Codebase(
            id=os.path.basename(codebase_path),
            name=kwargs.get("name", os.path.basename(codebase_path)),
            root_path=codebase_path,
            scanned_at=datetime.now(),
        )
        
        # Scan files and directories
        await self._scan_directory(codebase_path, codebase)
        
        # Identify technologies
        await self._identify_technologies(codebase)
        
        # Recognize architecture patterns
        await self._identify_architecture_patterns(codebase)
        
        return codebase
    
    async def _scan_directory(self, directory: str, codebase: Codebase) -> None:
        """Scans a directory recursively and adds components to the codebase.
        
        Args:
            directory: Directory to scan
            codebase: Codebase model to which components will be added
        """
        excluded_dirs = {".git", "node_modules", "venv", ".venv", "__pycache__", ".idea", ".vscode"}
        
        for root, dirs, files in os.walk(directory):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
            # Add directory as a component
            rel_path = os.path.relpath(root, directory)
            if rel_path != ".":
                component = Component(
                    name=os.path.basename(root),
                    path=rel_path,
                    type="directory",
                )
                codebase.add_component(component)
            
            # Add files as components
            for file in files:
                file_path = os.path.join(rel_path, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                # Only consider certain file types
                if file_ext in self.known_languages or file in ["Dockerfile", "docker-compose.yml", "package.json", "requirements.txt", "pyproject.toml"]:
                    component = Component(
                        name=file,
                        path=file_path,
                        type="file",
                    )
                    codebase.add_component(component)
    
    async def _identify_technologies(self, codebase: Codebase) -> None:
        """Identifies technologies used in the codebase.
        
        Args:
            codebase: Codebase to analyze
        """
        # Count used languages
        language_counts: Dict[str, int] = {}
        
        for component in codebase.components:
            if component.type == "file":
                file_ext = os.path.splitext(component.name)[1].lower()
                if file_ext in self.known_languages:
                    lang = self.known_languages[file_ext]
                    language_counts[lang] = language_counts.get(lang, 0) + 1
        
        # Add languages as technologies
        for lang, count in language_counts.items():
            tech = Technology(
                name=lang,
                category="language",
                description=f"{count} files found",
            )
            codebase.technologies.append(tech)
        
        # Check special files
        await self._check_special_files(codebase)
    
    async def _check_special_files(self, codebase: Codebase) -> None:
        """Checks special files to identify additional technologies.
        
        Args:
            codebase: Codebase to analyze
        """
        # Check if package.json exists
        package_json_components = [c for c in codebase.components if c.name == "package.json"]
        if package_json_components:
            # NPM project detected
            tech = Technology(
                name="NPM",
                category="package_manager",
                description="package.json found",
            )
            codebase.technologies.append(tech)
            
            # TODO: Parse package.json to extract dependencies
        
        # Check if requirements.txt exists
        requirements_txt_components = [c for c in codebase.components if c.name == "requirements.txt"]
        if requirements_txt_components:
            # Python project with Pip detected
            tech = Technology(
                name="Pip",
                category="package_manager",
                description="requirements.txt found",
            )
            codebase.technologies.append(tech)
            
            # TODO: Parse requirements.txt to extract dependencies
        
        # Check if pyproject.toml exists
        pyproject_toml_components = [c for c in codebase.components if c.name == "pyproject.toml"]
        if pyproject_toml_components:
            # Python project with Poetry detected
            tech = Technology(
                name="Poetry",
                category="package_manager",
                description="pyproject.toml found",
            )
            codebase.technologies.append(tech)
            
            # TODO: Parse pyproject.toml to extract dependencies
        
        # Check if Dockerfile exists
        dockerfile_components = [c for c in codebase.components if c.name == "Dockerfile"]
        if dockerfile_components:
            # Docker detected
            tech = Technology(
                name="Docker",
                category="containerization",
                description="Dockerfile found",
            )
            codebase.technologies.append(tech)
    
    async def _identify_architecture_patterns(self, codebase: Codebase) -> None:
        """Identifies architecture patterns in the codebase.
        
        Args:
            codebase: Codebase to analyze
        """
        # Here we would use Context 7 or another code analysis library
        # For now, we implement a simple heuristic detection
        
        # Analyze directory structure
        component_names = {c.name.lower() for c in codebase.components if c.type == "directory"}
        
        # Detect MVC pattern
        if "models" in component_names and "views" in component_names and "controllers" in component_names:
            codebase.architecture_patterns.append("Model-View-Controller (MVC)")
        
        # Detect Clean Architecture / Hexagonal Architecture
        if "domain" in component_names and "infrastructure" in component_names and "adapters" in component_names:
            codebase.architecture_patterns.append("Hexagonal Architecture")
        elif "core" in component_names and "infrastructure" in component_names:
            codebase.architecture_patterns.append("Clean Architecture")
        
        # Detect Microservices
        if "services" in component_names or "microservices" in component_names:
            service_count = len([c for c in codebase.components if c.type == "directory" and c.name.endswith("service")])
            if service_count >= 2:
                codebase.architecture_patterns.append("Microservice Architecture")
        
        # Detect Repository Pattern
        if "repositories" in component_names or "repos" in component_names:
            codebase.architecture_patterns.append("Repository Pattern")
