TITLE: Install Google ADK Package
DESCRIPTION: Installs the Google Agent Development Kit (ADK) library and its dependencies using pip, the Python package installer. Requires an active Python environment (preferably a virtual environment).
SOURCE: https://github.com/google/adk-docs/blob/main/docs/get-started/quickstart.md#_snippet_4

LANGUAGE: bash
CODE:
```
pip install google-adk
```

----------------------------------------

TITLE: Installing ADK with pip
DESCRIPTION: Simple command to install the Google Agent Development Kit (ADK) package using pip package manager.
SOURCE: https://github.com/google/adk-docs/blob/main/README.md#_snippet_0

LANGUAGE: bash
CODE:
```
pip install google-adk
```

----------------------------------------

TITLE: Configuring Agents with State Management in Google ADK
DESCRIPTION: Setup of ADK agents with state management capabilities, including sub-agents for greetings and farewells, and a root agent configured with output_key to automatically save its responses to session state. The root agent uses the stateful weather tool to read from and write to state.
SOURCE: https://github.com/google/adk-docs/blob/main/examples/python/tutorial/agent_team/adk_tutorial.ipynb#2025-04-23_snippet_20

LANGUAGE: python
CODE:
```
# @title 3. Redefine Sub-Agents and Update Root Agent with output_key

# Ensure necessary imports: Agent, LiteLlm, Runner
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
# Ensure tools 'say_hello', 'say_goodbye' are defined (from Step 3)
# Ensure model constants MODEL_GPT_4O, MODEL_GEMINI_2_0_FLASH etc. are defined

# --- Redefine Greeting Agent (from Step 3) ---
greeting_agent = None
try:
    greeting_agent = Agent(
        model=MODEL_GEMINI_2_0_FLASH,
        name="greeting_agent",
        instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting using the 'say_hello' tool. Do nothing else.",
        description="Handles simple greetings and hellos using the 'say_hello' tool.",
        tools=[say_hello],
    )
    print(f"✅ Agent '{greeting_agent.name}' redefined.")
except Exception as e:
    print(f"❌ Could not redefine Greeting agent. Error: {e}")

# --- Redefine Farewell Agent (from Step 3) ---
farewell_agent = None
try:
    farewell_agent = Agent(
        model=MODEL_GEMINI_2_0_FLASH,
        name="farewell_agent",
        instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message using the 'say_goodbye' tool. Do not perform any other actions.",
        description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",
        tools=[say_goodbye],
    )
    print(f"✅ Agent '{farewell_agent.name}' redefined.")
except Exception as e:
    print(f"❌ Could not redefine Farewell agent. Error: {e}")

# --- Define the Updated Root Agent ---
root_agent_stateful = None
runner_root_stateful = None # Initialize runner

# Check prerequisites before creating the root agent
if greeting_agent and farewell_agent and 'get_weather_stateful' in globals():

    root_agent_model = MODEL_GEMINI_2_0_FLASH # Choose orchestration model

    root_agent_stateful = Agent(
        name="weather_agent_v4_stateful", # New version name
        model=root_agent_model,
        description="Main agent: Provides weather (state-aware unit), delegates greetings/farewells, saves report to state.",
        instruction="You are the main Weather Agent. Your job is to provide weather using 'get_weather_stateful'. "
                    "The tool will format the temperature based on user preference stored in state. "
                    "Delegate simple greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                    "Handle only weather requests, greetings, and farewells.",
        tools=[get_weather_stateful], # Use the state-aware tool
        sub_agents=[greeting_agent, farewell_agent], # Include sub-agents
        output_key="last_weather_report" # <<< Auto-save agent's final weather response
    )
    print(f"✅ Root Agent '{root_agent_stateful.name}' created using stateful tool and output_key.")

    # --- Create Runner for this Root Agent & NEW Session Service ---
    runner_root_stateful = Runner(
        agent=root_agent_stateful,
        app_name=APP_NAME,
        session_service=session_service_stateful # Use the NEW stateful session service
    )
    print(f"✅ Runner created for stateful root agent '{runner_root_stateful.agent.name}' using stateful session service.")

else:
    print("❌ Cannot create stateful root agent. Prerequisites missing.")
    if not greeting_agent: print(" - greeting_agent definition missing.")
    if not farewell_agent: print(" - farewell_agent definition missing.")
    if 'get_weather_stateful' not in globals(): print(" - get_weather_stateful tool missing.")
```

----------------------------------------

