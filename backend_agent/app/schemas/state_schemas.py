import operator
from typing import Annotated, TypedDict, Literal
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    query: str
    complexity: str 
    response: str

class ComplexState(TypedDict):
    messages: list[BaseMessage]
    query: str
    sub_tasks: list[str]
    worker_responses: Annotated[list[str], operator.add] 
    final_answer: str

class WorkerState(TypedDict):
    task: str

class RouterOutput(BaseModel):
    complexity: Literal["simple", "complex"] = Field(
        description="Classify query as 'simple' or 'complex'."
    )

class PlannerOutput(BaseModel):
    sub_tasks: list[str] = Field(
        description="List of specific search or data-retrieval tasks."
    )