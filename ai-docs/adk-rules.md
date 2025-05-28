•
Develop agents using the flexible and modular ADK framework, which is designed to make agent development feel more like software development and is model-agnostic, deployment-agnostic, and compatible with other frameworks.
•
Choose the appropriate agent type based on the task: LlmAgent for tasks requiring reasoning, generation, or tool use; Workflow Agents (Sequential, Parallel, Loop) for controlling execution flow; or Custom Agents for implementing unique logic or integrations. Understand their primary functions and core engines.
•
Configure each agent by providing the underlying language model (which can be Gemini, or others via LiteLlm such as OpenAI, Anthropic, Ollama, or self-hosted vLLM) and assigning a unique string name for identification.
•
For LlmAgent instances, provide clear and detailed instruction using a multiline string parameter. This instruction is crucial for shaping the agent's behavior, persona, task steps, guiding tool usage, and defining desired output formats.
•
Equip agents with relevant tools by providing a list of tool functions or tool instances (including Python functions, Built-in tools, Third-party tools like LangChain or CrewAI integrations, Google Cloud tools, MCP tools, or OpenAPI tools) to the agent's configuration. This enables agents to interact with external systems or perform specific actions. Tools can read from and write to the session state.
•
Build modular and scalable applications by composing multiple specialized agents in a hierarchy using the sub_agents parameter on a parent agent. This establishes parent-child relationships and enables complex coordination and delegation.
•
Define agent capabilities clearly using the description parameter. This is especially important for LlmAgents participating in multi-agent systems or using LLM Transfer, as the description helps the parent LLM understand the sub-agent's purpose and delegate tasks appropriately.
•
Utilize Workflow Agents such as SequentialAgent (for fixed pipelines), ParallelAgent (for concurrent execution), and LoopAgent (for iterative processes) to define predictable or repetitive orchestration patterns based on predefined logic rather than LLM reasoning.
•
Leverage shared Session state (context.state or session.state) for seamless communication between agents, tools, and callbacks within a single conversation or interaction flow. Use state to store data, user preferences, intermediate results, and decision-making flags.
•
Use the output_key parameter on an agent to automatically save its final response or structured output (when output_schema is used) to a designated key in the session state. This makes the agent's result easily accessible to subsequent agents, tools, or evaluation processes.
•
Use the Runner to orchestrate the interaction flow for a specific session. The Runner takes the agent, application name, and session service, managing the sequence of operations, callbacks, and event processing.
•
Implement SessionService (like InMemorySessionService for testing or DatabaseSessionService for persistence) to manage conversation history and the shared session state across turns.
•
Utilize callbacks (before_agent, after_agent, before_model, after_model, before_tool, after_tool) to hook into the agent execution lifecycle. Callbacks allow inspecting or modifying requests/responses, logging, adding context, or implementing conditional logic like skipping steps.
•
Implement safety and security patterns by using callbacks to create guardrails. These guardrails can inspect user input (before_model_callback), LLM responses (after_model_callback), or tool arguments (before_tool_callback) and potentially block or modify them based on defined criteria, building powerful and trustworthy agents.
•
Configure runtime settings using RunConfig to control aspects like response modalities (TEXT, AUDIO) and the maximum number of LLM calls. Fine-tune LLM generation parameters via generate_content_config (e.g., temperature, max output tokens) to adjust the agent's response style.
•
Design agents to process and yield events emitted by tools or sub-agents throughout the execution flow. Be prepared to handle different event types, including those containing content, tool results, state changes (state_delta), errors, and control flow signals (transfer_to_agent, escalate, skip_summarization).
•
Test and evaluate agent performance thoroughly using ADK's built-in tools, including the command-line adk eval tool, the adk web UI for interactive evaluation, and programmatic evaluation with AgentEvaluator. Use evaluation sets to define expected behavior, tool usage sequences, and intermediate responses against which to measure the agent's performance.
•
Prepare agent code for deployment by defining necessary Python dependencies (requirements.txt), packaging the application using container configurations (like a Dockerfile), and configuring environment variables needed by the agent and the target platform (Cloud Run, GKE, Agent Engine).
•
Ensure API keys for all required language models and services (Google AI, OpenAI, Anthropic via LiteLlm, Vertex AI endpoints, third-party tools, etc.) are securely configured, typically using environment variables, before running or deploying the agent.
•
Organize your project with a recommended directory structure that separates agent code, dependencies, and deployment configurations (like main.py, requirements.txt, Dockerfile, .env files) to ensure discoverability and facilitate deployment.