TITLE: Implementing Keyword-Blocking Guardrail with before_model_callback in Python
DESCRIPTION: This code defines a before_model_callback function that inspects user messages for a specific keyword ('BLOCK'). If the keyword is found, it blocks the request from reaching the LLM and returns a predefined response. The function accepts callback context and LLM request parameters, updates session state when a block occurs, and provides detailed logging.
SOURCE: https://github.com/google/adk-docs/blob/main/examples/python/notebooks/adk_tutorial.ipynb#2025-04-21_snippet_22

LANGUAGE: python
CODE:
```
# Ensure necessary imports are available
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types # For creating response content
from typing import Optional

def block_keyword_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    Inspects the latest user message for 'BLOCK'. If found, blocks the LLM call
    and returns a predefined LlmResponse. Otherwise, returns None to proceed.
    """
    agent_name = callback_context.agent_name # Get the name of the agent whose model call is being intercepted
    print(f"--- Callback: block_keyword_guardrail running for agent: {agent_name} ---")

    # Extract the text from the latest user message in the request history
    last_user_message_text = ""
    if llm_request.contents:
        # Find the most recent message with role 'user'
        for content in reversed(llm_request.contents):
            if content.role == 'user' and content.parts:
                # Assuming text is in the first part for simplicity
                if content.parts[0].text:
                    last_user_message_text = content.parts[0].text
                    break # Found the last user message text

    print(f"--- Callback: Inspecting last user message: '{last_user_message_text[:100]}...' ---") # Log first 100 chars

    # --- Guardrail Logic ---
    keyword_to_block = "BLOCK"
    if keyword_to_block in last_user_message_text.upper(): # Case-insensitive check
        print(f"--- Callback: Found '{keyword_to_block}'. Blocking LLM call! ---")
        # Optionally, set a flag in state to record the block event
        callback_context.state["guardrail_block_keyword_triggered"] = True
        print(f"--- Callback: Set state 'guardrail_block_keyword_triggered': True ---")

        # Construct and return an LlmResponse to stop the flow and send this back instead
        return LlmResponse(
            content=types.Content(
                role="model", # Mimic a response from the agent's perspective
                parts=[types.Part(text=f"I cannot process this request because it contains the blocked keyword '{keyword_to_block}'.")],
            )
            # Note: You could also set an error_message field here if needed
        )
    else:
        # Keyword not found, allow the request to proceed to the LLM
        print(f"--- Callback: Keyword not found. Allowing LLM call for {agent_name}. ---")
        return None # Returning None signals ADK to continue normally

print("✅ block_keyword_guardrail function defined.")
```

----------------------------------------

TITLE: Setting Up Session Management and Runner for ADK Agent
DESCRIPTION: Configures the session service and runner components needed to execute the agent. The session service manages conversation history and state, while the runner orchestrates the interaction flow between the user, agent, and tools.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/tutorials/agent-team.md#2025-04-23_snippet_6

LANGUAGE: python
CODE:
```
# --- Session Management ---
# Key Concept: SessionService stores conversation history & state.
# InMemorySessionService is simple, non-persistent storage for this tutorial.
session_service = InMemorySessionService()

# Define constants for identifying the interaction context
APP_NAME = "weather_tutorial_app"
USER_ID = "user_1"
SESSION_ID = "session_001" # Using a fixed ID for simplicity

# Create the specific session where the conversation will happen
session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)
print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

# --- Runner ---
# Key Concept: Runner orchestrates the agent execution loop.
runner = Runner(
    agent=weather_agent, # The agent we want to run
    app_name=APP_NAME,   # Associates runs with our app
    session_service=session_service # Uses our session manager
)
print(f"Runner created for agent '{runner.agent.name}'.")
```

----------------------------------------

TITLE: Using Multiple Built-in Tools with Agents - Python
DESCRIPTION: This snippet demonstrates how to use multiple built-in tools by assigning each tool to a separate agent and then combining these agents under a root agent using `AgentTool`. This is the supported method for using multiple built-in tools or combining them with other tools.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/tools/built-in-tools.md#_snippet_0

LANGUAGE: python
CODE:
```
from google.adk.tools import agent_tool
from google.adk.agents import Agent
from google.adk.tools import google_search, built_in_code_execution

search_agent = Agent(
    model='gemini-2.0-flash',
    name='SearchAgent',
    instruction="""
    You're a specialist in Google Search
    """,
    tools=[google_search],
)
coding_agent = Agent(
    model='gemini-2.0-flash',
    name='CodeAgent',
    instruction="""
    You're a specialist in Code Execution
    """,
    tools=[built_in_code_execution],
)
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.0-flash",
    description="Root Agent",
    tools=[agent_tool.AgentTool(agent=search_agent), agent_tool.AgentTool(agent=coding_agent)],
)
```

