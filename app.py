import asyncio
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from mcp_use import MCPAgent, MCPClient

def handle_search_error(error):
    """Handle search-related errors and provide user-friendly messages."""
    error_msg = str(error).lower()
    if 'rate limit' in error_msg or 'anomaly' in error_msg or 'too many' in error_msg:
        return "I'm getting rate limited by the search service. Please wait a few moments and try again."
    return "I'm having trouble with the search service. Please try a different query or try again later."

async def run_with_retry(operation, max_retries=3, delay=2):
    """Run an operation with retry logic."""
    last_error = None
    for attempt in range(max_retries):
        try:
            return await operation()
        except Exception as e:
            last_error = e
            if attempt < max_retries - 1:  # Don't sleep on the last attempt
                await asyncio.sleep(delay * (attempt + 1))  # Exponential backoff
    raise last_error

async def run_memory_chat():
    """Run a chat using the MCPAgent's built-in conversation memory."""
    # Load environment variables for the API keys
    load_dotenv()
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

    # Configuration path - change this to your file
    config_file = "browser_mcp.json"
    print("Initializing chat...")

    # Initialize client with error handling
    try:
        client = MCPClient.from_config_file(config_file)
    except Exception as e:
        print(f"Error initializing MCP client: {e}")
        print("Please check your configuration and try again.")
        return
    
    # Using Google's Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Ollama code (commented out)
    # llm = ChatOllama(
    #     model="llama3",
    #     temperature=0.2
    # )

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=30,
        memory_enabled=True
    )

    print("\n ==== interactive MCP chat ====")
    print("Type 'exit' or 'quite' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("===============================\n")

    try:
        while True:
            #getting the users input
            user_input = input("\nYou:   ")

            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversatin....")
                break
            #nowcheck for clear history command
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared")
                continue

            #response from agent
            print("\n Assistant ", end="", flush=True)

            try:
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\nError: {e}")
    finally:
        #clean up
        if client and client.sessions:
            await client.close_all_sessions()
  
if __name__ == "__main__":
    asyncio.run(run_memory_chat())
    
