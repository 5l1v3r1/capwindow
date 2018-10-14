import sys
import os
import configparser
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore

config = configparser.ConfigParser()

def get_settings():
    
    config = configparser.ConfigParser()
    config.read('capwin.ini')
    ss_interval = config['Screenshot']['ss_interval']
    show_ss_saved = config['Server']['show_ss_saved']
    
    if show_ss_saved == "True":
        show_ss_saved = True
    else:
        show_ss_saved = False

    return int(ss_interval), show_ss_saved

class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        
        self.is_online = False
        self.ss_interval, self.show_ss_saved = get_settings()
        self.init_ui()
        
    def init_ui(self):
        
        self.setWindowTitle("CapWin GUI")
        self.setGeometry(600, 350, 255, 300)

        self.server_timer = QtCore.QTimer()
        self.server_time = QtCore.QTime(0, 0, 0)
        
        self.save_button = QtWidgets.QPushButton("Save Settings")
        self.save_label = QtWidgets.QLabel("...")
        self.ss_interval_label = QtWidgets.QLabel("Screenshot interval(ms)")
        self.ss_interval_le = QtWidgets.QSpinBox()
        self.server_info_label = QtWidgets.QLabel("Server is Offline")
        self.start_server_button = QtWidgets.QPushButton("Start Server")
        self.kill_server_button = QtWidgets.QPushButton("Kill Server")
        self.show_ss_saved_setting = QtWidgets.QRadioButton("Show screenshot info")
        self.server_timer_label = QtWidgets.QLabel("Online Time : 00:00:00")

        self.show_ss_saved_setting.setChecked(self.show_ss_saved)
        self.ss_interval_le.setMinimum(500)
        self.ss_interval_le.setMaximum(60000)
        self.ss_interval_le.setValue(self.ss_interval)
        self.ss_interval_le.setSingleStep(500)
            
        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.save_label)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addWidget(self.ss_interval_label)
        v_box.addWidget(self.ss_interval_le)
        v_box.addWidget(self.show_ss_saved_setting)
        v_box.addWidget(self.save_button)
        
        v_box2 = QtWidgets.QVBoxLayout()
        v_box2.addWidget(self.server_info_label)
        v_box2.addWidget(self.server_timer_label)
        v_box2.addWidget(self.start_server_button)
        v_box2.addWidget(self.kill_server_button)
        v_box2.addLayout(v_box)
        v_box2.addLayout(h_box)

        self.save_button.clicked.connect(self.save_settings)
        self.start_server_button.clicked.connect(self.start_server)
        self.kill_server_button.clicked.connect(self.kill_server)
        
        self.setLayout(v_box2)
        self.show()    
        
    def save_settings(self):
        new_interval = self.ss_interval_le.value()
        new_show_ss_saved = self.show_ss_saved_setting.isChecked()
        self.show_ss_saved = new_show_ss_saved
        
        config.read("capwin.ini")
        config["Screenshot"]["ss_interval"] = str(new_interval)
        config["Server"]["show_ss_saved"] = str(new_show_ss_saved)

        try:
            with open('capwin.ini', 'w') as configfile:
                config.write(configfile)

            self.save_label.setText("New interval : " + str(new_interval) + " ms | Show scrshot info : " + str(new_show_ss_saved))
        except:
            self.save_label_label.setText("Error while saving settings...")
    
    def start_server(self):
        os.system('cls')
        self.ss_interval, self.show_ss_saved = get_settings()
        print("Screenshot interval : ", self.ss_interval)
        print("Show screenshot info : ", self.show_ss_saved)

        if(self.show_ss_saved):
            #os.system('start_server.bat')
            self.server_process = subprocess.Popen(['python', 'server.py'])
            self.auto_capper_process = subprocess.Popen(['python', 'auto_capper.py'])
        else:
            #os.system('start_server_nc.bat')
            self.server_process = subprocess.Popen(['python', 'server.py'])
            self.auto_capper_process = subprocess.Popen(['pythonw', 'auto_capper.py'])

        self.is_online = True
        self.server_info_label.setText("Server is Online")
        self.server_timer.timeout.connect(self.server_timer_event)
        self.server_timer.start(1000)

    def kill_server(self):
        if (self.is_online):
            print("Killing server...")

            self.server_info_label.setText("Shutting down the server...")
            # os.system('taskkill /f /im pythonw.exe & taskkill /f /im python.exe')
            self.server_process.kill()
            self.auto_capper_process.kill()
            self.is_online = False

            self.server_timer.stop()
            self.server_timer.disconnect()
            self.server_time = QtCore.QTime(0, 0, 0)

            self.server_info_label.setText("Server is Offline")
            print("Server is offline")

    def server_timer_event(self):
        self.server_time = self.server_time.addSecs(1)
        self.server_timer_label.setText("Online Time : " + self.server_time.toString("hh:mm:ss"))

app = QtWidgets.QApplication(sys.argv)
capwin_gui = Window()
sys.exit(app.exec_())