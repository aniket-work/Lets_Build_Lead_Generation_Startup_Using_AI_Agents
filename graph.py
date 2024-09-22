from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda

from assistant import State


def handle_tool_error(state):
    """Handle errors that occur during tool execution."""
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools):
    """Create a tool node with fallback error handling."""
    return ToolNode(tools).with_fallbacks([RunnableLambda(handle_tool_error)], exception_key="error")


def build_graph(assistant, tools):
    """Build the StateGraph for the conversation flow."""
    builder = StateGraph(State)
    builder.add_node("assistant", assistant)
    builder.add_node("tools", create_tool_node_with_fallback(tools))

    builder.add_edge(START, "assistant")
    builder.add_conditional_edges("assistant", tools_condition)
    builder.add_edge("tools", "assistant")

    memory = MemorySaver()
    return builder.compile(checkpointer=memory)