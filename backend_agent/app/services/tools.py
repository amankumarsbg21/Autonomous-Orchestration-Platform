from langchain_core.tools import tool
from app.core.config import tavily_client

@tool
def web_search(query: str) -> str:
    """Searches the web for current information, news, or factual data."""
    results = tavily_client.invoke(query)
    return f"[Search Results: {results}]"

# Export a list of all tools to be injected into agents
get_worker_tools = [web_search]