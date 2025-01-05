import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt
from playsound import playsound

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Settings')
        self.setGeometry(100, 100, 200, 100)
        
        layout = QVBoxLayout()
        
        # Add settings widgets here
        # Example: QLabel
        label = QLabel('Settings go here', self)
        layout.addWidget(label)
        
        self.setLayout(layout)
class TimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
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
        self.timer.start(1000)
        
    def stop_timer(self):
        self.timer.stop()
        
    def reset_timer(self):
        self.timer.stop()
        self.elapsed_time = 0
        self.timer_label.setText('0:00')

    def open_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.exec_()
       
    def update_timer(self):
        self.elapsed_time += 1
        minutes = self.elapsed_time // 60
        seconds = self.elapsed_time % 60
        self.timer_label.setText(f'{minutes}:{seconds:02}')
        
        if self.elapsed_time == 6 * 60:
            self.temp_label.setText('Temp: 375')
            playsound(self.sound)
        elif self.elapsed_time == 8 * 60:
            self.temp_label.setText('Temp: 400')
            playsound(self.sound)
        elif self.elapsed_time == 10 * 60:
            self.temp_label.hide()
            playsound(self.sound)
            self.timer_label.setText('Session Done!')
            self.timer.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TimerApp()
    ex.show()
    sys.exit(app.exec_())