import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QFormLayout, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt, QSettings
from PyQt5.QtGui import QIntValidator
from playsound import playsound

class SettingsWindow(QDialog):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Settings')
        self.setGeometry(100, 100, 600, 200)
        
        main_layout = QHBoxLayout()
        
        # Temperature settings
        temp_layout = QFormLayout()
        
        self.temp1_input = QComboBox(self)
        self.temp1_input.addItems([str(i) for i in range(122, 429)])
        self.temp1_input.setCurrentText(self.settings.value('temp1', '350'))
        temp_layout.addRow('Temp 1:', self.temp1_input)
        
        self.temp2_input = QComboBox(self)
        self.temp2_input.addItems([str(i) for i in range(122, 429)])
        self.temp2_input.setCurrentText(self.settings.value('temp2', '375'))
        temp_layout.addRow('Temp 2:', self.temp2_input)
        
        self.temp3_input = QComboBox(self)
        self.temp3_input.addItems([str(i) for i in range(122, 429)])
        self.temp3_input.setCurrentText(self.settings.value('temp3', '400'))
        temp_layout.addRow('Temp 3:', self.temp3_input)
        
        # Time settings
        time_layout = QFormLayout()
        
        self.time1_input = QLabel("0",self)
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

        # Add layouts to main layout
        main_layout.addLayout(temp_layout)
        main_layout.addLayout(time_layout)

        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save_settings)
        
        self.error_msg = QLabel('Please enter valid temperatures (122-428°F)', self)
        self.error_msg.setStyleSheet("color: red")
        self.error_msg.hide()

        layout = QVBoxLayout()
        layout.addLayout(main_layout)
        layout.addWidget(self.error_msg)
        layout.addWidget(save_button)
        
        self.setLayout(layout)
    
    def save_settings(self):
        temp1 = int(self.temp1_input.currentText())
        temp2 = int(self.temp2_input.currentText())
        temp3 = int(self.temp3_input.currentText())
        time2 = int(self.time2_input.currentText())
        time3 = int(self.time3_input.currentText())
        time4 = int(self.time4_input.currentText())
        if not time3 > time2 or not time4 > time3:
            self.error_msg.setText('Invalid time settings. Ensure each time is greater than the previous')
            self.error_msg.show()
            return
        if not (122 <= temp1 <= 428 and 
            122 <= temp2 <= 428 and 
            122 <= temp3 <= 428):
            self.error_msg.setText('Please enter valid temperatures (122-428°F)')
            self.error_msg.show()
            return
        
        self.settings.setValue('temp1', str(temp1))
        self.settings.setValue('temp2', str(temp2))
        self.settings.setValue('temp3', str(temp3))
        self.settings.setValue('time2', str(time2))
        self.settings.setValue('time3', str(time3))
        self.settings.setValue('time4', str(time4))
        self.accept()
    

class TimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('UnquenchedServant', 'DHV-Session-Timer')
        self.sound = "asset/ding.mp3"
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('DHV Session Timer')
        self.setGeometry(100, 100, 400, 150)
        
        self.timer_label = QLabel('0:00', self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 48px; color: black; font-weight: bold;")
        
        self.temp_label = QLabel('Temp: 350', self)
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
        
    def start_timer(self):
        self.reset_timer()
        self.timer.start(1000)
        
        
    def reset_timer(self):
        self.timer.stop()
        self.elapsed_time = 0
        self.timer_label.setText('0:00')
        self.timer_label.setStyleSheet("font-size: 48px; color: black; font-weight: bold;")
        self.temp_label.setText('Temp: 350')
        self.temp_label.show()

    def open_settings(self):
        settings_window = SettingsWindow(self.settings)
        if settings_window.exec_():
            self.temp_label.setText(f"Temp: {self.settings.value('temp1', '350')}")
       
    def update_timer(self):
        self.elapsed_time += 1
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.timer_label.setText(f'{minutes}:{seconds:02}')
        time2 = int(self.settings.value('time2', '6'))
        time3 = int(self.settings.value('time3', '8'))
        time4 = int(self.settings.value('time4', '10'))
        
        if self.elapsed_time == time2 * 60:
            self.temp_label.setText(f'Temp: {self.settings.value("temp2", "375")}')
            playsound(self.sound)
        elif self.elapsed_time == time3 * 60:
            self.temp_label.setText(f'Temp: {self.settings.value("temp3", "400")}')
            playsound(self.sound)
        elif self.elapsed_time == time4 * 60:
            self.temp_label.hide()
            self.timer_label.setText('Session Done!')
            self.timer_label.setStyleSheet("font-size: 38px; color: green; font-weight: bold;")
            playsound(self.sound)
            self.timer.stop()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = TimerApp()
    ex.show()
    sys.exit(app.exec_())