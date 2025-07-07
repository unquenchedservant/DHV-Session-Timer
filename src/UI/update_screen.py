from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout
)
from PyQt6.QtCore import QSettings
from .main_screen import TimerApp
import webbrowser
import sys

class UpdateApp(QDialog):

    def __init__(self):
        super().__init__()
        self.settings = QSettings(
            "UnquenchedServant", "DHV-Session-Timer"
        )  # initialize settings
        self.setWindowTitle("UPDATE AVAILABLE - DHV Session Timer")
        self.restoreGeometry(
            self.settings.value("geometry", b"")
        )  # Restores the window size and position
        palette = QApplication.instance().palette()
        self.setPalette(palette)
        main_layout = QVBoxLayout(self)
        
        label_layout = QHBoxLayout(self)
        update_label = QLabel("There is an update available, would you like to download?", self)
        label_layout.addWidget(update_label)

        button_layout = QHBoxLayout(self)

        yes_button = QPushButton("Yes", self)
        yes_button.clicked.connect(self.run_updater)

        no_button = QPushButton("No", self)
        no_button.clicked.connect(self.skip_update)

        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)

        main_layout.addLayout(label_layout)
        main_layout.addLayout(button_layout)


        

    def run_updater(self):
        webbrowser.open("https://github.com/unquenchedservant/DHV-Session-Timer/releases/latest")
        self.close()
        sys.exit()


    def skip_update(self):
        self.hide()
        TimerApp().show()

