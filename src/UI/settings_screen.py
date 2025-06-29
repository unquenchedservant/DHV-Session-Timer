"""
Handles all settings window UI and logic
"""
from PyQt6.QtWidgets import QComboBox, QLineEdit, QCheckBox, QFormLayout, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt6.QtGui import QIntValidator
from PyQt6 import QtCore
import math
from sys import platform

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
        self.keep_active = self.settings.value('keep_active_default', "False") == "True"
        self.notifications = self.settings.value('notifications', 'True') == "True"
        self.almightyDing = self.settings.value('almightyDing', 'True') == "True"
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

        self.notifications_checkbox = QCheckBox(self)
        self.notifications_checkbox.setChecked(self.notifications)
        self.notifications_checkbox.stateChanged.connect(self.handle_notifications)
        temp_layout.addRow("Notifications:", self.notifications_checkbox)
        


        # Create a widget to hold the temp layout, used for spacing
        temp_widget = QWidget() 
        temp_widget.setLayout(temp_layout)
        temp_widget.setFixedWidth(200) # aforementioned spacing
        
        # Time settings
        time_layout = QFormLayout() # Like what we did for temp, but with time.
        
        self.time1_input = QComboBox(self) # Time 1 will always be 0 seconds, so it's disabled and perma-set to 0
        self.time1_input.addItem("0") 
        self.time1_input.setEnabled(False) 
        time_layout.addRow('Start Time (min)', self.time1_input)
        
        self.time2_input = QComboBox(self)
        self.time2_input.addItems([str(i) for i in range(1,25)]) # Time 2-3 can be 1-25 minutes
        self.time2_input.setCurrentText(self.settings.value('time2', '6')) 
        time_layout.addRow('Stg. 2 Time (min):', self.time2_input)
        
        self.time3_input = QComboBox(self)
        self.time3_input.addItems([str(i) for i in range(1,25)])
        self.time3_input.setCurrentText(self.settings.value('time3', '8'))
        time_layout.addRow('Stg. 3 Time (min):', self.time3_input)

        self.time4_input = QComboBox(self)
        self.time4_input.addItems([str(i) for i in range(8,25)]) #Since 8 minutes is the lower limit for the auto-shutoff on the Solo 3, this will do
        self.time4_input.setCurrentText(self.settings.value('time4', '10'))
        time_layout.addRow('End Time (min):', self.time4_input)

        if not platform == "darwin":
            self.notification_timeout = QLineEdit(self)
            self.notification_timeout.setValidator(onlyInt)
            self.notification_timeout.setText(self.settings.value('timeout', '10'))
            self.notification_timeout.setFixedWidth(40)
            time_layout.addRow('Notif. Timeout:', self.notification_timeout)

        self.almighty_ding_checkbox = QCheckBox(self)
        self.almighty_ding_checkbox.setChecked(self.almightyDing)
        self.almighty_ding_checkbox.stateChanged.connect(self.handle_almighty_ding)
        time_layout.addRow('Ding:', self.almighty_ding_checkbox)

        time_widget = QWidget() # spacing again
        time_widget.setLayout(time_layout)
        time_widget.setFixedWidth(200)

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
    
    def handle_notifications(self):
        self.settings.setValue('notifications', f"{self.notifications_checkbox.isChecked()}")

    def handle_almighty_ding(self):
        self.settings.setValue('almightyDing', f"{self.almighty_ding_checkbox.isChecked()}")

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
        self.settings.setValue('temp_type', 'F')
        self.settings.setValue('time2', '6')
        self.settings.setValue('time3', '8')
        self.settings.setValue('time4', '10')
        self.settings.setValue("notifications", "True")
        self.settings.setValue('keep_active_default', "False")
        self.settings.setValue("timeout", "10")
        self.settings.setValue('almightyDing', "True")
        self.temp1_input.setText('350')
        self.temp2_input.setText('375')
        self.temp3_input.setText('400')
        self.time2_input.setCurrentText('6')
        self.time3_input.setCurrentText('8')
        self.time4_input.setCurrentText('10')
        self.temp_unit.setCurrentText('F')
        self.notification_timeout.setText("10")
        self.notifications_checkbox.setChecked(True)
        self.keep_active_default_slider.setChecked(False)
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
        notifchecked = str(self.notifications_checkbox.isChecked())
        dingChecked = str(self.almighty_ding_checkbox.isChecked())
        keepActive = str(self.keep_active_default_slider.isChecked())
        self.settings.setValue('temp1', str(temp1))
        self.settings.setValue('temp2', str(temp2))
        self.settings.setValue('temp3', str(temp3))
        self.settings.setValue('time2', str(time2))
        self.settings.setValue('time3', str(time3))
        self.settings.setValue('time4', str(time4))
        if not platform == "darwin":
            self.settings.setValue('timeout', self.notification_timeout.text())
        self.settings.setValue("almightyDing", dingChecked) # Save the almighty ding status
        self.settings.setValue("notifications", notifchecked) # Save the notification settin
        #self.settings.setValue('notifications', notifchecked)
        self.settings.setValue("temp_type", unit)
        self.settings.setValue('keep_active_default', keepActive)
        self.accept() # Save them settings!
