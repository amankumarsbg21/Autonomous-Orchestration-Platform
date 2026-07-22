from langgraph.checkpoint.memory import MemorySaver

def get_checkpointer():
    """Returns the checkpointer for LangGraph memory."""
    # In production, replace with PostgresSaver or RedisSaver
    return MemorySaver()