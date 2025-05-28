"""Generator for XML-based AI coding tasks."""

import os
from datetime import datetime
from typing import Any

from lxml import etree

from marvin.core.domain.models import PRD, Codebase, Feature, Task


class XMLTemplateGenerator:
    """Generator for XML-based AI coding tasks."""

    def __init__(self, template_path: str | None = None):
        """Initializes the XMLTemplateGenerator.

        Args:
            template_path: Path to the template XML file. If None, the default template is used.
        """
        self.template_path = template_path
        self._load_template()

    def _load_template(self) -> None:
        """Loads the XML template."""
        if self.template_path and os.path.exists(self.template_path):
            with open(self.template_path, encoding="utf-8") as f:
                self.template_content = f.read()
        else:
            # Use default template
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
        codebase: Codebase | None = None,
        additional_context: dict[str, Any] | None = None,
    ) -> str:
        """Generates an XML template for an AI coding task.

        Args:
            task: The task for which the template should be generated
            feature: The feature to which the task belongs
            prd: The PRD to which the feature belongs
            codebase: (Optional) The analyzed codebase
            additional_context: (Optional) Additional context for the template

        Returns:
            The generated XML template as a string
        """
        context = additional_context or {}

        # Basic task information
        context.update(
            {
                "task_id": task.task_id,
                "sequence_number": task.sequence_number,
                "depends_on": ",".join(task.depends_on),
                "author": prd.author,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "task_name": task.name,
                "task_description": task.description,
                "project_name": prd.title,
                "project_description": prd.description,
            }
        )

        # Feature information
        context.update(
            {
                "purpose": feature.description,
                "functional_requirements": "\n".join(feature.requirements),
                "user_stories": self._generate_user_stories(feature),
            }
        )

        # Codebase information, if available
        if codebase:
            context.update(
                {
                    "languages": self._generate_languages(codebase),
                    "frameworks": self._generate_frameworks(codebase),
                    "architecture_pattern": ", ".join(codebase.architecture_patterns),
                }
            )

        # Fill missing fields with placeholders
        self._fill_missing_placeholders(context)

        # Render template
        return self.template_content.format(**context)

    def _generate_user_stories(self, feature: Feature) -> str:
        """Generates XML for user stories from a feature.

        Args:
            feature: The feature

        Returns:
            XML string for user stories
        """
        # Simple example: One story per feature
        return f"""<Story id="{feature.id}_story_01"
                role="User"
                goal="to be able to {feature.name}"
                benefit="to {feature.description.split('.')[0] if '.' in feature.description else feature.description}"
                acceptanceCriteria="{'; '.join(feature.requirements[:3]) if feature.requirements else 'TBD'}"/>"""

    def _generate_languages(self, codebase: Codebase) -> str:
        """Generates XML for programming languages.

        Args:
            codebase: The analyzed codebase

        Returns:
            XML string for programming languages
        """
        languages = [
            tech for tech in codebase.technologies if tech.category == "language"
        ]

        if not languages:
            return '<Language name="" version=""/>'

        result = ""
        for lang in languages:
            result += f'<Language name="{lang.name}" version="{lang.version or "latest"}"/>\n      '

        return result.strip()

    def _generate_frameworks(self, codebase: Codebase) -> str:
        """Generates XML for frameworks.

        Args:
            codebase: The analyzed codebase

        Returns:
            XML string for frameworks
        """
        frameworks = [
            tech for tech in codebase.technologies if tech.category == "framework"
        ]

        if not frameworks:
            return '<Framework name="" version=""/>'

        result = ""
        for framework in frameworks:
            result += f'<Framework name="{framework.name}" version="{framework.version or "latest"}"/>\n      '

        return result.strip()

    def _fill_missing_placeholders(self, context: dict[str, Any]) -> None:
        """Fills missing placeholders in the template with default values.

        Args:
            context: The context for template generation
        """
        # Extract all placeholders from the template
        import re

        placeholders = re.findall(r"{([^{}]+)}", self.template_content)

        # Fill missing placeholders with default values
        for placeholder in placeholders:
            if placeholder not in context:
                context[placeholder] = ""

    def save_to_file(self, content: str, output_path: str) -> None:
        """Saves the generated content to a file.

        Args:
            content: The content to save
            output_path: The path to the output file

        Raises:
            IOError: If the file cannot be saved
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

    def validate_xml(self, xml_content: str) -> tuple[bool, str | None]:
        """Validates an XML document.

        Args:
            xml_content: The XML content

        Returns:
            Tuple of validation status (True/False) and error message (None if valid)
        """
        try:
            parser = etree.XMLParser(dtd_validation=False)
            etree.fromstring(xml_content.encode("utf-8"), parser)
            return True, None
        except etree.XMLSyntaxError as e:
            return False, str(e)
