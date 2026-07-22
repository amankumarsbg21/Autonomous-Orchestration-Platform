from langgraph.graph import StateGraph, END

from app.schemas.state_schemas import AgentState, ComplexState
from app.database.memory import get_checkpointer
from app.graph.nodes import (
    planner_node, map_to_workers, worker_node, aggregator_node,
    router_node, route_decision, general_agent_node
)

# 1. Build Complex Sub-Graph
complex_builder = StateGraph(ComplexState)
complex_builder.add_node("planner", planner_node)
complex_builder.add_node("worker", worker_node)
complex_builder.add_node("aggregator", aggregator_node)

complex_builder.set_entry_point("planner")
complex_builder.add_conditional_edges("planner", map_to_workers, ["worker"])
complex_builder.add_edge("worker", "aggregator")
complex_builder.add_edge("aggregator", END)

complex_agent = complex_builder.compile()

def complex_wrapper_node(state: AgentState):
    from langchain_core.messages import AIMessage
    result = complex_agent.invoke({
        "query": state["query"],
        "messages": state["messages"]
    })
    return {
        "response": result["final_answer"],
        "messages": [AIMessage(content=result["final_answer"])]
    }

# 2. Build Main Router Graph
main_builder = StateGraph(AgentState)
main_builder.add_node("router", router_node)
main_builder.add_node("general_agent", general_agent_node)
main_builder.add_node("complex_agent", complex_wrapper_node)

main_builder.set_entry_point("router")
main_builder.add_conditional_edges(
    "router", route_decision, 
    {"general_agent": "general_agent", "complex_agent": "complex_agent"}
)
main_builder.add_edge("general_agent", END)
main_builder.add_edge("complex_agent", END)

# 3. Compile final application with Checkpointer Database
compiled_graph = main_builder.compile(checkpointer=get_checkpointer())