"""Agent zur Generierung von AI-Coding-Task-Templates."""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from marvin.core.agents.base import Agent
from marvin.core.domain.models import Codebase, Feature, PRD, Task
from marvin.infrastructure.template_generator.xml_generator import XMLTemplateGenerator


class TemplateGenerationAgent(Agent):
    """Agent zur Generierung von XML-basierten AI-Coding-Task-Templates."""
    
    def __init__(self, name: str = "template_generation", config: Optional[Dict[str, Any]] = None):
        """Initialisiert den TemplateGenerationAgent.
        
        Args:
            name: Name des Agenten
            config: Konfiguration des Agenten
        """
        super().__init__(name, config)
        self.template_generator = XMLTemplateGenerator()
    
    async def execute(
        self,
        task: Task,
        feature: Feature,
        prd: PRD,
        output_dir: str,
        codebase: Optional[Codebase] = None,
        **kwargs: Any,
    ) -> str:
        """Generiert ein XML-Template für eine AI-Coding-Task.
        
        Args:
            task: Die Task, für die das Template generiert werden soll
            feature: Das Feature, zu dem die Task gehört
            prd: Das PRD, zu dem das Feature gehört
            output_dir: Ausgabeverzeichnis für das Template
            codebase: (Optional) Die analysierte Codebase
            **kwargs: Weitere Parameter
            
        Returns:
            Pfad zum generierten Template
            
        Raises:
            IOError: Wenn das Template nicht gespeichert werden kann
        """
        # Zusätzlichen Kontext für das Template erstellen
        additional_context = await self._prepare_additional_context(task, feature, prd, codebase, **kwargs)
        
        # Template generieren
        template_content = self.template_generator.generate_task_template(
            task, feature, prd, codebase, additional_context
        )
        
        # Prüfen, ob das Template valide ist
        is_valid, error = self.template_generator.validate_xml(template_content)
        if not is_valid:
            raise ValueError(f"Generiertes Template ist ungültig: {error}")
        
        # Ausgabepfad erstellen
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(
            output_dir, f"{task.sequence_number:02d}_{feature.id}_{task.task_id}.xml"
        )
        
        # Template speichern
        self.template_generator.save_to_file(template_content, output_path)
        
        return output_path
    
    async def _prepare_additional_context(
        self,
        task: Task,
        feature: Feature,
        prd: PRD,
        codebase: Optional[Codebase],
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """Bereitet zusätzlichen Kontext für das Template vor.
        
        Args:
            task: Die Task, für die das Template generiert werden soll
            feature: Das Feature, zu dem die Task gehört
            prd: Das PRD, zu dem das Feature gehört
            codebase: (Optional) Die analysierte Codebase
            **kwargs: Weitere Parameter
            
        Returns:
            Zusätzlicher Kontext für das Template
        """
        # Hier würden wir Google ADK verwenden, um den Kontext zu verbessern
        # Für jetzt implementieren wir eine einfache Kontexterstellung
        
        context = {}
        
        # Geschäftsdomäne aus dem PRD-Titel ableiten
        business_domain = prd.title.split(":")[1].strip() if ":" in prd.title else prd.title
        context["business_domain"] = business_domain
        
        # Annahmen hinzufügen
        context["assumptions"] = f"Feature '{feature.name}' kann unabhängig implementiert werden."
        
        # Risiken hinzufügen
        context["risks"] = f"Änderungen an {feature.name} können andere Komponenten beeinflussen."
        context["risk_mitigation"] = "Umfangreiche Tests durchführen"
        
        # Betroffene Komponenten hinzufügen
        if codebase:
            affected_files = []
            affected_folders = []
            
            # In einer vollständigen Implementierung würden wir hier Context 7 verwenden
            for component in codebase.components:
                # Einfache Heuristik: Wenn der Komponentenname im Feature-Namen enthalten ist
                if component.name.lower() in feature.name.lower():
                    if component.type == "file":
                        affected_files.append(component.path)
                    elif component.type == "directory":
                        affected_folders.append(component.path)
            
            context["affected_files"] = ", ".join(affected_files[:5])
            context["affected_folders"] = ", ".join(affected_folders[:3])
        
        # Akzeptanzkriterien aus den Feature-Anforderungen ableiten
        if feature.requirements:
            context["acceptance_criteria"] = "\n".join(
                f"- {req}" for req in feature.requirements
            )
        
        # Erwarteten Zeitrahmen schätzen
        context["expected_timeframe"] = "1-2 Tage"
        
        return context
