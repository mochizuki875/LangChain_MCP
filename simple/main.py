import os
from dotenv import load_dotenv
from pathlib import Path
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# 
#============================================================================
# Configuration Section
# ============================================================================
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

# Agent system prompt
SYSTEM_PROMPT = "You are a helpful assistant."

# ============================================================================
# Initialize LLM Model (module-level for reuse)
# ============================================================================
model = ChatOllama(
    model=MODEL_NAME,
    base_url=MODEL_BASE_URL
)


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
    1. Agent creation with model and tools
    2. Interactive conversation loop
    """
    
    # Create agent with LLM model, tools, and system prompt
    # The agent will use these tools to answer user queries
    agent = create_agent(
        model, 
        system_prompt=SYSTEM_PROMPT
    )
    
    # Start interactive conversation loop
    run_agent_loop(agent)


# ============================================================================
# Script Entry Point
# ============================================================================
if __name__ == "__main__":
    main()