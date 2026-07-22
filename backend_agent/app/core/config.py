import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

llm=ChatGoogleGenerativeAI(model='gemini-2.5-flash',max_tokens=500)

tavily_client = TavilySearchResults(max_results=2)