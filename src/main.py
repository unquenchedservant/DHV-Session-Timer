"""
This application is a timer for a Dry-Herb vape with a session. It has 3 temperature settings and 3 time settings.
It will remind you to increase the temperature at the specified times, and will notify you when the session is complete.
It was designed with the Arizer Solo 3 in mind, but can be used with most other session vapes.

Created by Jon Thorne © 2025
"""
import sys
from PyQt6.QtWidgets import QApplication
from utilities import resource_path
from UI.main_screen import TimerApp
from UI.update_screen import UpdateApp
import requests

APP_VERSION = "v1.04"

if __name__ == '__main__':
    app = QApplication(sys.argv)    
    app.setStyle('Fusion')
    if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
        resource = "asset/style.qss"
    else:
        resource = "asset\\style.qss"
    with open (resource_path(resource), "r") as f:
        app.setStyleSheet(f.read())
    response = requests.get("https://api.github.com/repos/unquenchedservant/DHV-Session-Timer/releases/latest")
    if response.json()["name"] != APP_VERSION:
        ex = UpdateApp()
    else:
        ex = TimerApp()
    ex.show() 
    sys.exit(app.exec())