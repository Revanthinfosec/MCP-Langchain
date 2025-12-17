import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

def test_gemini():
    # Load environment variables
    load_dotenv()
    
    # Get the API key
    api_key = os.getenv("GOOGLE_API_KEY")
    print(f"Using API key: {api_key[:5]}...{api_key[-5:] if api_key else ''}")
    
    if not api_key:
        print("Error: GOOGLE_API_KEY not found in .env file")
        return
    
    # Try to create the LLM instance
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=api_key,
            temperature=0.2
        )
        print("Successfully created ChatGoogleGenerativeAI instance")
        
        # Try a simple prediction
        response = llm.invoke("Hello, are you working?")
        print("Response from Gemini:")
        print(response.content)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_gemini()