----------------------------------------

TITLE: Initial FastAPI App Setup (main.py)
DESCRIPTION: Provides the initial imports and setup for a FastAPI web application intended to integrate with ADK Streaming, including necessary modules for environment loading, Google GenAI types, ADK components, and FastAPI.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/get-started/quickstart-streaming.md#_snippet_9

LANGUAGE: python
CODE:
```
import os
import json
import asyncio

from pathlib import Path
from dotenv import load_dotenv

from google.genai.types import (
    Part,
    Content,
)

from google.adk.runners import Runner
from google.adk.agents import LiveRequestQueue
from google.adk.agents.run_config import RunConfig
from google.adk.sessions.in_memory_session_service import InMemorySessionService

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from google_search_agent.agent import root_agent

#
# ADK Streaming
#

```

----------------------------------------

TITLE: Updating Session State Manually with EventActions in Python
DESCRIPTION: Shows how to manually update session state using EventActions and state_delta. This method is used for complex scenarios involving multiple key updates, non-string values, or updates to specific state scopes like user or app state.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/sessions/state.md#2025-04-21_snippet_1

LANGUAGE: python
CODE:
```
from google.adk.sessions import InMemorySessionService, Session
from google.adk.events import Event, EventActions
from google.genai.types import Part, Content
import time

# --- Setup ---
session_service = InMemorySessionService()
app_name, user_id, session_id = "state_app_manual", "user2", "session2"
session = session_service.create_session(
    app_name=app_name,
    user_id=user_id,
    session_id=session_id,
    state={"user:login_count": 0, "task_status": "idle"}
)
print(f"Initial state: {session.state}")

# --- Define State Changes ---
current_time = time.time()
state_changes = {
    "task_status": "active",              # Update session state
    "user:login_count": session.state.get("user:login_count", 0) + 1, # Update user state
    "user:last_login_ts": current_time,   # Add user state
    "temp:validation_needed": True        # Add temporary state (will be discarded)
}

# --- Create Event with Actions ---
actions_with_update = EventActions(state_delta=state_changes)
# This event might represent an internal system action, not just an agent response
system_event = Event(
    invocation_id="inv_login_update",
    author="system", # Or 'agent', 'tool' etc.
    actions=actions_with_update,
    timestamp=current_time
    # content might be None or represent the action taken
)

# --- Append the Event (This updates the state) ---
session_service.append_event(session, system_event)
print("`append_event` called with explicit state delta.")

# --- Check Updated State ---
updated_session = session_service.get_session(app_name=app_name,
                                            user_id=user_id,
                                            session_id=session_id)
print(f"State after event: {updated_session.state}")
# Expected: {'user:login_count': 1, 'task_status': 'active', 'user:last_login_ts': <timestamp>}
# Note: 'temp:validation_needed' is NOT present.
```

----------------------------------------

TITLE: Implementing after_tool_callback in Python for ADK Framework
DESCRIPTION: This example shows how to use after_tool_callback to process or modify a tool's results before they're sent back to the LLM. It can be used for logging, reformatting results, or saving specific information to the session state.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/callbacks/types-of-callbacks.md#2025-04-21_snippet_5

LANGUAGE: python
CODE:
```
--8<-- "examples/python/snippets/callbacks/after_tool_callback.py"
```

----------------------------------------

TITLE: Initializing InMemorySessionService in Python
DESCRIPTION: A simple code snippet demonstrating how to import and initialize the InMemorySessionService, which stores session data in memory and is suitable for development and testing.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/sessions/session.md#2025-04-23_snippet_1

LANGUAGE: python
CODE:
```
from google.adk.sessions import InMemorySessionService
session_service = InMemorySessionService()
```

----------------------------------------

TITLE: Setting Up LLM-Driven Delegation in ADK Python
DESCRIPTION: This example demonstrates the basic setup required for LLM-driven agent delegation within an ADK multi-agent system. It shows a parent LlmAgent configured with instructions on how to delegate tasks to its sub-agents, which are defined with descriptions that help the parent LLM understand their capabilities, enabling dynamic task routing via function calls.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/agents/multi-agents.md#_snippet_5

