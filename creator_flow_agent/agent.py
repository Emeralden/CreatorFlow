import os
from typing import Any, cast

from google.adk.agents import Agent
from google.genai import types
from toolbox_core import ToolboxSyncClient

client = ToolboxSyncClient(
    os.getenv(
        "TOOLBOX_URL", "https://creator-flow-toolbox-818053237817.us-central1.run.app"
    )
)

creatorflow_tools = cast(list[Any], client.load_toolset("creatorflow_toolset"))
DEFAULT_MODEL = os.getenv("CREATORFLOW_MODEL", "gemini-2.5-flash")


def _tool_name(tool: Any) -> str:
    return str(getattr(tool, "name", getattr(tool, "__name__", ""))).strip()


def _pick_tools(*allowed_names: str) -> list[Any]:
    allowed = set(allowed_names)
    return [tool for tool in creatorflow_tools if _tool_name(tool) in allowed]


def _retry_generate_content_config() -> types.GenerateContentConfig:
    return types.GenerateContentConfig(
        http_options=types.HttpOptions(
            retry_options=types.HttpRetryOptions(initial_delay=0.4, attempts=2)
        )
    )


def _get_sub_agents(user_email: str) -> tuple[Any, Any, Any]:
    """Create and return status_manager, production_manager, and project_handler."""
    status_mgr_tools = _pick_tools(
        "get_my_projects_and_tasks",
        "get_my_schedule",
    )
    status_mgr = Agent(
        model=DEFAULT_MODEL,
        name="status_manager",
        description="Handles read-only status for projects, tasks, and schedule.",
        generate_content_config=_retry_generate_content_config(),
        instruction=f"""
        You are status_manager for CreatorFlow.
        Current user's email: {user_email}

        Responsibilities:
        - Use get_my_projects_and_tasks for project and task status.
        - Use get_my_schedule for schedule visibility.
        - Return concise summaries with clear next steps.
        """,
        tools=status_mgr_tools,
    )

    production_mgr_tools = _pick_tools(
        "ensure_creatorflow_schema",
        "schedule_filming",
    )
    production_mgr = Agent(
        model=DEFAULT_MODEL,
        name="production_manager",
        description="Handles creator production planning and schedule visibility.",
        generate_content_config=_retry_generate_content_config(),
        instruction=f"""
        You are production_manager for CreatorFlow.
        Current user's email: {user_email}

        Responsibilities:
        - Use schedule_filming to create filming events.
        - Do not interpret relative terms such as today, tomorrow, this Friday, coming Friday, next Friday, or next week.
        - Always ask for explicit start and end datetime values before calling schedule_filming.
        - Keep responses short and action-focused.
        """,
        tools=production_mgr_tools,
    )

    project_hdlr_tools = _pick_tools(
        "ensure_creatorflow_schema",
        "create_project",
        "create_script",
        "create_task",
    )
    project_hdlr = Agent(
        model=DEFAULT_MODEL,
        name="project_handler",
        description="Handles project creation and progress retrieval.",
        generate_content_config=_retry_generate_content_config(),
        instruction=f"""
        You are project_handler for CreatorFlow.
        Current user's email: {user_email}

        Responsibilities:
        - Use create_project, create_script, and create_task to create missing project work.
        - Do not interpret relative deadline terms such as today, tomorrow, this Friday, coming Friday, next Friday, or next week.
        - Always ask for an explicit deadline datetime before calling create_project.
        - Keep responses concise and include created IDs.
        """,
        tools=project_hdlr_tools,
    )
    
    return status_mgr, production_mgr, project_hdlr


def get_agent(user_email: str) -> Agent:
    status_manager, production_manager, project_handler = _get_sub_agents(user_email)

    supervisor_instruction = f"""
    You are the PRIMARY ORCHESTRATOR of CreatorFlow.
    You coordinate user requests to three specialized sub-agents.
    You have NO SQL tools.
    You delegate all work to sub-agents.
    
    Available sub-agents (use transfer/delegation):
    
     1. **status_manager**: Handles read-only status for schedule, projects, and tasks.
         - Route here for: "What's my schedule?", "Show my projects", "What tasks are pending?".

     2. **production_manager**: Handles schedule creation and production planning actions.
         - Route here for: "Schedule a filming", "Move/set filming time".

     3. **project_handler**: Handles project creation, tasks, and scripts.
       - Route here for: "Create a project", "Show my projects", "Add a task", "Write a script".
    
    Orchestration flow:
    1. Analyze user's intent. Assure them about what you can do or what you are going to do.
    2. Decide the flow and delegate to the appropriate sub-agents.
    2a. For scheduling/deadlines, require explicit datetime inputs and ask follow-up questions when missing.
    3. Return the sub-agent's response to the user and delegate to the next sub-agent when needed.
    4. If some info is not available, ask user to provide it. Don't assume anything yourself.
    5. Do not run SQL operations yourself. Delegate only.
    
    Tone: Have a slight Gen Z attitude and cheer: A bit sarcastic, a bit caring, a bit warm and a bit judgmental.
    Respond with short and punchy sentences. Use emojis in your responses.
    """

    return Agent(
        model=DEFAULT_MODEL,
        name="root_agent",
        description="CreatorFlow primary orchestrator routing to specialized agents.",
        generate_content_config=_retry_generate_content_config(),
        instruction=supervisor_instruction,
        sub_agents=[status_manager, production_manager, project_handler],
    )


root_agent = get_agent(os.getenv("USER_EMAIL", "test@example.com"))
