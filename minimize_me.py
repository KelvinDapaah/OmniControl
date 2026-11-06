import sys
import os
sys.path.append(os.getcwd())

from api import OmniControlAPI
import pyautogui

api = OmniControlAPI()
print("Attempting to minimize active window using Win+Down...")
api.execute({"tool": "hotkey", "args": {"keys": ["win", "down"]}})
