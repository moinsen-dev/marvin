"""Gemini API client for AI operations."""

import json
import os
from typing import Any, Optional

import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory


class GeminiClient:
    """Client for interacting with Google's Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None) -> None:
        """Initialize the Gemini client."""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required")
        
        genai.configure(api_key=self.api_key)
        
        # Configure generation settings
        self.generation_config = genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=8192,
            candidate_count=1,
        )
        
        # Configure safety settings
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
        
        # Initialize models
        self.flash_model = genai.GenerativeModel(
            "gemini-2.0-flash-exp",
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
        )
        
        self.pro_model = genai.GenerativeModel(
            "gemini-1.5-pro",
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
        )
    
    async def extract_features(self, prd_content: str) -> list[dict[str, Any]]:
        """Extract features from PRD content using AI."""
        prompt = self._build_feature_extraction_prompt(prd_content)
        
        response = await self.flash_model.generate_content_async(prompt)
        return self._parse_json_response(response.text)
    
    async def analyze_codebase(self, file_contents: dict[str, str]) -> dict[str, Any]:
        """Analyze codebase structure and extract insights."""
        prompt = self._build_codebase_analysis_prompt(file_contents)
        
        response = await self.pro_model.generate_content_async(prompt)
        return self._parse_json_response(response.text)
    
    async def generate_task_sequence(self, features: list[dict], codebase_info: Optional[dict] = None) -> list[dict]:
        """Generate an optimal task sequence from features."""
        prompt = self._build_task_sequence_prompt(features, codebase_info)
        
        response = await self.pro_model.generate_content_async(prompt)
        return self._parse_json_response(response.text)
    
    async def generate_xml_template(self, task: dict, context: dict) -> str:
        """Generate XML template for a specific task."""
        prompt = self._build_template_generation_prompt(task, context)
        
        response = await self.flash_model.generate_content_async(prompt)
        return response.text.strip()
    
    def _build_feature_extraction_prompt(self, prd_content: str) -> str:
        """Build prompt for feature extraction."""
        return f"""Analyze the following PRD document and extract all features.

For each feature, provide:
- name: Feature name
- description: Detailed description
- requirements: List of specific requirements
- user_stories: User stories in standard format
- priority: critical/high/medium/low
- dependencies: List of other feature names this depends on
- estimated_effort: Time estimate (e.g., "2 weeks", "1 month")

Return the result as a JSON array.

PRD Content:
{prd_content}

JSON Response:"""
    
    def _build_codebase_analysis_prompt(self, file_contents: dict[str, str]) -> str:
        """Build prompt for codebase analysis."""
        files_summary = "\n".join([f"File: {path}\n{content[:500]}..." for path, content in file_contents.items()])
        
        return f"""Analyze the following codebase structure and content.

Identify:
- Primary programming language and version
- Frameworks and major libraries used
- Architecture patterns (MVC, hexagonal, etc.)
- Entry points (main files, APIs, services)
- Key components and their relationships

Files:
{files_summary}

Return the analysis as JSON with structure:
{{
  "primary_language": {{}},
  "frameworks": [],
  "libraries": [],
  "architecture_patterns": [],
  "entry_points": [],
  "components": []
}}"""
    
    def _build_task_sequence_prompt(self, features: list[dict], codebase_info: Optional[dict]) -> str:
        """Build prompt for task sequence generation."""
        context = "greenfield project" if not codebase_info else f"existing codebase with {codebase_info.get('primary_language', {}).get('name', 'unknown')} stack"
        
        return f"""Create an optimal sequence of AI coding tasks for implementing these features in a {context}.

Features:
{json.dumps(features, indent=2)}

For each task provide:
- task_id: Unique identifier
- name: Clear task name
- description: What needs to be done
- type: implementation/refactoring/testing/documentation
- dependencies: List of task_ids that must be completed first
- estimated_time: Time estimate
- files_to_modify: Existing files to change
- files_to_create: New files to create

Consider dependencies and create a logical implementation order.

Return as JSON array ordered by execution sequence."""
    
    def _build_template_generation_prompt(self, task: dict, context: dict) -> str:
        """Build prompt for XML template generation."""
        return f"""Generate an XML template for the following AI coding task.

Task Details:
{json.dumps(task, indent=2)}

Context:
{json.dumps(context, indent=2)}

Create a well-structured XML template that an AI coding assistant can use to implement this task.
Include clear instructions, acceptance criteria, and any relevant code examples.

XML Template:"""
    
    def _parse_json_response(self, response: str) -> Any:
        """Parse JSON from AI response."""
        # Extract JSON from response (handle markdown code blocks)
        if "```json" in response:
            json_str = response.split("```json")[1].split("```")[0]
        elif "```" in response:
            json_str = response.split("```")[1].split("```")[0]
        else:
            json_str = response
        
        try:
            return json.loads(json_str.strip())
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {e}")
