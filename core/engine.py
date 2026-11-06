import pyautogui
import pywinauto
from pywinauto import Application
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OmniControl")

class DesktopEngine:
    """
    The core execution engine for desktop interaction.
    Provides atomic actions that can be mapped to AI tool calls.
    """
    def __init__(self, fail_safe=True):
        # Fail-safe: move mouse to any corner of the screen to abort
        pyautogui.FAILSAFE = fail_safe
        logger.info(f"OmniControl Engine initialized. Fail-safe: {fail_safe}")

    def move_to(self, x, y, relative=False):
        """Moves mouse to coordinates. Coordinates are normalized 0-1000."""
        screen_w, screen_h = pyautogui.size()
        real_x = (x / 1000) * screen_w
        real_y = (y / 1000) * screen_h
        pyautogui.moveTo(real_x, real_y, duration=0.2)
        return {"status": "success", "position": [real_x, real_y]}

    def click(self, x, y, button='left', clicks=1):
        """Clicks at normalized coordinates."""
        self.move_to(x, y)
        pyautogui.click(button=button, clicks=clicks)
        return {"status": "success", "action": f"click_{button}"}

    def type_text(self, text):
        """Types string into the current focused element."""
        pyautogui.write(text, interval=0.05)
        return {"status": "success", "text_typed": text}

    def press_key(self, key):
        """Presses a specific key (e.g., 'enter', 'esc', 'win')."""
        pyautogui.press(key)
        return {"status": "success", "key_pressed": key}

    def hotkey(self, *keys):
        """Presses a combination of keys (e.g., ['ctrl', 'c'])."""
        pyautogui.hotkey(*keys)
        return {"status": "success", "hotkey_pressed": keys}

    def capture_screen(self, filename="screenshot.png"):
        """Captures the current screen state."""
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return {"status": "success", "path": filename}

    def get_active_window_title(self):
        """Returns the title of the currently active window."""
        try:
            # More robust method to get active window title
            app = Application().connect(active_window=True)
            win = app.active_window()
            return win.texts()[0] if win.texts() else "Unknown Window"
        except Exception:
            return "Unknown Window"
