"""
Base module for Marvin agents.

Contains common configurations and utilities used by all Marvin agents.
"""

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService

# Constants
APP_NAME = "marvin"
USER_ID = "marvin_user"
DEFAULT_SESSION_ID = "default_session"

# Model configurations
MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
MODEL_GEMINI_2_0_PRO = "gemini-2.0-pro"

# Session service for all agents
session_service = InMemorySessionService()


def create_runner(agent: Agent, session_id: str = DEFAULT_SESSION_ID) -> Runner:
    """
    Create a runner for the specified agent.

    Args:
        agent: The agent to create a runner for
        session_id: Optional session ID (defaults to DEFAULT_SESSION_ID)

    Returns:
        Runner configured for the agent
    """
    # Create a session if it doesn't exist
    try:
        # Try to get the session - if it exists, this will succeed
        session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )
    except:
        # Session doesn't exist, create it
        session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=session_id
        )

    # Create and return the runner
    return Runner(agent=agent, app_name=APP_NAME, session_service=session_service)