LANGUAGE: python
CODE:
```
# Conceptual Setup: LLM Transfer
from google.adk.agents import LlmAgent

booking_agent = LlmAgent(name="Booker", description="Handles flight and hotel bookings.")
info_agent = LlmAgent(name="Info", description="Provides general information and answers questions.")

coordinator = LlmAgent(
    name="Coordinator",
    model="gemini-2.0-flash",
    instruction="You are an assistant. Delegate booking tasks to Booker and info requests to Info.",
    description="Main coordinator.",
    # AutoFlow is typically used implicitly here
    sub_agents=[booking_agent, info_agent]
)
# If coordinator receives "Book a flight", its LLM should generate:
# FunctionCall(name='transfer_to_agent', args={'agent_name': 'Booker'})

```

----------------------------------------

TITLE: Implementing Async Agent Interaction Handler
DESCRIPTION: Creates an asynchronous function to handle agent interactions. Processes user queries, manages event streams, and extracts final responses from the agent.
SOURCE: https://github.com/google/adk-docs/blob/main/examples/python/tutorial/agent_team/adk_tutorial.ipynb#2025-04-23_snippet_7

LANGUAGE: python
CODE:
```
async def call_agent_async(query: str, runner, user_id, session_id):
  print(f"\n>>> User Query: {query}")

  content = types.Content(role='user', parts=[types.Part(text=query)])

  final_response_text = "Agent did not produce a final response."

  async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
      if event.is_final_response():
          if event.content and event.content.parts:
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate:
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          break

  print(f"<<< Agent Response: {final_response_text}")
```

----------------------------------------

TITLE: Make Authenticated API Call in Tool (Python)
DESCRIPTION: This Python snippet shows how to use the valid `Credentials` object obtained from caching or the auth response to make a call to a protected API (using `googleapiclient.build` as an example). It includes basic error handling.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/tools/authentication.md#_snippet_14

LANGUAGE: Python
CODE:
```
# Inside your tool function, using the valid 'creds' object
# Ensure creds is valid before proceeding
if not creds or not creds.valid:
   return {"status": "error", "error_message": "Cannot proceed without valid credentials."}

try:
   service = build("calendar", "v3", credentials=creds) # Example
   api_result = service.events().list(...).execute()
   # Proceed to Step 7
except Exception as e:
   # Handle API errors (e.g., check for 401/403, maybe clear cache and re-request auth)
   print(f"ERROR: API call failed: {e}")
   return {"status": "error", "error_message": f"API call failed: {e}"}

```

----------------------------------------

TITLE: Initializing LlmAgent with Output Key in Python
DESCRIPTION: Demonstrates how to define an LlmAgent with an output_key to automatically save the agent's response to the session state. This example includes setting up a Runner and Session, running the agent, and checking the updated state.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/sessions/state.md#2025-04-21_snippet_0

LANGUAGE: python
CODE:
```
from google.adk.agents import LlmAgent
from google.adk.sessions import InMemorySessionService, Session
from google.adk.runners import Runner
from google.genai.types import Content, Part

# Define agent with output_key
greeting_agent = LlmAgent(
    name="Greeter",
    model="gemini-2.0-flash", # Use a valid model
    instruction="Generate a short, friendly greeting.",
    output_key="last_greeting" # Save response to state['last_greeting']
)

# --- Setup Runner and Session ---
app_name, user_id, session_id = "state_app", "user1", "session1"
session_service = InMemorySessionService()
runner = Runner(
    agent=greeting_agent,
    app_name=app_name,
    session_service=session_service
)
session = session_service.create_session(app_name=app_name,
                                        user_id=user_id,
                                        session_id=session_id)
print(f"Initial state: {session.state}")

# --- Run the Agent ---
# Runner handles calling append_event, which uses the output_key
# to automatically create the state_delta.
user_message = Content(parts=[Part(text="Hello")])
for event in runner.run(user_id=user_id,
                        session_id=session_id,
                        new_message=user_message):
    if event.is_final_response():
      print(f"Agent responded.") # Response text is also in event.content

# --- Check Updated State ---
updated_session = session_service.get_session(app_name, user_id, session_id)
print(f"State after agent run: {updated_session.state}")
# Expected output might include: {'last_greeting': 'Hello there! How can I help you today?'}
```

----------------------------------------

TITLE: Implementing a Guardrail using before_model_callback in ADK
DESCRIPTION: This example shows how to implement a basic content filter as a guardrail using the before_model_callback. It checks the LLM request for forbidden words and either allows the request to proceed or returns a predefined safe response.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/callbacks/index.md#2025-04-21_snippet_1

