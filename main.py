from api import OmniControlAPI
import json

def main():
    print("--- OmniControl Engine Online ---")
    api = OmniControlAPI()

    # Example of how an external AI would communicate with this:
    # In a real scenario, this would be a FastAPI or WebSocket server.
    mock_ai_calls = [
        {"tool": "screenshot", "args": {}},
        {"tool": "get_window", "args": {}},
        {"tool": "move_mouse", "args": {"x": 100, "y": 100}},
        {"tool": "type_text", "args": {"text": "OmniControl Active"}},
        {"tool": "press_key", "args": {"key": "enter"}},
    ]

    for call in mock_ai_calls:
        print(f"AI Request: {call['tool']} -> {call['args']}")
        result = api.execute(call)
        print(f"Engine Response: {result}\n")

if __name__ == "__main__":
    main()
