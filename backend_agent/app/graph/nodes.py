from langgraph.constants import Send
from langchain.agents import create_agent
from langchain_core.messages import AIMessage
from app.core.config import llm
from app.services.tools import get_worker_tools
from app.schemas.state_schemas import AgentState, ComplexState, WorkerState, RouterOutput, PlannerOutput
from app.tools.web_search import web_search


get_worker_tools = [web_search]
tool_equipped_worker = create_agent(llm, get_worker_tools)

def planner_node(state: ComplexState):
    query = state["query"]
    history = "\n".join([f"{m.type}: {m.content}" for m in state.get("messages", [])[:-1]])
    
    structured_llm = llm.with_structured_output(PlannerOutput)
    prompt = f"Chat History:\n{history}\n\nBreak this request into specific search tasks: {query}"
    plan = structured_llm.invoke(prompt)
    print("plan****************",plan)
    return {"sub_tasks": plan.sub_tasks}

def map_to_workers(state: ComplexState):
    return [Send("worker", {"task": task}) for task in state["sub_tasks"]]

def worker_node(state: WorkerState):
    task = state["task"]
    
    agent_result = tool_equipped_worker.invoke({
        "messages": [("user", f"Complete this sub-task using tools: {task}")]
    }) 
    print("agent_result********",agent_result)
    final_output = agent_result["messages"][-1].content
    return {"worker_responses": [f"Task: {task}\nResult: {final_output}"]}

def aggregator_node(state: ComplexState):
    query = state["query"]
    history = "\n".join([f"{m.type}: {m.content}" for m in state.get("messages", [])[:-1]])
    all_responses = "\n\n".join(state.get("worker_responses", []))
    
    prompt = f"Chat History: {history}\nRequest: {query}\n\nData:\n{all_responses}\nSynthesize a final answer."
    final_output = llm.invoke(prompt).content
    return {"final_answer": final_output}

def router_node(state: AgentState):
    query = state["messages"][-1].content 
    history = "\n".join([f"{m.type}: {m.content}" for m in state["messages"][:-1]])
    
    structured_llm = llm.with_structured_output(RouterOutput)
    decision = structured_llm.invoke(f"Chat History:\n{history}\n\nClassify this query: {query}")
    return {"complexity": decision.complexity, "query": query}

def route_decision(state: AgentState):
    return "general_agent" if state["complexity"] == "simple" else "complex_agent"

def general_agent_node(state: AgentState):
    response = llm.invoke(state["messages"])
    return {
        "response": response.content,
        "messages": [AIMessage(content=response.content)]
    }