LANGUAGE: python
CODE:
```
from typing import Optional
from google.adk import types
from google.adk.llm import LlmResponse

FORBIDDEN_WORDS = ["dangerous", "harmful", "illegal"]

def content_filter(context: types.CallbackContext) -> Optional[LlmResponse]:
    for word in FORBIDDEN_WORDS:
        if word in context.llm_request.prompt.lower():
            print(f"Blocked request containing forbidden word: {word}")
            return LlmResponse(content="I cannot assist with that request.")
    # If we reach here, the content is safe
    return None  # Allows the LLM call to proceed normally

# Usage:
agent = Agent(
    name="SafeAgent",
    llm=my_llm_config,
    before_model_callback=content_filter
)
```

----------------------------------------

TITLE: Run ADK API Server
DESCRIPTION: Starts a local FastAPI server for the agent, enabling interaction via HTTP requests (e.g., using cURL). Useful for testing agent endpoints before deployment. Requires being in the parent directory of the agent project.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/get-started/quickstart.md#_snippet_16

LANGUAGE: shell
CODE:
```
adk api_server
```

----------------------------------------

TITLE: Configuring Weather Agent with ADK
DESCRIPTION: Creates and configures an ADK Agent with the weather tool. Specifies the agent's name, model, description, and instructions for handling weather queries.
SOURCE: https://github.com/google/adk-docs/blob/main/examples/python/tutorial/agent_team/adk_tutorial.ipynb#2025-04-23_snippet_5

LANGUAGE: python
CODE:
```
weather_agent = Agent(
    name="weather_agent_v1",
    model=AGENT_MODEL, # Can be a string for Gemini or a LiteLlm object
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "When the user asks for the weather in a specific city, "
                "use the 'get_weather' tool to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the weather report clearly.",
    tools=[get_weather], # Pass the function directly
)

print(f"Agent '{weather_agent.name}' created using model '{AGENT_MODEL}'.")
```

----------------------------------------

TITLE: Streaming Query to Remote Agent Python
DESCRIPTION: Sends a message query to the remotely deployed Agent Engine within a specified session and streams the response events back, simulating a real-time conversational flow with the agent running in the cloud.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/deploy/agent-engine.md#_snippet_12

LANGUAGE: python
CODE:
```
for event in remote_app.stream_query(
    user_id="u_456",
    session_id=remote_session["id"],
    message="whats the weather in new york",
):
    print(event)
```

----------------------------------------

TITLE: Check and Refresh Cached Credentials in Tool (Python)
DESCRIPTION: This Python code checks the `tool_context.state` for previously cached credentials. If found, it attempts to load and refresh them. If invalid or expired and not refreshable, it clears the cache.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/tools/authentication.md#_snippet_10

LANGUAGE: Python
CODE:
```
# Inside your tool function
TOKEN_CACHE_KEY = "my_tool_tokens" # Choose a unique key
SCOPES = ["scope1", "scope2"] # Define required scopes

creds = None
cached_token_info = tool_context.state.get(TOKEN_CACHE_KEY)
if cached_token_info:
    try:
        creds = Credentials.from_authorized_user_info(cached_token_info, SCOPES)
        if not creds.valid and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            tool_context.state[TOKEN_CACHE_KEY] = json.loads(creds.to_json()) # Update cache
        elif not creds.valid:
            creds = None # Invalid, needs re-auth
            tool_context.state[TOKEN_CACHE_KEY] = None
    except Exception as e:
        print(f"Error loading/refreshing cached creds: {e}")
        creds = None
        tool_context.state[TOKEN_CACHE_KEY] = None

if creds and creds.valid:
    # Skip to Step 5: Make Authenticated API Call
    pass
else:
    # Proceed to Step 2...
    pass

```

----------------------------------------

TITLE: Implementing before_tool_callback in Python for ADK Framework
DESCRIPTION: This example demonstrates how to use before_tool_callback to inspect or modify tool arguments before execution. It can perform authorization checks, implement caching, or skip tool execution entirely by returning a dictionary that serves as the tool's response.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/callbacks/types-of-callbacks.md#2025-04-21_snippet_4

LANGUAGE: python
CODE:
```
--8<-- "examples/python/snippets/callbacks/before_tool_callback.py"
```

----------------------------------------

TITLE: Creating Weather Agent with Model Guardrail in Python
DESCRIPTION: Creates a root weather agent with model guardrail using a callback function. The agent handles weather requests through a tool, delegates greetings and farewells to sub-agents, and implements a keyword-based guardrail that blocks requests containing specific words.
SOURCE: https://github.com/google/adk-docs/blob/main/examples/python/tutorial/agent_team/adk_tutorial.ipynb#2025-04-23_snippet_25

