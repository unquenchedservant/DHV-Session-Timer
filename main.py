"""
This application is a timer for a Dry-Herb vape with a session. It has 3 temperature settings and 3 time settings.
It will remind you to increase the temperature at the specified times, and will notify you when the session is complete.
It was designed with the Arizer Solo 3 in mind, but can be used with most other session vapes.

Created by Jon Thorne © 2025
"""
import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QComboBox, QLineEdit, QCheckBox, QFormLayout, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtCore import QTimer, Qt, QSettings
from PyQt6.QtGui import QKeySequence, QPalette, QIntValidator, QShortcut
from pygame import mixer
import math
import concurrent.futures

def is_system_dark_mode():
    palette = QApplication.instance().palette()
    return palette.color(QPalette.ColorRole.Window).lightness() < 128

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class SettingsWindow(QDialog):
    """
    Class to hold the settings window layout and logic.
    """
    def __init__(self, settings):
        """
        Initialize the settings window.

        :param name: settings: The QSettings object to save the settings
        :return: None
        """
        super().__init__()
        self.settings = settings
        if self.settings.value('keep_active_default', "False") == "True":
            self.keep_active = True
        else:
            self.keep_active = False
        self.initUI()
        
    def initUI(self):
        """
        Initializes the UI for the settings window. Sets the window title, creates the widgets needed, and lays them out.

        :return: None
        """
        self.setWindowTitle('Settings')
        onlyInt = QIntValidator(50, 428, self) # yes, I also think of OF when I see this variable name
        
        main_layout = QHBoxLayout() # holds the main layout
        
        # Temperature settings
        temp_layout = QFormLayout() # holds the temp layout
        
        self.temp1_input = QLineEdit(self)
        self.temp1_input.setValidator(onlyInt)
        self.temp1_input.setText(self.settings.value('temp1', '350'))
        self.temp1_input.setFixedWidth(40) # 40 works, so 40 works. 
        temp_layout.addRow('Temp 1:', self.temp1_input)
        
        self.temp2_input = QLineEdit(self) # repeat 2 more times for temp 2 and 3
        self.temp2_input.setValidator(onlyInt)
        self.temp2_input.setText(self.settings.value('temp2', '375'))
        self.temp2_input.setFixedWidth(40)
        temp_layout.addRow('Temp 2:', self.temp2_input)
        
        self.temp3_input = QLineEdit(self)
        self.temp3_input.setValidator(onlyInt)
        self.temp3_input.setText(self.settings.value('temp3', '400'))
        self.temp3_input.setFixedWidth(40)
        temp_layout.addRow('Temp 3:', self.temp3_input)

        self.temp_unit = QComboBox(self)
        self.temp_unit.addItems(['F', 'C']) # temperature unit combo box
        self.temp_unit.setCurrentText(self.settings.value('temp_type', 'F'))
        self.temp_unit.currentIndexChanged.connect(self.temp_unit_change) # connects to a function that converts the temperature unit
        self.temp_unit.setFixedWidth(40)
        temp_layout.addRow('Temp Unit:', self.temp_unit)

        # Create a widget to hold the temp layout, used for spacing
        temp_widget = QWidget() 
        temp_widget.setLayout(temp_layout)
        temp_widget.setFixedWidth(140) # aforementioned spacing
        
        # Time settings
        time_layout = QFormLayout() # Like what we did for temp, but with time.
        
        self.time1_input = QComboBox(self) # Time 1 will always be 0 seconds, so it's disabled and perma-set to 0
        self.time1_input.addItem("0") 
        self.time1_input.setEnabled(False) 
        time_layout.addRow('Time (min)', self.time1_input)
        
        self.time2_input = QComboBox(self)
        self.time2_input.addItems([str(i) for i in range(1,25)]) # Time 2-3 can be 1-25 minutes
        self.time2_input.setCurrentText(self.settings.value('time2', '6')) 
        time_layout.addRow('Time (min):', self.time2_input)
        
        self.time3_input = QComboBox(self)
        self.time3_input.addItems([str(i) for i in range(1,25)])
        self.time3_input.setCurrentText(self.settings.value('time3', '8'))
        time_layout.addRow('Time (min):', self.time3_input)

        self.time4_input = QComboBox(self)
        self.time4_input.addItems([str(i) for i in range(8,25)]) #Since 8 minutes is the lower limit for the auto-shutoff on the Solo 3, this will do
        self.time4_input.setCurrentText(self.settings.value('time4', '10'))
        time_layout.addRow('End Time (min):', self.time4_input)

        time_widget = QWidget() # spacing again
        time_widget.setLayout(time_layout)
        time_widget.setFixedWidth(140)

        # Add widgets to main layout
        main_layout.addWidget(temp_widget)
        main_layout.addWidget(time_widget)

        # Add a slider to default the Windows Active setting
        self.keep_active_label = QLabel('Keep Win on Top by Default', self)
        self.keep_active_default_slider = QCheckBox(self)
        self.keep_active_default_slider.setChecked(self.keep_active)
        self.keep_active_default_slider.stateChanged.connect(self.handle_slider)

        keep_active_layout = QHBoxLayout()
        keep_active_layout.addWidget(self.keep_active_label)
        keep_active_layout.addWidget(self.keep_active_default_slider)


        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save_settings)

        reset_button = QPushButton('Reset', self)
        reset_button.clicked.connect(self.reset_settings)
        
        self.error_msg = QLabel('Please enter valid temperatures (122-428°F)', self) # "you done messed up" label
        self.error_msg.setStyleSheet("color: red") # Gotta make sure it's red. 
        self.error_msg.hide() # Innocent until proven guilty ;)

        layout = QVBoxLayout()
        layout.addLayout(main_layout)
        layout.addWidget(self.error_msg)
        layout.addLayout(keep_active_layout)
        layout.addWidget(save_button)
        layout.addWidget(reset_button)
        
        self.setLayout(layout)

    def handle_slider(self):
        """
        Handles the slider for the keep active default setting. 

        :return: None
        """
        self.settings.setValue('keep_active_default', self.keep_active_default_slider.isChecked())

    # Allows for the settings window to be closed with the X button, and still save the settings
    def closeEvent(self, event):
        """
        Allows for the settings window to be closed with the X button, and still save the settings
        
        :param name: event: The close event
        :return: None
        """
        self.save_settings() 
        event.accept()    

    def temp_unit_change(self):
        """
        Converts the temperature unit when the combobox is changed, to some rough accuracy. 
        The conversion matches what the Solo 3 does as well. 

        :return: None
        """
        if self.temp_unit.currentText() == "F":
            self.temp1_input.setText(str(math.ceil(self.temp1_input * 9/5 + 32)))
            self.temp2_input.setText(str(math.ceil(self.temp2_input * 9/5 + 32)))
            self.temp3_input.setText(str(math.ceil(self.temp3_input * 9/5 + 32)))
        else:
            self.temp1_input.setText(str(math.floor((self.temp1_input - 32) * 5/9)))
            self.temp2_input.setText(str(math.floor((self.temp2_input - 32) * 5/9)))
            self.temp3_input.setText(str(math.floor((self.temp3_input - 32) * 5/9)))

    
    # Okay, you want the defaults?
    def reset_settings(self):
        """
        Resets the settings to the default values.

        :return: None
        """
        self.settings.setValue('temp1', '350')
        self.settings.setValue('temp2', '375')
        self.settings.setValue('temp3', '400')
        self.settings.setValue('temp_unit', 'F')
        self.settings.setValue('time2', '6')
        self.settings.setValue('time3', '8')
        self.settings.setValue('time4', '10')
        self.settings.setValue('keep_active_default', "False")

        self.temp1_input.setText('350')
        self.temp2_input.setText('375')
        self.temp3_input.setText('400')
        self.time2_input.setCurrentText('6')
        self.time3_input.setCurrentText('8')
        self.time4_input.setCurrentText('10')
        self.temp_unit.setCurrentText('F')
        self.keep_active_default_slider.setChecked("False")
        # You got 'em

    def save_settings(self):
        """
        Checks to make sure that all values for both temp and time are valid, and then
        saves the settings to the QSettings object.
        """
        # First we need to get the int values for the editable settings
        temp1 = int(self.temp1_input.text())
        temp2 = int(self.temp2_input.text())
        temp3 = int(self.temp3_input.text())
        time2 = int(self.time2_input.currentText())
        time3 = int(self.time3_input.currentText())
        time4 = int(self.time4_input.currentText())
        unit = self.temp_unit.currentText() # We also need the temp for later :D
        if not time3 > time2 or not time4 > time3: # You can't have a time that is less than the previous time, silly goose.
            self.error_msg.setText('Invalid time settings. Ensure each time is greater than the previous') # ID10T error, but for time.
            self.error_msg.show() # Guilty!
            return
        if unit == "F": # different ranges for F and C
            if not (122 <= temp1 <= 428 and 
                122 <= temp2 <= 428 and 
                122 <= temp3 <= 428): # Checks that all temps are within the Solo 3's F range
                self.error_msg.setText('Please enter valid temperatures (122-428°F)') # ID10T error, but for temp.
                self.error_msg.show() # Guilty!
                return
        else:
            if not (50 <= temp1 <= 220 and 
                50 <= temp2 <= 220 and 
                50 <= temp3 <= 220): # Checks that all temps are within the Solo 3's C range
                self.error_msg.setText('Please enter valid temperatures (50-220°C)') # ID10T error, but for non-US temp.
                self.error_msg.show() # Guilty!
                return
        # If we get here, the user didn't mess this up. 
        # but now we gotta convert them all back to strings :D
        self.settings.setValue('temp1', str(temp1))
        self.settings.setValue('temp2', str(temp2))
        self.settings.setValue('temp3', str(temp3))
        self.settings.setValue('time2', str(time2))
        self.settings.setValue('time3', str(time3))
        self.settings.setValue('time4', str(time4))
        self.settings.setValue("temp_type", unit)
        self.settings.setValue('keep_active_default', str(self.keep_active_default_slider.isChecked()))
        self.accept() # Save them settings!

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
        self.settings = QSettings('UnquenchedServant', 'DHV-Session-Timer') # initialize settings
        self.sound = resource_path("asset\\ding.mp3") # This is the almighty ding
        if self.settings.value('keep_active_default', "False") == "True":
            self.keep_on_top = True # Grab the default keep on top setting
            self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.keep_on_top = False
            self.setWindowFlags(Qt.WindowType.Widget)
        self.executor = concurrent.futures.ThreadPoolExecutor() # Needed for running the sound asynchronously
        self.is_complete = False # Used to check if the session is complete, helps with the start button efficiency
        self.initUI()
        
    def initUI(self):
        """
        Initializes the UI for the main window. Sets the window title, creates the widgets needed, and lays them out.

        :return: None
        """
        self.setWindowTitle('DHV Session Timer')
        self.setGeometry(100, 100, 400, 150)
        
        # the timer label has to be nice and big and bold
        self.timer_label = QLabel('0:00', self) 
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        self.timer_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        
        # the temp label is smaller and gray. Still mighty, but not as mighty.
        self.temp_label = QLabel(f"Temp: {self.settings.value('temp1', '350')}°{self.settings.value("temp_type", "F")}", self)
        self.temp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temp_label.setStyleSheet("font-size: 12px; color: gray;")
        
        self.keep_active_checkbox = QCheckBox('Keep Win on Top', self) # This is to make it so the window stays on top
        self.keep_active_checkbox.setChecked(self.keep_on_top) # Grab state from settings
        self.keep_active_checkbox.stateChanged.connect(self.handleWindow)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_timer)
        
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_timer)

        self.settings_button = QPushButton('Settings', self)
        self.settings_button.clicked.connect(self.open_settings)
        
        # Let's lay this out
        layout = QVBoxLayout() # Lil vertical box to hold everything
        start_reset_layout = QHBoxLayout() # Oh, surprise horizontal for the save and reset buttons!
        start_reset_layout.addWidget(self.start_button)
        start_reset_layout.addWidget(self.reset_button)
        settings_checkbox_layout = QHBoxLayout() # Horizontal layout for the settings button and Keep Active checkbox
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
        if self.is_complete: # Our friend is_complete is here!
            self.is_complete = False # No longer is_complete
            self.reset_timer() # reset everything, just in case (if the user hits start after the session ends to start a new one)
        self.timer.start(1000) # 1000 ms = 1 second
        
        
    def reset_timer(self):
        """
        Handles resetting the timer. Stops the timer, sets the elapsed_time variable to 0,
        sets the timer_label text to 0:00, and shows the first temp label again (as this would have been hidden at the end of 
        the session)

        :return: None
        """
        self.timer.stop() 
        self.elapsed_time = 0
        self.timer_label.setText('0:00')
        self.timer_label.setStyleSheet("font-size: 48px; font-weight: bold;")
        self.temp_label.setText(f"Temp: {self.settings.value('temp1', '350')}°{self.settings.value("temp_type", "F")}")
        self.temp_label.show() # We're going to hide this when the session is complete, so we need to show it again

    def open_settings(self):
        """
        Opens the settings, connected to self.settings_button.

        :return: None
        """
        settings_window = SettingsWindow(self.settings)
        if settings_window.exec():
            # Updates the temp label to reflect the new temp settings
            self.temp_label.setText(f"Temp: {self.settings.value('temp1', '350')}°{self.settings.value("temp_type", "F")}")
       
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
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.timer_label.setText(f'{minutes}:{seconds:02}')
        time2 = int(self.settings.value('time2', '6')) # Remember how these values are strings? they need to be ints again
        time3 = int(self.settings.value('time3', '8')) 
        time4 = int(self.settings.value('time4', '10'))
        mixer.init()
        mixer.music.load(self.sound)

        if self.elapsed_time == time2 * 60:
            self.temp_label.setText(f'Temp: {self.settings.value("temp2", "375")}°{self.settings.value("temp_type", "F")}')
            self.executor.submit(mixer.music.play) # plays the almighty ding asynchronously
        elif self.elapsed_time == time3 * 60:
            self.temp_label.setText(f'Temp: {self.settings.value("temp3", "400")}°{self.settings.value("temp_type", "F")}')
            self.executor.submit(mixer.music.play)
        elif self.elapsed_time == time4 * 60:
            self.temp_label.hide()
            # Woo! You made it, let's do it again!! (or not, if you don't want to)
            self.timer_label.setText('Session \nDone!')
            if is_system_dark_mode():
                self.timer_label.setStyleSheet("font-size: 38px; color: #9cb9d3; font-weight: bold;")
            else:
                self.timer_label.setStyleSheet("font-size: 38px; color: green; font-weight: bold;")
            self.executor.submit(mixer.music.play)
            self.timer.stop()
            self.is_complete = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if is_system_dark_mode():
        with open (resource_path("asset\\style-dark.qss"), "r") as f:
            app.setStyleSheet(f.read())
    else:
        with open (resource_path("asset\\style.qss"), "r") as f:
            app.setStyleSheet(f.read())
    #app.setStyle('Fusion')
    ex = TimerApp()
    ex.show()
    sys.exit(app.exec())