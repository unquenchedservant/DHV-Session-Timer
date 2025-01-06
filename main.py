import sys
from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QFormLayout, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
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
        self.setGeometry(100, 100, 300, 200)
        
        layout = QFormLayout()
        onlyInt = QIntValidator(122,428, self)

        self.temp1_input = QLineEdit(self)
        self.temp1_input.setValidator(onlyInt)
        self.temp1_input.setText(self.settings.value('temp1', '350'))
        layout.addRow('Temp 1:', self.temp1_input)
        
        self.temp2_input = QLineEdit(self)
        self.temp2_input.setValidator(onlyInt)
        self.temp2_input.setText(self.settings.value('temp2', '375'))
        layout.addRow('Temp 2:', self.temp2_input)
        
        self.temp3_input = QLineEdit(self)
        self.temp3_input.setValidator(onlyInt)
        self.temp3_input.setText(self.settings.value('temp3', '400'))
        layout.addRow('Temp 3:', self.temp3_input)
        
        self.error_msg = QLabel('Please enter valid temperatures (122-428°F)', self)
        self.error_msg.setStyleSheet("color: red")
        layout.addWidget(self.error_msg)
        self.error_msg.hide()
        
        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)
        
        
        self.setLayout(layout)
    
    def save_settings(self):
        if not (122 <= int(self.temp1_input.text()) <= 428 and 
            122 <= int(self.temp2_input.text()) <= 428 and 
            122 <= int(self.temp3_input.text()) <= 428):
            self.error_msg.show()
            return
        
        self.settings.setValue('temp1', self.temp1_input.text())
        self.settings.setValue('temp2', self.temp2_input.text())
        self.settings.setValue('temp3', self.temp3_input.text())
        self.accept()

class TimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings('UnquenchedServant', 'DHV-Session-Timer')
        self.sound = "asset/ding.mp3"
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Timer App')
        
        self.timer_label = QLabel('0:00', self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 48px; color: black; font-weight: bold;")
        
        self.temp_label = QLabel('Temp: 350', self)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.temp_label.setStyleSheet("font-size: 12px; color: gray;")
        
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_timer)
        
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(self.stop_timer)
        
        self.reset_button = QPushButton('Reset', self)
        self.reset_button.clicked.connect(self.reset_timer)

        self.settings_button = QPushButton('Settings', self)
        self.settings_button.clicked.connect(self.open_settings)
        
        layout = QVBoxLayout()
        start_stop_layout = QHBoxLayout()
        start_stop_layout.addWidget(self.start_button)
        start_stop_layout.addWidget(self.stop_button)
        reset_settings_layout = QHBoxLayout()
        reset_settings_layout.addWidget(self.reset_button)
        reset_settings_layout.addWidget(self.settings_button)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.temp_label)
        layout.addLayout(start_stop_layout)
        layout.addLayout(reset_settings_layout)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        
        self.elapsed_time = 0
        
    def start_timer(self):
        self.reset_timer()
        self.timer.start()
        
    def stop_timer(self):
        self.reset_timer()
        
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
        
        if self.elapsed_time == 6 * 60:
            self.temp_label.setText(f'Temp: {self.settings.value("temp2", "375")}')
            playsound(self.sound)
        elif self.elapsed_time == 8 * 60:
            self.temp_label.setText(f'Temp: {self.settings.value("temp3", "400")}')
            playsound(self.sound)
        elif self.elapsed_time == 10*60:
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