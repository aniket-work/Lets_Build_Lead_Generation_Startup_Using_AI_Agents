from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langgraph.graph.message import AnyMessage, add_messages
from constants import LLM_MODEL, LLM_TEMPERATURE, MAX_INTERACTIONS, SYSTEM_MESSAGE, PROCESSING_ERROR, INTERACTION_LIMIT_ERROR


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable
        self.interaction_count = 0
        self.last_user_message = None

    def __call__(self, state: State):
        last_message = state["messages"][-1]
        if isinstance(last_message, HumanMessage) and last_message.content != self.last_user_message:
            self.interaction_count = 0
            self.last_user_message = last_message.content

        self.interaction_count += 1
        if self.interaction_count > MAX_INTERACTIONS:
            return {"messages": [AIMessage(content=INTERACTION_LIMIT_ERROR)]}

        result = self.runnable.invoke(state)

        if self._is_invalid_result(result):
            return {"messages": [AIMessage(content=PROCESSING_ERROR)]}

        return {"messages": [result] if isinstance(result, AIMessage) else result}

    def _is_invalid_result(self, result):
        if isinstance(result, AIMessage):
            return not result.content and not getattr(result, 'tool_calls', None)
        elif isinstance(result, dict):
            return not result.get('content') and not result.get('tool_calls')
        return False


def create_assistant(tools):
    llm = ChatOllama(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_MESSAGE),
        ("placeholder", "{messages}"),
    ])

    assistant_runnable = prompt | llm.bind_tools(tools)
    return Assistant(assistant_runnable)