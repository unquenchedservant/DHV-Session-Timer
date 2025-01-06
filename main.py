import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QLineEdit, QShortcut, QFormLayout, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
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
       # self.setGeometry(100, 100, 600, 200)

        onlyInt = QIntValidator(50, 428, self)
        
        main_layout = QHBoxLayout()
        
        # Temperature settings
        temp_layout = QFormLayout()
        
        self.temp1_input = QLineEdit(self)
        self.temp1_input.setValidator(onlyInt)
        self.temp1_input.setText(self.settings.value('temp1', '350'))
        self.temp1_input.setFixedWidth(40)
        temp_layout.addRow('Temp 1:', self.temp1_input)
        
        self.temp2_input = QLineEdit(self)
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
        self.temp_unit.addItems(['F', 'C'])
        self.temp_unit.setCurrentText(self.settings.value('temp_type', 'F'))
        self.temp_unit.currentIndexChanged.connect(self.temp_unit_change)
        self.temp_unit.setFixedWidth(40)
        temp_layout.addRow('Temp Unit:', self.temp_unit)

        temp_widget = QWidget()
        temp_widget.setLayout(temp_layout)
        temp_widget.setFixedWidth(140)
        
        # Time settings
        time_layout = QFormLayout()
        
        self.time1_input = QComboBox(self)
        self.time1_input.addItem("0")
        self.time1_input.setEnabled(False)
        time_layout.addRow('Time (min)', self.time1_input)
        
        self.time2_input = QComboBox(self)
        self.time2_input.addItems([str(i) for i in range(1,25)])
        self.time2_input.setCurrentText(self.settings.value('time2', '6'))
        time_layout.addRow('Time (min):', self.time2_input)
        
        self.time3_input = QComboBox(self)
        self.time3_input.addItems([str(i) for i in range(1,25)])
        self.time3_input.setCurrentText(self.settings.value('time3', '8'))
        time_layout.addRow('Time (min):', self.time3_input)

        self.time4_input = QComboBox(self)
        self.time4_input.addItems([str(i) for i in range(8,25)])
        self.time4_input.setCurrentText(self.settings.value('time4', '10'))
        time_layout.addRow('End Time (min):', self.time4_input)

        time_widget = QWidget()
        time_widget.setLayout(time_layout)
        time_widget.setFixedWidth(140)

        # Add layouts to main layout
        main_layout.addWidget(temp_widget)
        main_layout.addWidget(time_widget)

        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save_settings)

        reset_button = QPushButton('Reset', self)
        reset_button.clicked.connect(self.reset_settings)
        
        self.error_msg = QLabel('Please enter valid temperatures (122-428°F)', self)
        self.error_msg.setStyleSheet("color: red")
        self.error_msg.hide()

        layout = QVBoxLayout()
        layout.addLayout(main_layout)
        layout.addWidget(self.error_msg)
        layout.addWidget(save_button)
        layout.addWidget(reset_button)
        
        self.setLayout(layout)

    

    def temp_unit_change(self):
        if self.temp_unit.currentText() == "F":
            self.temp1_input.setText(str(self.c_to_f(int(self.temp1_input.text()))))
            self.temp2_input.setText(str(self.c_to_f(int(self.temp2_input.text()))))
            self.temp3_input.setText(str(self.c_to_f(int(self.temp3_input.text()))))
        else:
            self.temp1_input.setText(str(self.f_to_c(int(self.temp1_input.text()))))
            self.temp2_input.setText(str(self.f_to_c(int(self.temp2_input.text()))))
            self.temp3_input.setText(str(self.f_to_c(int(self.temp3_input.text()))))


    def f_to_c(self, f_temp):
        return math.floor((f_temp - 32) * 5/9)
    
    def c_to_f(self, c_temp):
        return math.ceil(c_temp * 9/5 + 32)
    
    def reset_settings(self):
        '''
        the following could be used to save the values automatically on reset
        but I found that it does some weird things if you close the settings window
        instead of saving after a reset, so i'm just going to leave it out for now

        self.settings.setValue('temp1', '350')
        self.settings.setValue('temp2', '375')
        self.settings.setValue('temp3', '400')
        self.settings.setValue('time2', '6')
        self.settings.setValue('time3', '8')
        self.settings.setValue('time4', '10')
        self.settings.setValue("temp_type", "F")
        '''
        self.temp1_input.setText('350')
        self.temp2_input.setText('375')
        self.temp3_input.setText('400')
        self.time2_input.setCurrentText('6')
        self.time3_input.setCurrentText('8')
        self.time4_input.setCurrentText('10')
        self.temp_unit.setCurrentText('F')
    
    def save_settings(self):
        temp1 = int(self.temp1_input.text())
        temp2 = int(self.temp2_input.text())
        temp3 = int(self.temp3_input.text())
        time2 = int(self.time2_input.currentText())
        time3 = int(self.time3_input.currentText())
        time4 = int(self.time4_input.currentText())
        unit = self.temp_unit.currentText()
        if not time3 > time2 or not time4 > time3:
            self.error_msg.setText('Invalid time settings. Ensure each time is greater than the previous')
            self.error_msg.show()
            return
        if unit == "F":
            if not (122 <= temp1 <= 428 and 
                122 <= temp2 <= 428 and 
                122 <= temp3 <= 428):
                self.error_msg.setText('Please enter valid temperatures (122-428°F)')
                self.error_msg.show()
                return
        else:
            if not (50 <= temp1 <= 220 and 
                50 <= temp2 <= 220 and 
                50 <= temp3 <= 220):
                self.error_msg.setText('Please enter valid temperatures (50-220°C)')
                self.error_msg.show()
                return
        
        self.settings.setValue('temp1', str(temp1))
        self.settings.setValue('temp2', str(temp2))
        self.settings.setValue('temp3', str(temp3))
        self.settings.setValue('time2', str(time2))
        self.settings.setValue('time3', str(time3))
        self.settings.setValue('time4', str(time4))
        self.settings.setValue("temp_type", unit)
        self.accept()
    

class TimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('UnquenchedServant', 'DHV-Session-Timer')
        self.sound = "asset/ding.mp3"
        self.executor = concurrent.futures.ThreadPoolExecutor()
        self.is_complete = False
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('DHV Session Timer')
        self.setGeometry(100, 100, 400, 150)
        
        self.timer_label = QLabel('0:00', self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 48px; color: black; font-weight: bold;")
        
        self.temp_label = QLabel(f"Temp: {self.settings.value('temp1', '350')}°{self.settings.value("temp_type", "F")}", self)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setStyleSheet("font-size: 12px; color: gray;")
        
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_timer)
        
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_timer)

        self.settings_button = QPushButton('Settings', self)
        self.settings_button.clicked.connect(self.open_settings)
        
        layout = QVBoxLayout()
        start_reset_layout = QHBoxLayout()
        start_reset_layout.addWidget(self.start_button)
        start_reset_layout.addWidget(self.reset_button)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.temp_label)
        layout.addLayout(start_reset_layout)
        layout.addWidget(self.settings_button)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        
        self.elapsed_time = 0

        self.start_shortcut = QShortcut(QKeySequence("Space"), self)
        self.start_shortcut.activated.connect(self.handle_spacebar)

    def handle_spacebar(self):
        if self.timer.isActive():
            self.reset_timer()
        else:
            self.start_timer()
        
    def start_timer(self):
        if self.is_complete:
            self.is_complete = False
            self.reset_timer()
        self.timer.start(1000)
        
        
    def reset_timer(self):
        self.timer.stop()
        self.elapsed_time = 0
        self.timer_label.setText('0:00')
        self.timer_label.setStyleSheet("font-size: 48px; color: black; font-weight: bold;")
        self.temp_label.setText(f"Temp: {self.settings.value('temp1', '350')}°{self.settings.value("temp_type", "F")}")
        self.temp_label.show()

    def open_settings(self):
        settings_window = SettingsWindow(self.settings)
        if settings_window.exec_():
            self.temp_label.setText(f"Temp: {self.settings.value('temp1', '350')}°{self.settings.value("temp_type", "F")}")
       
    def update_timer(self):
        self.elapsed_time += 1
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.timer_label.setText(f'{minutes}:{seconds:02}')
        time2 = int(self.settings.value('time2', '6'))
        time3 = int(self.settings.value('time3', '8'))
        time4 = int(self.settings.value('time4', '10'))
        
        if self.elapsed_time == time2 * 60:
            self.temp_label.setText(f'Temp: {self.settings.value("temp2", "375")}°{self.settings.value("temp_type", "F")}')
            self.executor.submit(playsound, self.sound)
        elif self.elapsed_time == time3 * 60:
            self.temp_label.setText(f'Temp: {self.settings.value("temp3", "400")}°{self.settings.value("temp_type", "F")}')
            self.executor.submit(playsound, self.sound)
        elif self.elapsed_time == time4 * 60:
            self.temp_label.hide()
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