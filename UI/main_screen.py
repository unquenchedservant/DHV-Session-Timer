"""
Holds the main screen and logic for the application.
"""

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QCheckBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
)
from PyQt6.QtCore import QTimer, Qt, QSettings
from PyQt6.QtGui import QKeySequence, QShortcut
from pygame import mixer
from utilities import resource_path, get_ding_resource
import concurrent.futures
from sys import platform
from .settings_screen import SettingsWindow
from plyer import notification


DEBUG_TIME = 60 # Prod - 60


class TimerApp(QMainWindow):
    """
    Class to hold the main window layout and logic. Main window of the application
    """

    def __init__(self):
        """
        initialize the main window, settings, and concurrent stream executor.

        :return: None
        """
        super().__init__()
        
        self.settings = QSettings(
            "UnquenchedServant", "DHV-Session-Timer"
        )  # initialize settings
        self.sound = resource_path(get_ding_resource())  # This is the almighty ding
        if self.settings.value("keep_active_default", "False") == "True":
            self.keep_on_top = True  # Grab the default keep on top setting
            self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.keep_on_top = False
            self.setWindowFlags(Qt.WindowType.Widget)
        self.executor = (
            concurrent.futures.ThreadPoolExecutor()
        )  # Needed for running the sound asynchronously
        self.started = False
        self.is_complete = False  # Used to check if the session is complete, helps with the start button efficiency
        self.initVariables()
        self.initUI()

    def initVariables(self):
        self.temp1 = self.settings.value("temp1", "350")
        self.temp2 = self.settings.value("temp2", "375")
        self.temp3 = self.settings.value("temp3", "400")
        self.time2 = int(self.settings.value("time2", "4"))
        self.time3 = int(self.settings.value("time3", "8"))
        self.time4 = int(self.settings.value("time4", "10"))
        self.temp_type = self.settings.value("temp_unit", "F")

    def initUI(self):
        """
        Initializes the UI for the main window. Sets the window title, creates the widgets needed, and lays them out.

        :return: None
        """
        self.setWindowTitle("DHV Session Timer")
        self.restoreGeometry(
            self.settings.value("geometry", b"")
        )  # Restores the window size and position
        palette = QApplication.instance().palette()
        self.setPalette(palette)

        # the timer label has to be nice and big and bold
        self.timer_label = QLabel("0:00", self)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 48px; font-weight: bold;")

        # the temp label is smaller and gray. Still mighty, but not as mighty.
        self.temp_label = QLabel(f"Temp: {self.temp1}°{self.temp_type}", self)
        self.temp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temp_label.setStyleSheet("font-size: 12px; color: gray;")

        self.keep_active_checkbox = QCheckBox(
            "Keep Win on Top", self
        )  # This is to make it so the window stays on top
        self.keep_active_checkbox.setChecked(
            self.keep_on_top
        )  # Grab state from settings
        self.keep_active_checkbox.stateChanged.connect(self.handleWindow)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_timer)

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.clicked.connect(self.reset_timer)

        self.settings_button = QPushButton("Settings", self)
        self.settings_button.clicked.connect(self.open_settings)
        if not self.is_complete:
            self.settings_button.isEnabled = False

        # Let's lay this out
        layout = QVBoxLayout()  # Lil vertical box to hold everything
        start_reset_layout = (
            QHBoxLayout()
        )  # Oh, surprise horizontal for the save and reset buttons!
        start_reset_layout.addWidget(self.start_button)
        start_reset_layout.addWidget(self.reset_button)
        settings_checkbox_layout = (
            QHBoxLayout()
        )  # Horizontal layout for the settings button and Keep Active checkbox
        settings_checkbox_layout.addWidget(self.settings_button)
        settings_checkbox_layout.addWidget(self.keep_active_checkbox)
        # Adds widgets/layouts in the following order: timer, temp, start/reset buttons, settings button
        layout.addWidget(self.timer_label)
        layout.addWidget(self.temp_label)
        layout.addLayout(start_reset_layout)
        layout.addLayout(settings_checkbox_layout)

        # We need to contain the layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.elapsed_time = 0

        # Spacebar to start/stop the timer
        self.start_shortcut = QShortcut(QKeySequence("Space"), self)
        self.start_shortcut.activated.connect(self.handle_spacebar)

    def closeEvent(self, event):
        """
        Saves the window size and position when the window is closed.

        :return: None
        """
        self.settings.setValue("geometry", self.saveGeometry())

    def handleWindow(self):
        """
        If the checkbox is checked, the window stays on top. If unchecked, the window behaves normally.
        This does have the adverse effect of flashing the window, but as far as I can tell, timing stays consistent.

        :return: None
        """
        if self.keep_active_checkbox.isChecked():
            self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
            self.keep_on_top = True
            self.show()
        else:
            self.setWindowFlags(Qt.WindowType.Widget)
            self.keep_on_top = False
            self.show()

    def handle_spacebar(self):
        """
        Space bar acts as a start/stop button. If the timer is active, reset the timer. If the timer isn't active, start the timer.

        :return: None
        """
        if self.timer.isActive():
            self.reset_timer()
        else:
            self.start_timer()

    def start_timer(self):
        """
        This is done for efficiency sake.
        Allows the user to press the start button at the end of a completed session to start a new one, but
        reset_timer() takes a little time, which isn't great when you want to start a timer.
        This only calls reset_timer() if the timer is active, otherwise it starts the timer without doing that.

        :return: None
        """
        if self.started:
            self.reset_timer()
        else:
            if self.is_complete:  # Our friend is_complete is here!
                self.is_complete = False  # No longer is_complete
                self.reset_timer()  # reset everything, just in case (if the user hits start after the session ends to start a new one)
            self.started = True
            self.start_button.setText("Stop/Reset")
            self.settings_button.setEnabled(False)
            self.timer.start(1000)  # 1000 ms = 1 second

    def reset_timer(self):
        """
        Handles resetting the timer. Stops the timer, sets the elapsed_time variable to 0,
        sets the timer_label text to 0:00, and shows the first temp label again (as this would have been hidden at the end of
        the session)

        :return: None
        """
        self.stop_timer(finished=False)
        self.elapsed_time = 0
        self.timer_label.setText("0:00")
        self.timer_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        self.temp_label.setText(f"Temp: {self.temp1}°{self.temp_type}")

    def open_settings(self):
        """        self.settings_button.disconnect()

        Opens the settings, connected to self.settings_button.

        :return: None
        """
        settings_window = SettingsWindow(self.settings)
        if settings_window.exec():
            # Updates the temp label to reflect the new temp settings
            self.temp_label.setText(
                f"Temp: {self.temp1}°{self.temp_type}"
            )

    def handle_time_change(self, temp, stage):
        if stage == "2" or stage == "3":
            message = f"Temp: {temp}°{self.temp_type}"
            title = f"DHV - Stage {stage}"
            self.temp_label.setText(f"Temp: {temp}°{self.temp_type}")
        elif stage == "end":
            message = "Session Done!"
            title = "DHV - Done"
            self.temp_label.setText("Session Done!")
        self.handle_notification(title, message)
        self.executor.submit(mixer.music.play)  

    def handle_notification(self, title, message):
        notif_on = True if self.settings.value('notifications', "True") == "True" else False
        timeout = int(self.settings.value("timeout", "10")) if not platform == "darwin" else 0
        if notif_on:
            notification.notify(title=f"{title}", message=f"{message}", timeout=timeout, app_name="DHVSessionTimer")

    def init_sound(self):
        mixer.init()
        mixer.music.load(self.sound)

    def handle_timer_label(self):
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.timer_label.setText(f"{minutes}:{seconds:02}")

    def stop_timer(self, finished=False):
        self.timer.stop()
        self.started = False
        self.start_button.setText("Start")
        self.settings_button.setEnabled(True)
        self.is_complete = finished
        if finished:
            self.timer_label.setText("Done!")
            self.timer_label.setStyleSheet("font-size: 38px; color: #9cb9d3; font-weight: bold;")

    def update_timer(self):
        """
        Called every second by the timer.
        Increments the elapsed_time variable by 1, converts the seconds to a human readable format (mm:ss),
        and updates the timer_label text to the new time. At user set intervals (default 6, 8, and 10 minutes), it will ding
        indicating that either an increase in temperature is needed or the session is complete. If the session is complete,
        it will show that in green text and the temperature label will hide, also stopping the timer so that update_timer()
        is no longer called

        :return: None
        """
        self.elapsed_time += 1
        self.handle_timer_label()
        self.init_sound()
        
        if self.elapsed_time == self.time2 * DEBUG_TIME:
            self.handle_time_change(self.temp2, "2")
        elif self.elapsed_time == self.time3 * DEBUG_TIME:
            self.handle_time_change(self.temp3, "3")
        elif self.elapsed_time == self.time4 * DEBUG_TIME:
            self.handle_time_change("350", "end")
            self.stop_timer(finished=True)