LANGUAGE: python
CODE:
```
# Check all components before proceeding
if greeting_agent and farewell_agent and 'get_weather_stateful' in globals() and 'block_keyword_guardrail' in globals():

    # Use a defined model constant
    root_agent_model = MODEL_GEMINI_2_0_FLASH

    root_agent_model_guardrail = Agent(
        name="weather_agent_v5_model_guardrail", # New version name for clarity
        model=root_agent_model,
        description="Main agent: Handles weather, delegates greetings/farewells, includes input keyword guardrail.",
        instruction="You are the main Weather Agent. Provide weather using 'get_weather_stateful'. "
                    "Delegate simple greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                    "Handle only weather requests, greetings, and farewells.",
        tools=[get_weather],
        sub_agents=[greeting_agent, farewell_agent], # Reference the redefined sub-agents
        output_key="last_weather_report", # Keep output_key from Step 4
        before_model_callback=block_keyword_guardrail # <<< Assign the guardrail callback
    )
    print(f"✅ Root Agent '{root_agent_model_guardrail.name}' created with before_model_callback.")

    # --- Create Runner for this Agent, Using SAME Stateful Session Service ---
    # Ensure session_service_stateful exists from Step 4
    if 'session_service_stateful' in globals():
        runner_root_model_guardrail = Runner(
            agent=root_agent_model_guardrail,
            app_name=APP_NAME, # Use consistent APP_NAME
            session_service=session_service_stateful # <<< Use the service from Step 4
        )
        print(f"✅ Runner created for guardrail agent '{runner_root_model_guardrail.agent.name}', using stateful session service.")
    else:
        print("❌ Cannot create runner. 'session_service_stateful' from Step 4 is missing.")

else:
    print("❌ Cannot create root agent with model guardrail. One or more prerequisites are missing or failed initialization:")
    if not greeting_agent: print("   - Greeting Agent")
    if not farewell_agent: print("   - Farewell Agent")
    if 'get_weather_stateful' not in globals(): print("   - 'get_weather_stateful' tool")
    if 'block_keyword_guardrail' not in globals(): print("   - 'block_keyword_guardrail' callback")

```

----------------------------------------

TITLE: Initializing LlmAgent Identity (Python)
DESCRIPTION: This snippet shows the basic instantiation of an `LlmAgent` in ADK. It requires specifying the underlying LLM `model`, a unique string `name` for identification, and an optional `description` that helps other agents understand its purpose in a multi-agent system. This defines the agent's fundamental identity before adding instructions or tools.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/agents/llm-agents.md#_snippet_0

LANGUAGE: python
CODE:
```
# Example: Defining the basic identity
capital_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="capital_agent",
    description="Answers user questions about the capital city of a given country."
    # instruction and tools will be added next
)
```

----------------------------------------

TITLE: Implementing Hierarchical Task Decomposition with ADK AgentTool in Python
DESCRIPTION: Demonstrates a multi-level agent hierarchy where higher-level agents delegate tasks to lower-level agents using `AgentTool`. A `ReportWriter` uses a `ResearchAssistant` tool, which in turn uses `WebSearch` and `Summarizer` tools, showcasing how complexity can be managed through recursive delegation.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/agents/multi-agents.md#_snippet_10

LANGUAGE: python
CODE:
```
# Conceptual Code: Hierarchical Research Task
from google.adk.agents import LlmAgent
from google.adk.tools import agent_tool

# Low-level tool-like agents
web_searcher = LlmAgent(name="WebSearch", description="Performs web searches for facts.")
summarizer = LlmAgent(name="Summarizer", description="Summarizes text.")

# Mid-level agent combining tools
research_assistant = LlmAgent(
    name="ResearchAssistant",
    model="gemini-2.0-flash",
    description="Finds and summarizes information on a topic.",
    tools=[agent_tool.AgentTool(agent=web_searcher), agent_tool.AgentTool(agent=summarizer)]
)

# High-level agent delegating research
report_writer = LlmAgent(
    name="ReportWriter",
    model="gemini-2.0-flash",
    instruction="Write a report on topic X. Use the ResearchAssistant to gather information.",
    tools=[agent_tool.AgentTool(agent=research_assistant)]
    # Alternatively, could use LLM Transfer if research_assistant is a sub_agent
)
# User interacts with ReportWriter.
# ReportWriter calls ResearchAssistant tool.
# ResearchAssistant calls WebSearch and Summarizer tools.
# Results flow back up.
```

----------------------------------------

TITLE: Initializing Weather Agent with Model Guardrail in Python
DESCRIPTION: Creates a weather agent with a model input guardrail callback that blocks requests containing specific keywords. The agent delegates to greeting and farewell sub-agents and maintains stateful sessions.
SOURCE: https://github.com/google/adk-docs/blob/main/examples/python/notebooks/adk_tutorial.ipynb#2025-04-21_snippet_24

