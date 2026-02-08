import os
from dotenv import load_dotenv
from pathlib import Path
import asyncio
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_mcp_adapters.client import MultiServerMCPClient

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)
RUN_NAME="mcp_stdio"

# Initialize LLM Model based on provider
# LLM Provider Selection (set via environment variable or default to ollama)
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-oss:20b")
MODEL_BASE_URL = os.getenv("MODEL_BASE_URL", "http://127.0.0.1:11434")
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
if LLM_PROVIDER == "ollama":
    model = ChatOllama(
        model=MODEL_NAME,
        base_url=MODEL_BASE_URL
    )
    print(f"Using Ollama: {MODEL_NAME} at {MODEL_BASE_URL}")
else:
    raise ValueError(f"Unknown LLM_PROVIDER: {LLM_PROVIDER}. Use 'ollama'.")

# MCP server configuration
server_params = StdioServerParameters(
    command="python",
    args=["./schedule_mcp.py"],
)

# Agent system prompt
SYSTEM_PROMPT = "You are a helpful assistant."

# ============================================================================
# Initialize LLM Model (module-level for reuse)
# ============================================================================
model = ChatOllama(
    model=MODEL_NAME,
    base_url=MODEL_BASE_URL
)

# ============================================================================
# Tool Definitions
# ============================================================================
@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    # Mock weather tool - returns dummy data
    return f"Weather in {location}: Sunny, 25°C"


def display_tools(tools):
    """
    Display available tools and their arguments.
    
    This function prints tool information that will be sent to the model
    in the system prompt, allowing the model to understand what tools
    are available and how to use them.
    
    Args:
        tools: List of tool objects to display
    """
    print("Available Tools:")
    for t in tools:
        print(f"  - Name: {t.name}")
        print(f"    Description: {t.description}")
        # Display tool arguments if available
        if hasattr(t, 'args') and t.args:
            print(f"    Arguments:")
            for arg_name, arg_info in t.args.items():
                arg_type = arg_info.get('type', 'unknown')
                arg_desc = arg_info.get('description', '')
                print(f"      - {arg_name} ({arg_type}): {arg_desc}")
        print()


async def setup_tools(session):
    """
    Setup and return all available tools.
    
    This function:
    1. Retrieves tools from MCP servers
    2. Combines MCP tools with local tools
    
    Args:
        session: Active MCP ClientSession
    
    Returns:
        List of all available tools (MCP + local)
    """
    # Get tools from MCP session
    mcp_tools = await load_mcp_tools(session)
    
    # Combine MCP tools with local tools
    return mcp_tools + [get_weather]


async def run_agent_loop(agent):
    """
    Run the interactive agent conversation loop.
    
    This function:
    1. Maintains conversation history
    2. Accepts user input
    3. Streams agent responses
    4. Updates message history after each turn
    
    Args:
        agent: The LangChain agent to run
    """
    # Initialize empty message history
    messages = []

    while True:
        # Get user input
        query = input("Enter your question (exit/quit/q to quit): ")
        
        # Check for exit commands
        if query.lower() in ['exit', 'quit', 'q']:
            print("Exiting...")
            break
        
        # Add user message to conversation history
        messages.append({"role": "user", "content": query})
        
        # Stream agent response
        # agent.astream() yields intermediate states during execution
        async for event in agent.astream(
            {"messages": messages},
            stream_mode="values",  # Stream complete state at each step
            config={"run_name": RUN_NAME},
        ):
            # Print the last message (agent's response or tool output)
            event["messages"][-1].pretty_print()
        
        # Update message history with the complete conversation
        # including agent responses and tool calls
        messages = event["messages"]


async def main():
    """
    Main entry point for the application.
    
    This function orchestrates:
    1. MCP server connection
    2. Tool setup (MCP + local tools)
    3. Tool display (for debugging)
    4. Agent creation with model and tools
    5. Interactive conversation loop
    """
    # Connect to MCP server and keep the session alive
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # Setup all available tools (async operation)
            tools = await setup_tools(session)
            
            # Display tools for debugging
            # This shows what capabilities the model has access to
            display_tools(tools)
            
            # Create agent with LLM model, tools, and system prompt
            # The agent will use these tools to answer user queries
            agent = create_agent(
                model, 
                tools,
                system_prompt=SYSTEM_PROMPT
            )
            
            # Start interactive conversation loop
            await run_agent_loop(agent)

# ============================================================================
# Script Entry Point
# ============================================================================
if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
