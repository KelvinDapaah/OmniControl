from core.engine import DesktopEngine
from core.vision import VisionSystem
import json

class OmniControlAPI:
    """
    The Interface layer. Maps external JSON tool calls
    to internal Engine actions.
    """
    def __init__(self):
        self.engine = DesktopEngine()
        self.vision = VisionSystem()

    def execute(self, tool_call):
        """
        Main entry point for the AI.
        Now includes the Verification Loop (Phase 2).
        """
        tool_name = tool_call.get("tool")
        args = tool_call.get("args", {})

        # 1. Capture State BEFORE action
        before_state = {
            "window": self.engine.get_active_window_title(),
            "elements_count": len(self.vision.get_ui_elements())
        }

        try:
            if tool_name == "move_mouse":
                result = self.engine.move_to(args['x'], args['y'])
            elif tool_name == "click":
                result = self.engine.click(args['x'], args['y'], args.get('button', 'left'))
            elif tool_name == "type_text":
                result = self.engine.type_text(args['text'])
            elif tool_name == "press_key":
                result = self.engine.press_key(args['key'])
            elif tool_name == "hotkey":
                result = self.engine.hotkey(*args['keys'])
            elif tool_name == "screenshot":
                result = self.engine.capture_screen()
            elif tool_name == "get_window":
                result = {"window": self.engine.get_active_window_title()}
            elif tool_name == "get_ui_tree":
                result = {"elements": self.vision.get_ui_elements()}
            else:
                return {"error": f"Unknown tool: {tool_name}"}

            # 2. Capture State AFTER action
            after_state = {
                "window": self.engine.get_active_window_title(),
                "elements_count": len(self.vision.get_ui_elements())
            }

            # 3. Verify if a meaningful change occurred (for interactive tools)
            interactive_tools = ["click", "type_text", "press_key", "hotkey"]
            if tool_name in interactive_tools:
                changed = (before_state["window"] != after_state["window"]) or \
                           (before_state["elements_count"] != after_state["elements_count"])

                result["verification"] = {
                    "changed": changed,
                    "before": before_state,
                    "after": after_state
                }

            return result

        except Exception as e:
            return {"error": str(e)}

    def get_tool_definitions(self):
        """Returns the schema any LLM needs to interact with this tool."""
        return [
            {"name": "move_mouse", "description": "Moves cursor to normalized (0-1000) coords", "parameters": {"x": "int", "y": "int"}},
            {"name": "click", "description": "Clicks at normalized coords", "parameters": {"x": "int", "y": "int", "button": "string"}},
            {"name": "type_text", "description": "Types string into focused field", "parameters": {"text": "string"}},
            {"name": "press_key", "description": "Presses a single key", "parameters": {"key": "string"}},
            {"name": "hotkey", "description": "Presses key combination", "parameters": {"keys": "list[string]"}},
            {"name": "screenshot", "description": "Captures screen", "parameters": {}},
            {"name": "get_window", "description": "Gets active window title", "parameters": {}},
            {"name": "get_ui_tree", "description": "Gets semantic UI elements (labels, types, coords)", "parameters": {}},
        ]
