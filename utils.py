import json
from constants import CONFIG_FILE_PATH


def load_config():
    """Load configuration from JSON file."""
    with open(CONFIG_FILE_PATH, 'r') as config_file:
        return json.load(config_file)


def print_event(event, printed_set):
    """Print event messages and tool calls."""
    if 'messages' in event:
        for message in event['messages']:
            _print_message(message, printed_set)
    else:
        _print_other_event(event, printed_set)


def _print_message(message, printed_set):
    """Helper function to print different types of messages."""
    if hasattr(message, 'content') and message.content not in printed_set:
        role = type(message).__name__.replace('Message', '')
        print(f"{role}: {message.content}")
        printed_set.add(message.content)

    if hasattr(message, 'tool_calls') and message.tool_calls:
        _print_tool_calls(message.tool_calls, printed_set)


def _print_tool_calls(tool_calls, printed_set):
    """Helper function to print tool calls."""
    for tool_call in tool_calls:
        if isinstance(tool_call, dict):
            tool_call_str = f"Tool Call: {tool_call.get('name', 'Unknown')}({tool_call.get('args', {})})"
        else:
            tool_call_str = f"Tool Call: {getattr(tool_call, 'name', 'Unknown')}({getattr(tool_call, 'arguments', {})})"
        if tool_call_str not in printed_set:
            print(tool_call_str)
            printed_set.add(tool_call_str)


def _print_other_event(event, printed_set):
    """Helper function to print non-message events."""
    event_str = str(event)
    if event_str not in printed_set:
        print(f"Event: {event_str}")
        printed_set.add(event_str)