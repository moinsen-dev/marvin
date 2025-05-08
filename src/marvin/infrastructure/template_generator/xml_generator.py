"""Generator für XML-basierte AI-Coding-Tasks."""

import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from lxml import etree

from marvin.core.domain.models import Codebase, Feature, PRD, Task


class XMLTemplateGenerator:
    """Generator für XML-basierte AI-Coding-Tasks."""
    
    def __init__(self, template_path: Optional[str] = None):
        """Initialisiert den XMLTemplateGenerator.
        
        Args:
            template_path: Pfad zur Template-XML-Datei. Wenn None, wird das Standard-Template verwendet.
        """
        self.template_path = template_path
        self._load_template()
    
    def _load_template(self) -> None:
        """Lädt das XML-Template."""
        if self.template_path and os.path.exists(self.template_path):
            with open(self.template_path, "r", encoding="utf-8") as f:
                self.template_content = f.read()
        else:
            # Standard-Template verwenden
            self.template_content = """<?xml version="1.0" encoding="UTF-8"?>
<CodingTask>
  <SequenceInfo>
    <TaskID>{task_id}</TaskID>
    <SequenceNumber>{sequence_number}</SequenceNumber>
    <DependsOn>{depends_on}</DependsOn>
  </SequenceInfo>

  <Metadata>
    <Author>{author}</Author>
    <Date>{date}</Date>
    <TemplateVersion>2.0</TemplateVersion>
    <RevisionHistory>
      <Change version="1.0" date="{date}" author="{author}" summary="Initial version"/>
    </RevisionHistory>
  </Metadata>

  <Context>
    <ProjectName>{project_name}</ProjectName>
    <ProjectDescription>{project_description}</ProjectDescription>
    <BusinessDomain>{business_domain}</BusinessDomain>
    <Stakeholders>
      <Stakeholder role="Product Owner" name="{stakeholder_name}" contact="{stakeholder_contact}" responsibility="Feature prioritization"/>
    </Stakeholders>
    <Assumptions>{assumptions}</Assumptions>
    <Risks mitigationPlan="{risk_mitigation}">{risks}</Risks>
    <Dependencies>
      <Upstream>{upstream_dependencies}</Upstream>
      <Downstream>{downstream_dependencies}</Downstream>
    </Dependencies>
    <Constraints>{constraints}</Constraints>
  </Context>

  <TechnologyStack>
    <Languages>
      {languages}
    </Languages>
    <Frameworks>
      {frameworks}
    </Frameworks>
    <PackageManagers>{package_managers}</PackageManagers>
    <DatabaseSystems>{database_systems}</DatabaseSystems>
    <CloudProvider>{cloud_provider}</CloudProvider>
    <Containerization>{containerization}</Containerization>
    <OtherTechnologies>
      {other_technologies}
    </OtherTechnologies>
  </TechnologyStack>

  <Architecture>
    <Pattern>{architecture_pattern}</Pattern>
    <ArchitectureDecisionRecords>
      {adrs}
    </ArchitectureDecisionRecords>
    <DomainModel>{domain_model}</DomainModel>
  </Architecture>

  <Task>
    <TaskName>{task_name}</TaskName>
    <UserStories>
      {user_stories}
    </UserStories>
    <Description>{task_description}</Description>
    <Purpose>{purpose}</Purpose>
    <Scope>
      <InScope>{in_scope}</InScope>
      <OutOfScope>{out_of_scope}</OutOfScope>
    </Scope>
    <AffectedComponents>
      <Files>{affected_files}</Files>
      <Folders>{affected_folders}</Folders>
    </AffectedComponents>
  </Task>

  <ExpectedOutcome>
    <FunctionalRequirements>{functional_requirements}</FunctionalRequirements>
    <NonFunctionalRequirements>
      <Performance>{performance}</Performance>
      <Scalability>{scalability}</Scalability>
      <Security level="{security_level}">{security}</Security>
      <Accessibility targetWCAGLevel="{wcag_level}">{accessibility}</Accessibility>
      <Internationalization locales="{locales}">{i18n}</Internationalization>
      <Observability SLOs="{slos}">{observability}</Observability>
    </NonFunctionalRequirements>
    <AcceptanceCriteria>{acceptance_criteria}</AcceptanceCriteria>
  </ExpectedOutcome>

  <Implementation>
    <CodeStandardsRef link="{code_standards_link}">{code_standards}</CodeStandardsRef>
    <APIContract type="{api_contract_type}" link="{api_contract_link}">{api_contract}</APIContract>
    <DesignPatterns>{design_patterns}</DesignPatterns>
    <Security>
      <ThreatModel>{threat_model}</ThreatModel>
      <Auth>{auth}</Auth>
      <DataClassification>{data_classification}</DataClassification>
      <ComplianceStandards>{compliance_standards}</ComplianceStandards>
    </Security>
    <Testing>
      <TestFramework>{test_framework}</TestFramework>
      <CoverageTarget>{coverage_target}</CoverageTarget>
      <QualityGates>{quality_gates}</QualityGates>
    </Testing>
    <CI_CD_Pipeline>
      <Toolchain>{ci_cd_toolchain}</Toolchain>
      <Environments dev="{dev_env}" test="{test_env}" staging="{staging_env}" prod="{prod_env}"/>
      <DeploymentStrategy>{deployment_strategy}</DeploymentStrategy>
      <RollbackPlan>{rollback_plan}</RollbackPlan>
    </CI_CD_Pipeline>
    <LoggingMonitoring>
      <LogSchema>{log_schema}</LogSchema>
      <AlertingRules>{alerting_rules}</AlertingRules>
    </LoggingMonitoring>
    <DataMigration>
      <Scope>{data_migration_scope}</Scope>
      <DryRunPlan>{dry_run_plan}</DryRunPlan>
      <Validation>{data_validation}</Validation>
      <Fallback>{data_fallback}</Fallback>
    </DataMigration>
    <PerformanceConsiderations>{performance_considerations}</PerformanceConsiderations>
  </Implementation>

  <References>
    <ExistingCode link="{existing_code_link}">{existing_code}</ExistingCode>
    <Documentation link="{documentation_link}">{documentation}</Documentation>
    <ExternalResources link="{external_resources_link}">{external_resources}</ExternalResources>
  </References>

  <Deliverables>
    <Checklist>
      <Item done="false">Repo branch created</Item>
      <Item done="false">Unit tests pass at 90% coverage</Item>
      <Item done="false">Security review signed-off</Item>
    </Checklist>
    <ExpectedTimeframe>{expected_timeframe}</ExpectedTimeframe>
  </Deliverables>

  <Glossary>
    {glossary}
  </Glossary>
</CodingTask>
"""
    
    def generate_task_template(
        self,
        task: Task,
        feature: Feature,
        prd: PRD,
        codebase: Optional[Codebase] = None,
        additional_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Generiert ein XML-Template für eine AI-Coding-Task.
        
        Args:
            task: Die Task, für die das Template generiert werden soll
            feature: Das Feature, zu dem die Task gehört
            prd: Das PRD, zu dem das Feature gehört
            codebase: (Optional) Die analysierte Codebase
            additional_context: (Optional) Zusätzlicher Kontext für das Template
            
        Returns:
            Das generierte XML-Template als String
        """
        context = additional_context or {}
        
        # Grundlegende Task-Informationen
        context.update({
            "task_id": task.task_id,
            "sequence_number": task.sequence_number,
            "depends_on": ",".join(task.depends_on),
            "author": prd.author,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "task_name": task.name,
            "task_description": task.description,
            "project_name": prd.title,
            "project_description": prd.description,
        })
        
        # Feature-Informationen
        context.update({
            "purpose": feature.description,
            "functional_requirements": "\n".join(feature.requirements),
            "user_stories": self._generate_user_stories(feature),
        })
        
        # Codebase-Informationen, falls verfügbar
        if codebase:
            context.update({
                "languages": self._generate_languages(codebase),
                "frameworks": self._generate_frameworks(codebase),
                "architecture_pattern": ", ".join(codebase.architecture_patterns),
            })
        
        # Fehlende Felder mit Platzhaltern füllen
        self._fill_missing_placeholders(context)
        
        # Template rendern
        return self.template_content.format(**context)
    
    def _generate_user_stories(self, feature: Feature) -> str:
        """Generiert XML für User Stories aus einem Feature.
        
        Args:
            feature: Das Feature
            
        Returns:
            XML-String für User Stories
        """
        # Einfaches Beispiel: Eine Story pro Feature
        return f"""<Story id="{feature.id}_story_01" 
                role="User" 
                goal="to be able to {feature.name}" 
                benefit="to {feature.description.split('.')[0] if '.' in feature.description else feature.description}"
                acceptanceCriteria="{'; '.join(feature.requirements[:3]) if feature.requirements else 'TBD'}"/>"""
    
    def _generate_languages(self, codebase: Codebase) -> str:
        """Generiert XML für Programmiersprachen.
        
        Args:
            codebase: Die analysierte Codebase
            
        Returns:
            XML-String für Programmiersprachen
        """
        languages = [
            tech for tech in codebase.technologies if tech.category == "language"
        ]
        
        if not languages:
            return "<Language name=\"\" version=\"\"/>"
        
        result = ""
        for lang in languages:
            result += f'<Language name="{lang.name}" version="{lang.version or "latest"}"/>\n      '
        
        return result.strip()
    
    def _generate_frameworks(self, codebase: Codebase) -> str:
        """Generiert XML für Frameworks.
        
        Args:
            codebase: Die analysierte Codebase
            
        Returns:
            XML-String für Frameworks
        """
        frameworks = [
            tech for tech in codebase.technologies if tech.category == "framework"
        ]
        
        if not frameworks:
            return "<Framework name=\"\" version=\"\"/>"
        
        result = ""
        for framework in frameworks:
            result += f'<Framework name="{framework.name}" version="{framework.version or "latest"}"/>\n      '
        
        return result.strip()
    
    def _fill_missing_placeholders(self, context: Dict[str, Any]) -> None:
        """Füllt fehlende Platzhalter im Template mit Standardwerten.
        
        Args:
            context: Der Kontext für die Template-Generierung
        """
        # Alle Platzhalter aus dem Template extrahieren
        import re
        placeholders = re.findall(r"{([^{}]+)}", self.template_content)
        
        # Fehlende Platzhalter mit Standardwerten füllen
        for placeholder in placeholders:
            if placeholder not in context:
                context[placeholder] = ""
    
    def save_to_file(self, content: str, output_path: str) -> None:
        """Speichert den generierten Inhalt in einer Datei.
        
        Args:
            content: Der zu speichernde Inhalt
            output_path: Der Pfad zur Ausgabedatei
            
        Raises:
            IOError: Wenn die Datei nicht gespeichert werden kann
        """
        # Verzeichnis erstellen, falls es nicht existiert
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    def validate_xml(self, xml_content: str) -> Tuple[bool, Optional[str]]:
        """Validiert ein XML-Dokument.
        
        Args:
            xml_content: Der XML-Inhalt
            
        Returns:
            Tupel aus Validierungsstatus (True/False) und Fehlermeldung (None, wenn valide)
        """
        try:
            parser = etree.XMLParser(dtd_validation=False)
            etree.fromstring(xml_content.encode("utf-8"), parser)
            return True, None
        except etree.XMLSyntaxError as e:
            return False, str(e)
