import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLineEdit, QCheckBox, QShortcut, QFormLayout, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt, QSettings
from PyQt5.QtGui import QKeySequence, QIntValidator
from playsound import playsound
import math
import concurrent.futures

class SettingsWindow(QDialog):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.initUI()
        
    def initUI(self):
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
        layout.addWidget(save_button)
        layout.addWidget(reset_button)
        
        self.setLayout(layout)

    # Allows for the settings window to be closed with the X button, and still save the settings
    def closeEvent(self, event):
        self.save_settings() 
        event.accept()    

    # Converts the temperature unit when the combo box is changed, to some rough accuracy
    # Worth noting that the Solo 3 does the same conversion.
    def temp_unit_change(self):
        if self.temp_unit.currentText() == "F":
            self.temp1_input.setText(str(self.c_to_f(int(self.temp1_input.text()))))
            self.temp2_input.setText(str(self.c_to_f(int(self.temp2_input.text()))))
            self.temp3_input.setText(str(self.c_to_f(int(self.temp3_input.text()))))
        else:
            self.temp1_input.setText(str(self.f_to_c(int(self.temp1_input.text()))))
            self.temp2_input.setText(str(self.f_to_c(int(self.temp2_input.text()))))
            self.temp3_input.setText(str(self.f_to_c(int(self.temp3_input.text()))))

    # Converts Fahrenheit to Celsius
    def f_to_c(self, f_temp):
        return math.floor((f_temp - 32) * 5/9)
    
    # Converts Celsius to Fahrenheit
    def c_to_f(self, c_temp):
        return math.ceil(c_temp * 9/5 + 32)
    
    # Okay, you want the defaults?
    def reset_settings(self):
        self.settings.setValue('temp1', '350')
        self.settings.setValue('temp2', '375')
        self.settings.setValue('temp3', '400')
        self.settings.setValue('temp_unit', 'F')
        self.settings.setValue('time2', '6')
        self.settings.setValue('time3', '8')
        self.settings.setValue('time4', '10')

        self.temp1_input.setText('350')
        self.temp2_input.setText('375')
        self.temp3_input.setText('400')
        self.time2_input.setCurrentText('6')
        self.time3_input.setCurrentText('8')
        self.time4_input.setCurrentText('10')
        self.temp_unit.setCurrentText('F')
        # You got 'em

    def save_settings(self):
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
        self.accept() # Save them settings!

class TimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('UnquenchedServant', 'DHV-Session-Timer') # initialize settings
        self.sound = "asset/ding.mp3" # This is the almighty ding
        self.executor = concurrent.futures.ThreadPoolExecutor() # Needed for running the sound asynchronously
        self.is_complete = False # Used to check if the session is complete, helps with the start button efficiency
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('DHV Session Timer')
        self.setGeometry(100, 100, 400, 150)
        
        # the timer label has to be nice and big and bold
        self.timer_label = QLabel('0:00', self) 
        self.timer_label.setAlignment(Qt.AlignCenter) 
        self.timer_label.setStyleSheet("font-size: 48px; color: black; font-weight: bold;")
        
        # the temp label is smaller and gray. Still mighty, but not as mighty.
        self.temp_label = QLabel(f"Temp: {self.settings.value('temp1', '350')}°{self.settings.value("temp_type", "F")}", self)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setStyleSheet("font-size: 12px; color: gray;")
        
        self.keep_active_checkbox = QCheckBox('Keep Win on Top', self) # This is to make it so the window stays on top 
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
        if self.keep_active_checkbox.isChecked():
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.setWindowFlags(Qt.Widget)
            self.show()

    def handle_spacebar(self):
        if self.timer.isActive():
            self.reset_timer()
        else:
            self.start_timer()
        
    def start_timer(self):
        if self.is_complete: # Our friend is_complete is here!
            self.is_complete = False # No longer is_complete
            self.reset_timer() # reset everything, just in case (if the user hits start after the session ends to start a new one)
        self.timer.start(1000) # 1000 ms = 1 second
        
        
    def reset_timer(self):
        # Handles resetting the timer
        self.timer.stop() 
        self.elapsed_time = 0
        self.timer_label.setText('0:00')
        self.timer_label.setStyleSheet("font-size: 48px; color: black; font-weight: bold;")
        self.temp_label.setText(f"Temp: {self.settings.value('temp1', '350')}°{self.settings.value("temp_type", "F")}")
        self.temp_label.show() # We're going to hide this when the session is complete, so we need to show it again

    def open_settings(self):
        settings_window = SettingsWindow(self.settings)
        if settings_window.exec_():
            # Updates the temp label to reflect the new temp settings
            self.temp_label.setText(f"Temp: {self.settings.value('temp1', '350')}°{self.settings.value("temp_type", "F")}")
       
    def update_timer(self):
        self.elapsed_time += 1
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.timer_label.setText(f'{minutes}:{seconds:02}')
        time2 = int(self.settings.value('time2', '6')) # Remember how these values are strings? they need to be ints again
        time3 = int(self.settings.value('time3', '8')) 
        time4 = int(self.settings.value('time4', '10'))
        
        if self.elapsed_time == time2 * 60:
            self.temp_label.setText(f'Temp: {self.settings.value("temp2", "375")}°{self.settings.value("temp_type", "F")}')
            self.executor.submit(playsound, self.sound) # plays the almighty ding asynchronously
        elif self.elapsed_time == time3 * 60:
            self.temp_label.setText(f'Temp: {self.settings.value("temp3", "400")}°{self.settings.value("temp_type", "F")}')
            self.executor.submit(playsound, self.sound)
        elif self.elapsed_time == time4 * 60:
            self.temp_label.hide()
            # Woo! You made it, let's do it again!! (or not, if you don't want to)
            self.timer_label.setText('Session Done!')
            self.timer_label.setStyleSheet("font-size: 38px; color: green; font-weight: bold;")
            self.executor.submit(playsound, self.sound)
            self.timer.stop()
            self.is_complete = True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TimerApp()
    ex.show()
    sys.exit(app.exec_())