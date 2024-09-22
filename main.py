import uuid
from tools import estimate_savings
from assistant import create_assistant
from graph import build_graph
from utils import print_event


def main():
    tools = [estimate_savings]
    assistant = create_assistant(tools)
    graph = build_graph(assistant, tools)

    tutorial_questions = [
        "Hi There, can you calculate my energy saving my monthly cost is $100, what will i save"
    ]

    thread_id = str(uuid.uuid4())
    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 50
    }

    printed_set = set()
    for question in tutorial_questions:
        events = graph.stream(
            {"messages": ("user", question)}, config, stream_mode="values"
        )
        for event in events:
            print_event(event, printed_set)


if __name__ == "__main__":
    main()