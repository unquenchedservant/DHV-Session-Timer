"""
For various utility functions
"""
import os
import sys

def get_ding_resource():
    if sys.platform in ("linux", "linux2", "darwin"):
        return "asset/ding.mp3"
    else:
        return "asset\\ding.mp3"
    
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)