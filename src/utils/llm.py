import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def get_llm(model_name: str = "qwen/qwen3-32b"):
    """
    Returns a ChatGroq instance.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")
    
    return ChatGroq(
        model_name=model_name,
        api_key=api_key,
        temperature=0
    )