LANGUAGE: python
CODE:
```
# Check all components before proceeding
if greeting_agent and farewell_agent and 'get_weather_stateful' in globals() and 'block_keyword_guardrail' in globals():

    # Use a defined model constant like MODEL_GEMINI_2_5_PRO
    root_agent_model = MODEL_GEMINI_2_0_FLASH

    root_agent_model_guardrail = Agent(
        name="weather_agent_v5_model_guardrail", # New version name for clarity
        model=root_agent_model,
        description="Main agent: Handles weather, delegates greetings/farewells, includes input keyword guardrail.",
        instruction="You are the main Weather Agent. Provide weather using 'get_weather_stateful'. "
                    "Delegate simple greetings to 'greeting_agent' and farewells to 'farewell_agent'. "
                    "Handle only weather requests, greetings, and farewells.",
        tools=[get_weather],
        sub_agents=[greeting_agent, farewell_agent], # Reference the redefined sub-agents
        output_key="last_weather_report", # Keep output_key from Step 4
        before_model_callback=block_keyword_guardrail # <<< Assign the guardrail callback
    )
    print(f"✅ Root Agent '{root_agent_model_guardrail.name}' created with before_model_callback.")

    # --- Create Runner for this Agent, Using SAME Stateful Session Service ---
    # Ensure session_service_stateful exists from Step 4
    if 'session_service_stateful' in globals():
        runner_root_model_guardrail = Runner(
            agent=root_agent_model_guardrail,
            app_name=APP_NAME, # Use consistent APP_NAME
            session_service=session_service_stateful # <<< Use the service from Step 4
        )
        print(f"✅ Runner created for guardrail agent '{runner_root_model_guardrail.agent.name}', using stateful session service.")
    else:
        print("❌ Cannot create runner. 'session_service_stateful' from Step 4 is missing.")

else:
    print("❌ Cannot create root agent with model guardrail. One or more prerequisites are missing or failed initialization:")
    if not greeting_agent: print("   - Greeting Agent")
    if not farewell_agent: print("   - Farewell Agent")
    if 'get_weather_stateful' not in globals(): print("   - 'get_weather_stateful' tool")
    if 'block_keyword_guardrail' not in globals(): print("   - 'block_keyword_guardrail' callback")
```

----------------------------------------

TITLE: Implementing State-Aware Weather Tool in Python
DESCRIPTION: Defines a weather tool that reads user temperature unit preferences from session state and formats weather data accordingly. Uses ToolContext for state access and includes mock weather data.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/tutorials/agent-team.md#2025-04-23_snippet_19

LANGUAGE: python
CODE:
```
from google.adk.tools.tool_context import ToolContext

def get_weather_stateful(city: str, tool_context: ToolContext) -> dict:
    """Retrieves weather, converts temp unit based on session state."""
    print(f"--- Tool: get_weather_stateful called for {city} ---")

    # --- Read preference from state ---
    preferred_unit = tool_context.state.get("user_preference_temperature_unit", "Celsius") # Default to Celsius
    print(f"--- Tool: Reading state 'user_preference_temperature_unit': {preferred_unit} ---")

    city_normalized = city.lower().replace(" ", "")

    # Mock weather data (always stored in Celsius internally)
    mock_weather_db = {
        "newyork": {"temp_c": 25, "condition": "sunny"},
        "london": {"temp_c": 15, "condition": "cloudy"},
        "tokyo": {"temp_c": 18, "condition": "light rain"},
    }

    if city_normalized in mock_weather_db:
        data = mock_weather_db[city_normalized]
        temp_c = data["temp_c"]
        condition = data["condition"]

        # Format temperature based on state preference
        if preferred_unit == "Fahrenheit":
            temp_value = (temp_c * 9/5) + 32 # Calculate Fahrenheit
            temp_unit = "°F"
        else: # Default to Celsius
            temp_value = temp_c
            temp_unit = "°C"

        report = f"The weather in {city.capitalize()} is {condition} with a temperature of {temp_value:.0f}{temp_unit}."
        result = {"status": "success", "report": report}
        print(f"--- Tool: Generated report in {preferred_unit}. Result: {result} ---")

        # Example of writing back to state (optional for this tool)
        tool_context.state["last_city_checked_stateful"] = city
        print(f"--- Tool: Updated state 'last_city_checked_stateful': {city} ---")

        return result
    else:
        # Handle city not found
        error_msg = f"Sorry, I don't have weather information for '{city}'."
        print(f"--- Tool: City '{city}' not found. ---")
        return {"status": "error", "error_message": error_msg}
```

