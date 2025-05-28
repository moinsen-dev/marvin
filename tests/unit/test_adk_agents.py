"""
Unit tests for ADK agents.

Following TDD approach - comprehensive testing of ADK agent functionality.
"""

import json
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest

from marvin.adapters.adk_agents.marvin_orchestrator_adk import (
    MarvinOrchestratorADKAgent,
    analyze_prd_document,
    create_project_workflow,
    generate_project_summary,
    generate_xml_templates,
)
from marvin.adapters.adk_agents.sequence_planner_adk import (
    SequencePlannerADKAgent,
    _calculate_complexity_score,
    _detect_circular_dependencies,
    _topological_sort,
    analyze_feature_dependencies,
    create_task_breakdown,
    validate_workflow_feasibility,
)
from marvin.core.domain.models import PRD, Feature, FeatureStatus


class TestSequencePlannerADK:
    """Test cases for the SequencePlannerADKAgent."""

    def setup_method(self):
        """Set up test fixtures."""
        self.agent = SequencePlannerADKAgent()

        # Mock tool context
        self.mock_tool_context = Mock()
        self.mock_tool_context.state = {}

        # Sample features data
        self.sample_features = [
            {
                "id": "auth-001",
                "name": "User Authentication",
                "description": "Secure user login system",
                "requirements": ["Email login", "Password hashing", "JWT tokens"],
                "dependencies": [],
                "priority": 0,
            },
            {
                "id": "profile-001",
                "name": "User Profile",
                "description": "User profile management",
                "requirements": ["View profile", "Edit profile", "Profile picture"],
                "dependencies": ["User Authentication"],
                "priority": 1,
            },
            {
                "id": "dashboard-001",
                "name": "Dashboard",
                "description": "Main application dashboard",
                "requirements": [
                    "Overview widgets",
                    "Quick actions",
                    "Recent activity",
                ],
                "dependencies": ["User Authentication", "User Profile"],
                "priority": 1,
            },
        ]

    def test_agent_initialization(self):
        """Test that the SequencePlannerADKAgent initializes correctly."""
        assert self.agent.name == "marvin_sequence_planner_adk"
        assert self.agent.model == "gemini-1.5-pro"
        assert len(self.agent.tools) == 3
        assert self.agent.output_key == "last_sequence_plan"

    def test_calculate_complexity_score(self):
        """Test complexity score calculation for features."""
        simple_feature = {
            "requirements": ["Simple req"],
            "dependencies": [],
            "priority": 2,
            "description": "Simple feature",
        }
        assert _calculate_complexity_score(simple_feature) == 1

        complex_feature = {
            "requirements": ["Req 1", "Req 2", "Req 3"],
            "dependencies": ["Dep 1", "Dep 2"],
            "priority": 0,
            "description": "Complex API integration with security",
        }
        score = _calculate_complexity_score(complex_feature)
        assert score >= 8  # 3 reqs + 4 deps + 3 priority + 2 keywords

    def test_detect_circular_dependencies(self):
        """Test circular dependency detection."""
        # No circular dependencies
        graph_clean = {
            "A": {"dependencies": []},
            "B": {"dependencies": ["A"]},
            "C": {"dependencies": ["B"]},
        }
        circular = _detect_circular_dependencies(graph_clean)
        assert len(circular) == 0

        # With circular dependency
        graph_circular = {
            "A": {"dependencies": ["C"]},
            "B": {"dependencies": ["A"]},
            "C": {"dependencies": ["B"]},
        }
        circular = _detect_circular_dependencies(graph_circular)
        assert len(circular) > 0

    def test_topological_sort(self):
        """Test topological sorting for dependency resolution."""
        dependency_graph = {
            "auth": {"dependencies": [], "complexity": 2},
            "profile": {"dependencies": ["auth"], "complexity": 1},
            "dashboard": {"dependencies": ["auth", "profile"], "complexity": 3},
        }

        result = _topological_sort(dependency_graph)

        # Auth should come first (no dependencies)
        assert result.index("auth") < result.index("profile")
        assert result.index("profile") < result.index("dashboard")

    def test_analyze_feature_dependencies_tool(self):
        """Test the analyze_feature_dependencies tool."""
        features_json = json.dumps(self.sample_features)

        result = analyze_feature_dependencies(features_json, self.mock_tool_context)

        assert "dependency_graph" in result
        assert "complexity_scores" in result
        assert "recommended_sequence" in result
        assert len(result["recommended_sequence"]) == 3

        # Verify auth comes first (no dependencies)
        sequence = result["recommended_sequence"]
        auth_index = next(i for i, item in enumerate(sequence) if "auth" in item)
        assert auth_index == 0

    def test_create_task_breakdown_tool(self):
        """Test the create_task_breakdown tool."""
        feature_json = json.dumps(self.sample_features[0])

        result = create_task_breakdown(feature_json, 1, self.mock_tool_context)

        assert "tasks" in result
        assert "feature_id" in result
        assert len(result["tasks"]) >= 1

        # Check main task structure
        main_task = result["tasks"][0]
        assert main_task["task_id"] == "task-001"
        assert "subtasks" in main_task
        assert "estimated_effort" in main_task

    def test_validate_workflow_feasibility_tool(self):
        """Test the validate_workflow_feasibility tool."""
        workflow = {
            "tasks": [
                {
                    "task_id": "task-001",
                    "depends_on": [],
                    "estimated_effort": "1-2 days",
                },
                {
                    "task_id": "task-002",
                    "depends_on": ["task-001"],
                    "estimated_effort": "2-3 days",
                },
            ]
        }
        workflow_json = json.dumps(workflow)

        result = validate_workflow_feasibility(workflow_json, self.mock_tool_context)

        assert "is_feasible" in result
        assert "estimated_timeline" in result
        assert "risk_assessment" in result
        assert result["is_feasible"] is True

    def test_workflow_validation_with_missing_dependencies(self):
        """Test workflow validation catches missing dependencies."""
        workflow = {
            "tasks": [
                {
                    "task_id": "task-001",
                    "depends_on": ["nonexistent-task"],
                },
            ]
        }
        workflow_json = json.dumps(workflow)

        result = validate_workflow_feasibility(workflow_json, self.mock_tool_context)

        assert result["is_feasible"] is False
        assert len(result["issues"]) > 0

    def test_agent_capabilities(self):
        """Test that agent capabilities are properly defined."""
        capabilities = self.agent.get_planning_capabilities()

        assert "supported_features" in capabilities
        assert "analysis_tools" in capabilities
        assert "risk_factors_considered" in capabilities
        assert len(capabilities["supported_features"]) > 0


