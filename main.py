from langchain_community.llms import OpenAI
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get OpenAI API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI LLM
llm = OpenAI(openai_api_key=api_key)
