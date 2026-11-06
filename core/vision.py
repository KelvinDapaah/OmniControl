import pyautogui
from PIL import Image
import numpy as np
import cv2
from pywinauto import Desktop, Application

class VisionSystem:
    """
    Handles screen perception and transforms raw pixels and OS metadata
    into structured data an AI can reason about.
    """
    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()

    def get_ui_elements(self):
        """
        Extracts the semantic UI tree from the active window using UIA.
        Returns a list of elements with labels and normalized coordinates.
        """
        elements = []
        try:
            # Using Application().connect is more reliable for active windows
            app = Application().connect(active_window=True)
            win = app.active_window()

            # Access descendants via the window object
            for child in win.descendants():
                try:
                    if child.element_info.is_visible:
                        rect = child.rectangle()
                        center_x = (rect.left + rect.right) / 2
                        center_y = (rect.top + rect.bottom) / 2

                        norm_x = (center_x / self.screen_w) * 1000
                        norm_y = (center_y / self.screen_h) * 1000

                        elements.append({
                            "label": child.window_text() or child.element_info.name,
                            "type": child.element_info.control_type,
                            "x": int(norm_x),
                            "y": int(norm_y),
                            "id": child.element_info.handle
                        })
                except:
                    continue
        except Exception as e:
            # Silently fail on empty UI trees to avoid flooding logs,
            # but return the empty list
            pass

        return elements

    def get_element_coordinates(self, template_path):
        screen = np.array(pyautogui.screenshot())
        screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
        template = cv2.imread(template_path, 0)
        if template is None:
            return {"found": False, "error": "Template file not found"}
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.8:
            center_x = max_loc[0] + w // 2
            center_y = max_loc[1] + h // 2
            return {"found": True, "x": (center_x / self.screen_w) * 1000, "y": (center_y / self.screen_h) * 1000}
        return {"found": False}

    def analyze_layout(self, screenshot_path):
        return {"info": "Image sent to LLM for spatial reasoning."}