class TestMarvinOrchestratorADK:
    """Test cases for the MarvinOrchestratorADKAgent."""

    def setup_method(self):
        """Set up test fixtures."""
        self.agent = MarvinOrchestratorADKAgent()

        # Mock tool context
        self.mock_tool_context = Mock()
        self.mock_tool_context.state = {}

        # Sample PRD content
        self.sample_prd_content = """# PRD: Test Application

Version: 1.0.0
Author: Test Team

## Features

### Feature 1: User Authentication
Users can log in securely.

**Requirements:**
- Email authentication
- Password security
- Session management
"""

    def test_orchestrator_initialization(self):
        """Test that the MarvinOrchestratorADKAgent initializes correctly."""
        assert self.agent.name == "marvin_orchestrator_adk"
        assert self.agent.model == "gemini-1.5-pro"
        assert len(self.agent.tools) == 4
        assert len(self.agent.sub_agents) == 2
        assert self.agent.output_key == "marvin_workflow_result"

    def test_orchestrator_capabilities(self):
        """Test orchestrator capabilities reporting."""
        capabilities = self.agent.get_orchestrator_capabilities()

        assert "workflow_steps" in capabilities
        assert "supported_formats" in capabilities
        assert "ai_assistants_supported" in capabilities
        assert "sub_agents" in capabilities
        assert "tools" in capabilities
        assert "safety_features" in capabilities

        # Verify sub-agents
        assert len(capabilities["sub_agents"]) == 2
        assert any(
            agent["name"] == "DocumentAnalyzer" for agent in capabilities["sub_agents"]
        )

    @patch("marvin.adapters.adk_agents.marvin_orchestrator_adk.DocumentAnalysisAgent")
    def test_analyze_prd_document_tool(self, mock_analyzer_class):
        """Test the analyze_prd_document tool."""
        # Mock the analyzer with async support
        mock_analyzer = Mock()
        mock_analyzer_class.return_value = mock_analyzer

        # Create sample PRD and features
        sample_prd = PRD(
            id="prd-001",
            title="Test App",
            description="Test application",
            author="Test Team",
            version="1.0.0",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        sample_features = [
            Feature(
                id="auth-001",
                name="Authentication",
                description="User auth",
                requirements=["Login", "Logout"],
                status=FeatureStatus.PROPOSED,
            )
        ]

        # Configure async mock to return our sample data
        mock_analyzer.execute = AsyncMock(return_value=(sample_prd, sample_features))

        # Create temporary PRD file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(self.sample_prd_content)
            temp_path = f.name

        try:
            # Test the tool
            result = analyze_prd_document(temp_path, self.mock_tool_context)

            assert result["success"] is True
            assert "prd" in result
            assert "features" in result
            assert result["prd"]["title"] == "Test App"
            assert len(result["features"]) == 1

            # Verify state was updated
            assert "last_prd_analysis" in self.mock_tool_context.state

        finally:
            # Clean up
            Path(temp_path).unlink()

    def test_generate_xml_templates_tool(self):
        """Test the generate_xml_templates tool."""
        # Sample data
        features_data = json.dumps(
            [
                {
                    "id": "auth-001",
                    "name": "Authentication",
                    "description": "User authentication",
                    "requirements": ["Login", "Logout"],
                    "dependencies": [],
                    "priority": 0,
                    "status": "proposed",
                }
            ]
        )

        prd_data = json.dumps(
            {
                "id": "prd-001",
                "title": "Test App",
                "description": "Test application",
                "author": "Test Team",
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            result = generate_xml_templates(
                features_data, prd_data, temp_dir, self.mock_tool_context
            )

            assert result["success"] is True
            assert result["templates_generated"] == 1
            assert "templates" in result

            # Verify template file was created
            template = result["templates"][0]
            template_path = Path(template["template_path"])
            assert template_path.exists()
            assert template["is_valid"] is True

    def test_create_project_workflow_tool(self):
        """Test the create_project_workflow tool."""
        features_data = json.dumps(
            [
                {
                    "id": "auth-001",
                    "name": "Authentication",
                    "requirements": ["Login", "Security"],
                    "dependencies": [],
                },
                {
                    "id": "profile-001",
                    "name": "Profile",
                    "requirements": ["View", "Edit"],
                    "dependencies": ["Authentication"],
                },
            ]
        )

        prd_data = json.dumps(
            {
                "id": "prd-001",
                "title": "Test App",
            }
        )

        result = create_project_workflow(
            features_data, prd_data, self.mock_tool_context
        )

        assert result["success"] is True
        assert "workflow" in result
        assert result["phases_count"] >= 1

        workflow = result["workflow"]
        assert "phases" in workflow
        assert "estimated_timeline" in workflow
        assert "risk_assessment" in workflow

    def test_generate_project_summary_tool(self):
        """Test the generate_project_summary tool."""
        # Set up mock state
        self.mock_tool_context.state = {
            "last_prd_analysis": {
                "prd": {"title": "Test App", "author": "Test Team"},
                "features": [{"name": "Auth"}],
                "analysis_timestamp": datetime.now().isoformat(),
            },
            "last_template_generation": {
                "templates_generated": 1,
                "templates": [{"is_valid": True}],
                "output_directory": "/tmp/test",
            },
            "project_workflow": {
                "phases_count": 2,
                "workflow": {
                    "estimated_timeline": "4 weeks",
                    "risk_assessment": "Low Risk",
                },
            },
        }

        result = generate_project_summary(self.mock_tool_context)

        assert result["success"] is True
        assert "summary" in result

        summary = result["summary"]
        assert "project_overview" in summary
        assert "implementation_plan" in summary
        assert "deliverables" in summary
        assert "next_steps" in summary

    def test_process_prd_complete_initialization(self):
        """Test the process_prd_complete method initialization."""
        mock_session = Mock()
        mock_session.state = {}

        result = self.agent.process_prd_complete(
            document_path="/test/prd.md",
            output_directory="/test/output",
            session=mock_session,
        )

        assert result["status"] == "initialized"
        assert result["document_path"] == "/test/prd.md"
        assert result["output_directory"] == "/test/output"

        # Verify session state was set
        assert "input_document" in mock_session.state
        assert "output_directory" in mock_session.state

    def test_error_handling_in_tools(self):
        """Test error handling in orchestrator tools."""
        # Test with invalid JSON
        result = create_project_workflow("invalid json", "{}", self.mock_tool_context)

        assert result["success"] is False
        assert "error" in result

        # Verify error was stored in state
        assert "last_workflow_error" in self.mock_tool_context.state


class TestADKAgentIntegration:
    """Integration tests for ADK agents working together."""

    def setup_method(self):
        """Set up integration test fixtures."""
        self.orchestrator = MarvinOrchestratorADKAgent()
        self.sequence_planner = SequencePlannerADKAgent()

    def test_agent_communication_pattern(self):
        """Test that agents can work together through state management."""
        # Simulate orchestrator setting up initial state

        # Verify both agents can access shared capabilities
        orchestrator_caps = self.orchestrator.get_orchestrator_capabilities()
        planner_caps = self.sequence_planner.get_planning_capabilities()

        assert "workflow_steps" in orchestrator_caps
        assert "supported_features" in planner_caps

        # Verify tool compatibility
        orchestrator_tools = {tool.__name__ for tool in self.orchestrator.tools}
        expected_tools = {
            "analyze_prd_document",
            "generate_xml_templates",
            "create_project_workflow",
            "generate_project_summary",
        }
        assert orchestrator_tools == expected_tools

    def test_workflow_state_consistency(self):
        """Test that workflow state remains consistent across agent interactions."""
        mock_tool_context = Mock()
        mock_tool_context.state = {}

        # Simulate workflow steps
        features_data = json.dumps(
            [
                {
                    "id": "auth",
                    "name": "Auth",
                    "requirements": ["Login"],
                    "dependencies": [],
                }
            ]
        )

        # Step 1: Analyze dependencies
        analyze_feature_dependencies(features_data, mock_tool_context)
        assert "last_dependency_analysis" in mock_tool_context.state

        # Step 2: Create task breakdown
        create_task_breakdown(
            json.dumps({"id": "auth", "name": "Auth"}), 1, mock_tool_context
        )
        assert "task_breakdowns" in mock_tool_context.state

        # Verify state consistency
        assert len(mock_tool_context.state) >= 2
        assert mock_tool_context.state["last_dependency_analysis"][
            "recommended_sequence"
        ]
        assert mock_tool_context.state["task_breakdowns"]["auth"]

    @pytest.mark.asyncio
    async def test_end_to_end_workflow_simulation(self):
        """Test a simulated end-to-end workflow."""
        # This test simulates how the agents would work together
        # in a real workflow without requiring actual LLM calls

        # Mock session
        mock_session = Mock()
        mock_session.state = {}

        # Step 1: Initialize workflow
        result = self.orchestrator.process_prd_complete(
            document_path="/test/prd.md",
            output_directory="/test/output",
            session=mock_session,
        )

        assert result["status"] == "initialized"

        # Step 2: Verify session state setup
        assert "input_document" in mock_session.state
        assert "output_directory" in mock_session.state
        assert "workflow_start_time" in mock_session.state

        # Step 3: Verify agent readiness
        assert len(self.orchestrator.sub_agents) == 2
        assert self.orchestrator.output_key == "marvin_workflow_result"

        # This confirms the workflow structure is ready for actual execution