----------------------------------------

TITLE: Extracting ADK Function Call Details (Python)
DESCRIPTION: Shows how to extract details of function call requests from an event using `event.get_function_calls()`. It demonstrates iterating through the list of calls to access the tool name and arguments (typically a dictionary).
SOURCE: https://github.com/google/adk-docs/blob/main/docs/events/index.md#_snippet_2

LANGUAGE: python
CODE:
```
calls = event.get_function_calls()
if calls:
    for call in calls:
        tool_name = call.name
        arguments = call.args # This is usually a dictionary
        print(f"  Tool: {tool_name}, Args: {arguments}")
        # Application might dispatch execution based on this
```

----------------------------------------

TITLE: Adding Function Tool to LlmAgent (Python)
DESCRIPTION: This snippet demonstrates how to equip an `LlmAgent` with external capabilities by defining a Python function (`get_capital_city`) and adding it to the agent's `tools` list. The function's docstring (`"""Retrieves the capital city..."""`) and parameters are used by the LLM to understand when and how to call the tool. The agent can then invoke this function during its reasoning process.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/agents/llm-agents.md#_snippet_2

LANGUAGE: python
CODE:
```
# Define a tool function
def get_capital_city(country: str) -> str:
  """Retrieves the capital city for a given country."""
  # Replace with actual logic (e.g., API call, database lookup)
  capitals = {"france": "Paris", "japan": "Tokyo", "canada": "Ottawa"}
  return capitals.get(country.lower(), f"Sorry, I don't know the capital of {country}.")

# Add the tool to the agent
capital_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="capital_agent",
    description="Answers user questions about the capital city of a given country.",
    instruction="""You are an agent that provides the capital city of a country... (previous instruction text)""",
    tools=[get_capital_city] # Provide the function directly
)
```

----------------------------------------

TITLE: Adding Instructions to LlmAgent (Python)
DESCRIPTION: This snippet illustrates how to provide detailed instructions to an `LlmAgent` using the `instruction` parameter. The instruction is a multiline string guiding the agent's behavior, persona, task steps, tool usage (`get_capital_city`), and desired output format, including examples. This parameter is crucial for shaping the agent's non-deterministic reasoning process.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/agents/llm-agents.md#_snippet_1

LANGUAGE: python
CODE:
```
# Example: Adding instructions
capital_agent = LlmAgent(
    model="gemini-2.0-flash",
    name="capital_agent",
    description="Answers user questions about the capital city of a given country.",
    instruction="""You are an agent that provides the capital city of a country.
When a user asks for the capital of a country:
1. Identify the country name from the user's query.
2. Use the `get_capital_city` tool to find the capital.
3. Respond clearly to the user, stating the capital city.
Example Query: "What's the capital of France?"
Example Response: "The capital of France is Paris."
""",
    # tools will be added next
)
```

----------------------------------------

TITLE: Obtaining Stock Price using Python Function Tool
DESCRIPTION: This Python function tool fetches the current stock price for a given ticker symbol using the `yfinance` library. It requires `pip install yfinance`. The function's docstring serves as the tool's description for the LLM. The return value will be automatically wrapped into a dictionary by the framework.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/tools/function-tools.md#_snippet_0

LANGUAGE: Python
CODE:
```
import yfinance as yf

def get_stock_price(ticker: str) -> str:
    """Obtains the Stock price of a given Stock ticker/ symbol.

    Args:
        ticker: The stock ticker symbol (e.g., "AAPL").

    Returns:
        The current stock price as a string (e.g., "$123.45").
    """
    try:
        stock = yf.Ticker(ticker)
        # Get the current price (last close or current if market open)
        price = stock.history(period="1d")['Close'].iloc[-1]
        return f"${price:.2f}"
    except Exception as e:
        return f"Error fetching price for {ticker}: {e}"

```

----------------------------------------

TITLE: Add Tools to ADK Agent (Python)
DESCRIPTION: Import the necessary agent and tool classes, then initialize an LlmAgent instance. Provide the language model, agent name, instructions, and the list of tools the agent should have access to.
SOURCE: https://github.com/google/adk-docs/blob/main/docs/tools/google-cloud-tools.md#_snippet_12

LANGUAGE: python
CODE:
```
from google.adk.agents.llm_agent import LlmAgent
from .tools import integration_tool, connector_tool

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='integration_agent',
    instruction="Help user, leverage the tools you have access to",
    tools=integration_tool.get_tools(),
)
```