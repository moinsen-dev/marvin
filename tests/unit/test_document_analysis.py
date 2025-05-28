"""Tests for the DocumentAnalysisAgent."""

import os
import sys
import unittest
from datetime import datetime
from unittest.mock import patch

import pytest

# Add path to src directory
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
)

from marvin.core.agents.document_analysis import DocumentAnalysisAgent
from marvin.core.domain.models import PRD, Feature


class TestDocumentAnalysisAgent(unittest.TestCase):
    """Test class for the DocumentAnalysisAgent."""

    def setUp(self):
        """Set up test environment."""
        self.agent = DocumentAnalysisAgent()
        self.test_md_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../examples/prd/example_prd.md")
        )

    @pytest.mark.asyncio
    async def test_analyze_markdown(self):
        """Test for analyzing a Markdown PRD."""
        # Only test if the test file exists
        if not os.path.exists(self.test_md_path):
            self.skipTest(f"Test file not found: {self.test_md_path}")

        # Perform test
        prd, features = await self.agent._analyze_markdown(
            self.test_md_path,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        # Assertions
        self.assertIsInstance(prd, PRD)
        self.assertIsInstance(features, list)
        self.assertTrue(all(isinstance(f, Feature) for f in features))
        self.assertEqual(prd.title, "Example PRD: Task Management")
        self.assertGreater(len(features), 0)

    @pytest.mark.asyncio
    async def test_execute_with_nonexistent_file(self):
        """Test for execution with a non-existent file."""
        with self.assertRaises(FileNotFoundError):
            await self.agent.execute("nonexistent_file.md")

    @pytest.mark.asyncio
    async def test_execute_with_unsupported_format(self):
        """Test for execution with an unsupported format."""
        mock_path = "test.xyz"
        with patch("os.path.exists", return_value=True):
            with self.assertRaises(ValueError):
                await self.agent.execute(mock_path)


if __name__ == "__main__":
    unittest.main()
