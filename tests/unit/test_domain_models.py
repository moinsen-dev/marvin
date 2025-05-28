"""
Unit tests for domain models.

Following TDD approach - write tests first, then implement.
"""

from datetime import datetime

from marvin.core.domain.models import (
    PRD,
    Codebase,
    Component,
    Feature,
    FeatureStatus,
    Task,
    TaskStatus,
    Workflow,
)


class TestFeatureModel:
    """Test cases for Feature domain model."""

    def test_feature_creation_with_minimal_data(self):
        """Test that a feature can be created with minimal required data."""
        feature = Feature(
            id="feat-001",
            name="User Authentication",
            description="Users can log in to the system",
        )

        assert feature.id == "feat-001"
        assert feature.name == "User Authentication"
        assert feature.description == "Users can log in to the system"
        assert feature.status == FeatureStatus.PROPOSED
        assert feature.priority == 0
        assert feature.requirements == []
        assert feature.dependencies == []

    def test_feature_creation_with_full_data(self):
        """Test that a feature can be created with all fields."""
        feature = Feature(
            id="feat-002",
            name="Task Management",
            description="Users can manage tasks",
            requirements=["REQ-1", "REQ-2"],
            dependencies=["feat-001"],
            status=FeatureStatus.ACCEPTED,
            priority=1,
            estimated_effort="2 weeks",
            tags=["core", "mvp"],
        )

        assert feature.id == "feat-002"
        assert feature.requirements == ["REQ-1", "REQ-2"]
        assert feature.dependencies == ["feat-001"]
        assert feature.status == FeatureStatus.ACCEPTED
        assert feature.priority == 1
        assert feature.estimated_effort == "2 weeks"
        assert feature.tags == ["core", "mvp"]


class TestPRDModel:
    """Test cases for PRD domain model."""

    def test_prd_creation(self):
        """Test that a PRD can be created with required fields."""
        now = datetime.now()
        prd = PRD(
            id="prd-001",
            title="Task Management System",
            description="A system for managing tasks",
            author="Test Author",
            created_at=now,
            updated_at=now,
            version="1.0.0",
        )

        assert prd.id == "prd-001"
        assert prd.title == "Task Management System"
        assert prd.author == "Test Author"
        assert prd.version == "1.0.0"
        assert prd.features == []
        assert prd.tags == []

    def test_prd_add_feature(self):
        """Test that features can be added to a PRD."""
        now = datetime.now()
        prd = PRD(
            id="prd-001",
            title="Task Management System",
            description="A system for managing tasks",
            author="Test Author",
            created_at=now,
            updated_at=now,
            version="1.0.0",
        )

        feature = Feature(
            id="feat-001", name="User Authentication", description="Users can log in"
        )

        # Store original updated_at
        original_updated = prd.updated_at

        # Add feature
        prd.add_feature(feature)

        assert len(prd.features) == 1
        assert prd.features[0] == feature
        assert prd.updated_at > original_updated


class TestCodebaseModel:
    """Test cases for Codebase domain model."""

    def test_codebase_creation(self):
        """Test that a codebase can be created."""
        codebase = Codebase(
            id="cb-001", name="sample-project", root_path="/path/to/project"
        )

        assert codebase.id == "cb-001"
        assert codebase.name == "sample-project"
        assert codebase.root_path == "/path/to/project"
        assert codebase.components == []
        assert codebase.technologies == []
        assert isinstance(codebase.scanned_at, datetime)

    def test_codebase_add_component(self):
        """Test that components can be added to a codebase."""
        codebase = Codebase(
            id="cb-001", name="sample-project", root_path="/path/to/project"
        )

        component = Component(
            name="main.py",
            path="/path/to/project/src/main.py",
            type="file",
            description="Main entry point",
        )

        codebase.add_component(component)

        assert len(codebase.components) == 1
        assert codebase.components[0] == component


class TestTaskModel:
    """Test cases for Task domain model."""

    def test_task_creation(self):
        """Test that a task can be created."""
        task = Task(
            task_id="task-001",
            sequence_number=1,
            name="Implement login",
            description="Implement user login functionality",
            feature_id="feat-001",
        )

        assert task.task_id == "task-001"
        assert task.sequence_number == 1
        assert task.name == "Implement login"
        assert task.feature_id == "feat-001"
        assert task.status == TaskStatus.PLANNED
        assert task.depends_on == []
        assert isinstance(task.created_at, datetime)

    def test_task_is_blocked_property(self):
        """Test that is_blocked property works correctly."""
        task = Task(
            task_id="task-001",
            sequence_number=1,
            name="Implement login",
            description="Implement user login functionality",
            feature_id="feat-001",
        )

        assert not task.is_blocked

        task.status = TaskStatus.BLOCKED
        assert task.is_blocked


class TestWorkflowModel:
    """Test cases for Workflow domain model."""

    def test_workflow_creation(self):
        """Test that a workflow can be created."""
        workflow = Workflow(
            id="wf-001",
            name="MVP Implementation",
            description="Workflow for MVP features",
            prd_id="prd-001",
        )

        assert workflow.id == "wf-001"
        assert workflow.name == "MVP Implementation"
        assert workflow.prd_id == "prd-001"
        assert workflow.tasks == []
        assert workflow.codebase_id is None

    def test_workflow_add_task_maintains_order(self):
        """Test that tasks are kept in sequence order when added."""
        workflow = Workflow(
            id="wf-001",
            name="MVP Implementation",
            description="Workflow for MVP features",
            prd_id="prd-001",
        )

        # Add tasks out of order
        task2 = Task(
            task_id="task-002",
            sequence_number=2,
            name="Task 2",
            description="Second task",
            feature_id="feat-001",
        )
        task1 = Task(
            task_id="task-001",
            sequence_number=1,
            name="Task 1",
            description="First task",
            feature_id="feat-001",
        )
        task3 = Task(
            task_id="task-003",
            sequence_number=3,
            name="Task 3",
            description="Third task",
            feature_id="feat-002",
        )

        # Store original updated_at
        original_updated = workflow.updated_at

        # Add tasks in random order
        workflow.add_task(task2)
        workflow.add_task(task3)
        workflow.add_task(task1)

        # Verify tasks are sorted by sequence number
        assert len(workflow.tasks) == 3
        assert workflow.tasks[0].task_id == "task-001"
        assert workflow.tasks[1].task_id == "task-002"
        assert workflow.tasks[2].task_id == "task-003"
        assert workflow.updated_at > original_updated
