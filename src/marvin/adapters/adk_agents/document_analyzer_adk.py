"""ADK Agent for analyzing Product Requirements Documents (PRDs)."""

import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types

# Import domain models
from marvin.core.domain.models import PRD, Feature

# Placeholder for potential ADK tools if complex parsing logic needs to be toolified
# from google.adk.tools import FunctionTool


# Content filter callback for inappropriate content
def content_filter(
    context: CallbackContext, llm_request: LlmRequest
) -> LlmResponse | None:
    """Implements a content filter guardrail to prevent processing of inappropriate content."""
    FORBIDDEN_WORDS = ["confidential", "private", "secret", "internal"]

    # Extract the text from the latest user message
    last_user_message_text = ""
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.role == "user" and content.parts:
                if content.parts[0].text:
                    last_user_message_text = content.parts[0].text
                    break

    # Check for forbidden words
    for word in FORBIDDEN_WORDS:
        if word.lower() in last_user_message_text.lower():
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(
                            text=f"I cannot process documents containing '{word}' content. Please ensure the document is appropriate for analysis."
                        )
                    ],
                )
            )
    return None


class DocumentAnalyzerADKAgent(LlmAgent):
    """
    ADK Agent for analyzing PRDs using an LLM, extracting features, requirements,
    and other relevant information.
    """

    def __init__(
        self,
        name: str = "marvin_document_analyzer_adk",
        model: str = "gemini-pro",
        config: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        """Initializes the DocumentAnalyzerADKAgent.

        Args:
            name: Name of the agent.
            model: The LLM model to use (e.g., "gemini-pro", "gemini-1.5-flash").
            config: Optional dictionary for additional configurations.
            **kwargs: Additional arguments for the LlmAgent base class.
        """
        # Initialize a logger compatible with how ADK agents might expect it or use your own
        # ADK LlmAgent has its own self.logger, so this might be redundant unless for specific pre/post processing
        # self.custom_logger = get_logger(f"adk_agent.{name}") # Example if needed

        # Define the detailed instruction for the LLM
        instruction = (
            "You are an expert assistant specialized in analyzing Product Requirements Documents (PRDs). "
            "Your task is to meticulously read the provided PRD text and extract structured information. "
            "Specifically, identify the main title of the PRD, its version (if mentioned), and the author (if mentioned). "
            "Also extract a general description of the PRD if one is apparent (e.g., from an overview section). "
            "Then, extract all distinct features. For each feature, provide: "
            "1. A concise name for the feature. "
            "2. A detailed description of the feature. "
            "3. A list of specific requirements associated with that feature. "
            "4. A list of any dependencies this feature has on other features (if explicitly stated). "
            "Format your entire output as a single, valid JSON object. "
            "The JSON object should have top-level keys: 'prd_title', 'prd_version', 'prd_author', 'prd_description', and 'features'. "
            "The 'features' key should hold a list of objects, where each object represents a feature and contains "
            "the keys: 'name', 'description', 'requirements' (as a list of strings), and 'dependencies' (as a list of strings). "
            "If a piece of information (like version, author, description, or dependencies) is not found or is not applicable, use an empty string for string fields or an empty list for list fields in the JSON."
        )

        super().__init__(
            name=name,
            model=model,
            instruction=instruction,
            description="An ADK agent that analyzes PRD documents to extract structured information like title, version, features, requirements, and dependencies.",
            before_model_callback=content_filter,  # Add content filter guardrail
            output_key="last_analysis_result",  # Automatically save analysis results to state
            # tools=[], # Add any ADK tools if needed later
            **kwargs,
        )
        self.config = config or {}
        self.logger.info(
            f"Initialized DocumentAnalyzerADKAgent '{self.name}' with model '{self.model}'"
        )

    async def _read_document_content(
        self, document_path: str, tool_context: Any | None = None
    ) -> str:
        """
        Reads the content of the document based on its extension.
        Currently supports Markdown. PDF and Word can be added.
        """
        self.logger.info(f"Reading document content from: {document_path}")
        if not os.path.exists(document_path):
            self.logger.error(f"Document not found: {document_path}")
            raise FileNotFoundError(f"Document not found: {document_path}")

        file_ext = Path(document_path).suffix.lower()
        content = ""

        try:
            if file_ext == ".md":
                self.logger.debug(f"Processing Markdown document: {document_path}")
                with open(document_path, encoding="utf-8") as f:
                    content = f.read()

                # Update state if tool_context is provided
                if tool_context:
                    tool_context.state["last_processed_file"] = document_path
                    tool_context.state["last_processed_time"] = (
                        datetime.now().isoformat()
                    )
            # elif file_ext in [".docx", ".doc"]:
            # self.logger.warning("Word document reading not yet fully implemented in ADK agent. Placeholder.")
            # raise NotImplementedError("Word document reading needs a library like python-docx")
            # elif file_ext == ".pdf":
            # self.logger.warning("PDF document reading not yet fully implemented in ADK agent. Placeholder.")
            # raise NotImplementedError("PDF document reading needs a library like PyPDF2 or pdfplumber")
            else:
                error_msg = f"Unsupported document format: {file_ext}. ADK agent currently supports .md"
                self.logger.error(error_msg)
                raise ValueError(error_msg)

            self.logger.debug(
                f"Successfully read {len(content)} characters from {document_path}"
            )
            return content
        except Exception as e:
            self.logger.error(f"Error reading document {document_path}: {str(e)}")
            raise

    async def _parse_llm_response(self, llm_output: str) -> tuple[PRD, list[Feature]]:
        """
        Parses the structured JSON output from the LLM into PRD and Feature domain models.
        """
        self.logger.info("Parsing LLM response.")
        self.logger.debug(f"Raw LLM output: {llm_output[:500]}...")

        try:
            import json

            data = json.loads(llm_output)
            current_time = datetime.now()

            # Create PRD object
            prd_id = data.get("prd_id", "generated_prd_" + str(int(time.time())))
            prd = PRD(
                id=prd_id,
                title=data.get("prd_title") or "Unknown PRD Title",
                description=data.get("prd_description") or "",
                author=data.get("prd_author") or "Unknown Author",
                version=data.get("prd_version") or "0.0.0",
                created_at=current_time,
                updated_at=current_time,
            )

            extracted_features: list[Feature] = []
            for i, feature_data in enumerate(data.get("features", [])):
                feature = Feature(
                    id=feature_data.get("id", f"{prd_id}_feature_{i:02d}"),
                    name=feature_data.get("name") or f"Unnamed Feature {i + 1}",
                    description=feature_data.get("description") or "",
                    requirements=feature_data.get("requirements", []),
                    dependencies=feature_data.get("dependencies", []),
                )
                extracted_features.append(feature)

            prd.features = extracted_features

            self.logger.info(
                f"Successfully parsed LLM response into PRD '{prd.title}' with {len(extracted_features)} features."
            )
            return prd, extracted_features

        except json.JSONDecodeError as e:
            self.logger.error(
                f"Failed to decode LLM JSON output: {str(e)}\nOutput was: {llm_output}"
            )
            raise ValueError(f"LLM output was not valid JSON: {str(e)}") from e
        except Exception as e:
            self.logger.error(
                f"Error parsing LLM response into domain models: {str(e)}"
            )
            raise

    async def analyze_prd_file(
        self, document_path: str, **kwargs: Any
    ) -> tuple[PRD, list[Feature]]:
        """
        Analyzes a PRD document file by reading its content, invoking the LLM
        via ADK, and parsing the response into structured domain objects.

        Args:
            document_path: Path to the PRD document file.
            **kwargs: Additional parameters (currently not used but placeholder for future).

        Returns:
            A tuple containing the PRD domain object and a list of Feature domain objects.

        Raises:
            FileNotFoundError: If the document_path does not exist.
            ValueError: If the document format is unsupported or LLM output is unparsable.
            Exception: For other underlying errors during processing.
        """
        self.logger.info(f"Starting ADK PRD analysis for file: {document_path}")

        try:
            # Step 1: Read document content
            document_content = await self._read_document_content(document_path)
            if not document_content.strip():
                self.logger.warning(
                    f"Document is empty or contains only whitespace: {document_path}"
                )
                current_time = datetime.now()
                empty_prd = PRD(
                    id=Path(document_path).stem + "_empty",
                    title=f"Empty Document: {Path(document_path).name}",
                    description="Document was empty or contained only whitespace.",
                    author="System",
                    created_at=current_time,
                    updated_at=current_time,
                    version="0.0.0",
                    features=[],
                )
                return empty_prd, []

            # Step 2: Invoke the ADK agent (LLM call)
            self.logger.info(
                f"Invoking LLM for document analysis. Content length: {len(document_content)}"
            )

            llm_response_obj = await self.invoke(
                request_body={"document_text": document_content}
            )

            if llm_response_obj is None or llm_response_obj.content is None:
                self.logger.error(
                    "LLM invocation returned a null response or null content."
                )
                raise ValueError("LLM failed to return a valid response.")

            llm_text_output = llm_response_obj.content
            self.logger.info("LLM invocation successful. Proceeding to parse response.")

            # Step 3: Parse LLM response into domain models
            prd, features = await self._parse_llm_response(llm_text_output)

            self.logger.info(
                f"Successfully analyzed PRD: {document_path}. Title: {prd.title}"
            )
            return prd, features

        except FileNotFoundError:
            # Already logged in _read_document_content, re-raise
            raise
        except ValueError as ve:
            # Already logged (e.g. unsupported format, JSON parsing error), re-raise
            self.logger.error(f"Value error during PRD analysis: {str(ve)}")
            raise
        except Exception as e:
            self.logger.error(
                f"An unexpected error occurred during ADK PRD analysis for {document_path}: {str(e)}"
            )
            # Log the full traceback if possible in a real scenario
            # import traceback
            # self.logger.error(traceback.format_exc())
            raise


# Example usage (for testing purposes, would not be in the agent file itself)
# async def main():
#     # This requires google-adk to be installed and potentially model configuration
#     # (e.g., GOOGLE_API_KEY environment variable for Gemini)
#
#     # Create a dummy markdown PRD file for testing
#     dummy_prd_path = "./dummy_prd.md"
#     with open(dummy_prd_path, "w") as f:
#         f.write("# My Awesome Product\n")
#         f.write("Version: 2.0\nAuthor: AI Developer\n\n")
#         f.write("## Feature One\n")
#         f.write("This is the first feature.\n")
#         f.write("- Requirement 1.1\n- Requirement 1.2\n")
#         f.write("Depends on: Feature Two\n\n")
#         f.write("## Feature Two\n")
#         f.write("This is the second feature.\n")
#         f.write("- Requirement 2.1\n")
#
#     analyzer_agent = DocumentAnalyzerADKAgent(model="gemini-1.5-flash-latest") # Use a specific model
#
#     try:
#         print(f"Analyzing {dummy_prd_path}...")
#         prd_result, features_result = await analyzer_agent.analyze_prd_file(dummy_prd_path)
#         print("\n--- PRD Result ---")
#         print(f"ID: {prd_result.id}")
#         print(f"Title: {prd_result.title}")
#         print(f"Version: {prd_result.version}")
#         print(f"Author: {prd_result.author}")
#         print(f"Description: {prd_result.description}")
#
#         print("\n--- Features --- (" + str(len(features_result)) + ")")
#         for i, feature in enumerate(features_result):
#             print(f"\nFeature {i+1}:")
#             print(f"  ID: {feature.id}")
#             print(f"  Name: {feature.name}")
#             print(f"  Description: {feature.description}")
#             print(f"  Requirements: {feature.requirements}")
#             print(f"  Dependencies: {feature.dependencies}")
#
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         import traceback
#         traceback.print_exc()
#     finally:
#         if os.path.exists(dummy_prd_path):
#             os.remove(dummy_prd_path)

# if __name__ == "__main__":
#     import asyncio
#     # To run this example:
#     # 1. Ensure GOOGLE_API_KEY is set if using Gemini, or your model is configured.
#     # 2. Run `python -m marvin.adapters.adk_agents.document_analyzer_adk`
#     #    (adjust path based on your project structure and how you run Python modules)
#     # Or, if running this file directly and it's not part of a package structure recognized
#     # by Python's module system in the current context, you might need to adjust PYTHONPATH
#     # or run it as a script: `python path/to/document_analyzer_adk.py`
#     asyncio.run(main())

"""
# Note: The example usage (main function) is commented out as it's for illustrative/testing purposes.
# The core ADK agent implementation is the class DocumentAnalyzerADKAgent.
# The _read_document_content method has placeholders for .docx and .pdf.
# The _parse_llm_response method implements basic JSON parsing based on the specified instruction format.
# Error handling and logging are included.
# The `marvin.logging` import assumes your logger is accessible; adjust if necessary.
# ADK LlmAgent already provides `self.logger`, so using a custom one via `get_logger`
# might be for specific logging needs outside of the ADK agent's direct operational logs.
# I've kept the custom logger line commented for now.
# The `invoke` method of `LlmAgent` is used, assuming `request_body` is the correct parameter name
# for passing the input dictionary. Please verify with ADK documentation if `request_body` is standard
# or if it should be `input` or another parameter.
# For `gemini-pro` or `gemini-1.5-flash-latest` ensure that the necessary API keys/authentication is set up in your environment.
"""


# Example usage and setup
def setup_document_analyzer(
    app_name: str = "prd_analyzer",
    user_id: str = "default_user",
    session_id: str = "default_session",
) -> tuple[DocumentAnalyzerADKAgent, Runner]:
    """
    Sets up the document analyzer agent with proper session management.

    Returns:
        A tuple of (agent, runner) ready for use.
    """
    # Initialize session service
    session_service = InMemorySessionService()

    # Create session
    session_service.create_session(
        app_name=app_name, user_id=user_id, session_id=session_id
    )

    # Create agent
    agent = DocumentAnalyzerADKAgent()

    # Create runner
    runner = Runner(agent=agent, app_name=app_name, session_service=session_service)

    return agent, runner
