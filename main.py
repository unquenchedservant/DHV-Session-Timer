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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open (resource_path("asset\\style.qss"), "r") as f:
        app.setStyleSheet(f.read())
    app.setStyle('Fusion')
    ex = TimerApp()
    ex.show()
    sys.exit(app.exec())