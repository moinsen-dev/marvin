"""Agent zur Analyse von Codebases."""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from marvin.core.agents.base import Agent
from marvin.core.domain.models import Codebase, Component, Technology


class CodebaseAnalysisAgent(Agent):
    """Agent zur Analyse von Codebases und Extraktion von Architektur und Technologien."""
    
    def __init__(self, name: str = "codebase_analysis", config: Optional[Dict[str, Any]] = None):
        """Initialisiert den CodebaseAnalysisAgent.
        
        Args:
            name: Name des Agenten
            config: Konfiguration des Agenten
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
        """Analysiert eine Codebase und extrahiert Architektur und Technologien.
        
        Args:
            codebase_path: Pfad zur Codebase
            **kwargs: Weitere Parameter
            
        Returns:
            Analysierte Codebase
            
        Raises:
            FileNotFoundError: Wenn die Codebase nicht gefunden wurde
        """
        if not os.path.exists(codebase_path):
            raise FileNotFoundError(f"Codebase nicht gefunden: {codebase_path}")
        
        # Codebase-Modell erstellen
        codebase = Codebase(
            id=os.path.basename(codebase_path),
            name=kwargs.get("name", os.path.basename(codebase_path)),
            root_path=codebase_path,
            scanned_at=datetime.now(),
        )
        
        # Dateien und Verzeichnisse scannen
        await self._scan_directory(codebase_path, codebase)
        
        # Technologien identifizieren
        await self._identify_technologies(codebase)
        
        # Architekturmuster erkennen
        await self._identify_architecture_patterns(codebase)
        
        return codebase
    
    async def _scan_directory(self, directory: str, codebase: Codebase) -> None:
        """Scannt ein Verzeichnis rekursiv und fügt Komponenten zur Codebase hinzu.
        
        Args:
            directory: Zu scannendes Verzeichnis
            codebase: Codebase-Modell, zu dem Komponenten hinzugefügt werden
        """
        excluded_dirs = {".git", "node_modules", "venv", ".venv", "__pycache__", ".idea", ".vscode"}
        
        for root, dirs, files in os.walk(directory):
            # Ausgeschlossene Verzeichnisse überspringen
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            
            # Verzeichnis als Komponente hinzufügen
            rel_path = os.path.relpath(root, directory)
            if rel_path != ".":
                component = Component(
                    name=os.path.basename(root),
                    path=rel_path,
                    type="directory",
                )
                codebase.add_component(component)
            
            # Dateien als Komponenten hinzufügen
            for file in files:
                file_path = os.path.join(rel_path, file)
                file_ext = os.path.splitext(file)[1].lower()
                
                # Nur bestimmte Dateitypen berücksichtigen
                if file_ext in self.known_languages or file in ["Dockerfile", "docker-compose.yml", "package.json", "requirements.txt", "pyproject.toml"]:
                    component = Component(
                        name=file,
                        path=file_path,
                        type="file",
                    )
                    codebase.add_component(component)
    
    async def _identify_technologies(self, codebase: Codebase) -> None:
        """Identifiziert verwendete Technologien in der Codebase.
        
        Args:
            codebase: Zu analysierende Codebase
        """
        # Verwendete Sprachen zählen
        language_counts: Dict[str, int] = {}
        
        for component in codebase.components:
            if component.type == "file":
                file_ext = os.path.splitext(component.name)[1].lower()
                if file_ext in self.known_languages:
                    lang = self.known_languages[file_ext]
                    language_counts[lang] = language_counts.get(lang, 0) + 1
        
        # Sprachen als Technologien hinzufügen
        for lang, count in language_counts.items():
            tech = Technology(
                name=lang,
                category="language",
                description=f"{count} Dateien gefunden",
            )
            codebase.technologies.append(tech)
        
        # Spezielle Dateien prüfen
        await self._check_special_files(codebase)
    
    async def _check_special_files(self, codebase: Codebase) -> None:
        """Prüft spezielle Dateien, um weitere Technologien zu identifizieren.
        
        Args:
            codebase: Zu analysierende Codebase
        """
        # Prüfen, ob package.json existiert
        package_json_components = [c for c in codebase.components if c.name == "package.json"]
        if package_json_components:
            # NPM-Projekt erkannt
            tech = Technology(
                name="NPM",
                category="package_manager",
                description="Package.json gefunden",
            )
            codebase.technologies.append(tech)
            
            # TODO: package.json parsen, um Dependencies zu extrahieren
        
        # Prüfen, ob requirements.txt existiert
        requirements_txt_components = [c for c in codebase.components if c.name == "requirements.txt"]
        if requirements_txt_components:
            # Python-Projekt mit Pip erkannt
            tech = Technology(
                name="Pip",
                category="package_manager",
                description="Requirements.txt gefunden",
            )
            codebase.technologies.append(tech)
            
            # TODO: requirements.txt parsen, um Dependencies zu extrahieren
        
        # Prüfen, ob pyproject.toml existiert
        pyproject_toml_components = [c for c in codebase.components if c.name == "pyproject.toml"]
        if pyproject_toml_components:
            # Python-Projekt mit Poetry erkannt
            tech = Technology(
                name="Poetry",
                category="package_manager",
                description="pyproject.toml gefunden",
            )
            codebase.technologies.append(tech)
            
            # TODO: pyproject.toml parsen, um Dependencies zu extrahieren
        
        # Prüfen, ob Dockerfile existiert
        dockerfile_components = [c for c in codebase.components if c.name == "Dockerfile"]
        if dockerfile_components:
            # Docker erkannt
            tech = Technology(
                name="Docker",
                category="containerization",
                description="Dockerfile gefunden",
            )
            codebase.technologies.append(tech)
    
    async def _identify_architecture_patterns(self, codebase: Codebase) -> None:
        """Identifiziert Architekturmuster in der Codebase.
        
        Args:
            codebase: Zu analysierende Codebase
        """
        # Hier würden wir Context 7 oder eine andere Codeanalyse-Bibliothek verwenden
        # Für jetzt implementieren wir eine einfache heuristische Erkennung
        
        # Verzeichnisstruktur analysieren
        component_names = {c.name.lower() for c in codebase.components if c.type == "directory"}
        
        # MVC-Muster erkennen
        if "models" in component_names and "views" in component_names and "controllers" in component_names:
            codebase.architecture_patterns.append("Model-View-Controller (MVC)")
        
        # Clean Architecture / Hexagonal Architecture erkennen
        if "domain" in component_names and "infrastructure" in component_names and "adapters" in component_names:
            codebase.architecture_patterns.append("Hexagonal Architecture")
        elif "core" in component_names and "infrastructure" in component_names:
            codebase.architecture_patterns.append("Clean Architecture")
        
        # Microservices erkennen
        if "services" in component_names or "microservices" in component_names:
            service_count = len([c for c in codebase.components if c.type == "directory" and c.name.endswith("service")])
            if service_count >= 2:
                codebase.architecture_patterns.append("Microservice Architecture")
        
        # Repository Pattern erkennen
        if "repositories" in component_names or "repos" in component_names:
            codebase.architecture_patterns.append("Repository Pattern")
