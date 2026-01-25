from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langchain.tools import tool

# ============================================================================
# Configuration Section
# ============================================================================
# LLM model configuration
MODEL_NAME = "gpt-oss:20b"
MODEL_BASE_URL = "http://edgexpert01:11434"

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


def get_tools():
    """
    Return all available tools.
    
    Returns:
        List of all available tools
    """
    return [get_weather]


def run_agent_loop(agent):
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
        # agent.stream() yields intermediate states during execution
        for event in agent.stream(
            {"messages": messages},
            stream_mode="values",  # Stream complete state at each step
        ):
            # Print the last message (agent's response or tool output)
            event["messages"][-1].pretty_print()
        
        # Update message history with the complete conversation
        # including agent responses and tool calls
        messages = event["messages"]


def main():
    """
    Main entry point for the application.
    
    This function orchestrates:
    1. Tool setup
    2. Tool display (for debugging)
    3. Agent creation with model and tools
    4. Interactive conversation loop
    """
    # Get all available tools
    tools = get_tools()
    
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
    run_agent_loop(agent)


# ============================================================================
# Script Entry Point
# ============================================================================
if __name__ == "__main__":
    main()