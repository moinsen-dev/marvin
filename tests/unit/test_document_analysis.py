"""Tests für den DocumentAnalysisAgent."""

import os
import sys
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

import pytest

# Pfad zum src-Verzeichnis hinzufügen
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

from marvin.core.agents.document_analysis import DocumentAnalysisAgent
from marvin.core.domain.models import Feature, PRD


class TestDocumentAnalysisAgent(unittest.TestCase):
    """Testklasse für den DocumentAnalysisAgent."""
    
    def setUp(self):
        """Testumgebung einrichten."""
        self.agent = DocumentAnalysisAgent()
        self.test_md_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../examples/prd/example_prd.md")
        )
    
    @pytest.mark.asyncio
    async def test_analyze_markdown(self):
        """Test für die Analyse eines Markdown-PRDs."""
        # Nur testen, wenn die Testdatei existiert
        if not os.path.exists(self.test_md_path):
            self.skipTest(f"Testdatei nicht gefunden: {self.test_md_path}")
        
        # Test durchführen
        prd, features = await self.agent._analyze_markdown(
            self.test_md_path,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        
        # Assertions
        self.assertIsInstance(prd, PRD)
        self.assertIsInstance(features, list)
        self.assertTrue(all(isinstance(f, Feature) for f in features))
        self.assertEqual(prd.title, "Beispiel-PRD: Aufgabenverwaltung")
        self.assertGreater(len(features), 0)
    
    @pytest.mark.asyncio
    async def test_execute_with_nonexistent_file(self):
        """Test für die Ausführung mit nicht existierender Datei."""
        with self.assertRaises(FileNotFoundError):
            await self.agent.execute("nonexistent_file.md")
    
    @pytest.mark.asyncio
    async def test_execute_with_unsupported_format(self):
        """Test für die Ausführung mit nicht unterstütztem Format."""
        mock_path = "test.xyz"
        with patch("os.path.exists", return_value=True):
            with self.assertRaises(ValueError):
                await self.agent.execute(mock_path)


if __name__ == "__main__":
    unittest.main()
