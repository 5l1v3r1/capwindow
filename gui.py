import sys
import os
import webbrowser
import configparser
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore

config = configparser.ConfigParser()

def get_settings():
    
    config = configparser.ConfigParser()
    config.read('capwin.ini')
    ss_interval = config['Screenshot']['ss_interval']
    server_port = config['Server']['server_port']
    show_ss_saved = config['Server']['show_ss_saved']
    
    if show_ss_saved == "True":
        show_ss_saved = True
    else:
        show_ss_saved = False

    return int(ss_interval), server_port, show_ss_saved

class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        
        self.is_online = False
        self.ss_interval, self.server_port, self.show_ss_saved = get_settings()
        self.init_ui()
        
    def init_ui(self):
        
        self.setWindowTitle("CapWin GUI")
        self.setFixedSize(255, 300)

        self.server_timer = QtCore.QTimer()
        self.server_time = QtCore.QTime(0, 0, 0)
        
        self.save_button = QtWidgets.QPushButton("Save Settings")
        self.save_label = QtWidgets.QLabel("...")
        self.ss_interval_label = QtWidgets.QLabel("Screenshot interval(ms)  Server port")
        self.ss_interval_le = QtWidgets.QSpinBox()
        self.server_port_le = QtWidgets.QSpinBox()
        self.server_info_label = QtWidgets.QLabel("Server Status : OFFLINE")
        self.start_server_button = QtWidgets.QPushButton("Start Server")
        self.kill_server_button = QtWidgets.QPushButton("Kill Server")
        self.open_on_browser_button = QtWidgets.QPushButton("Open on browser")
        self.show_ss_saved_setting = QtWidgets.QRadioButton("Show screenshot info")
        self.server_timer_label = QtWidgets.QLabel("Online Time : 00:00:00")

        self.show_ss_saved_setting.setChecked(self.show_ss_saved)
        self.ss_interval_le.setMinimum(500)
        self.ss_interval_le.setMaximum(60000)
        self.ss_interval_le.setValue(self.ss_interval)
        self.ss_interval_le.setSingleStep(500)

        self.server_port_le.setMinimum(2)
        self.server_port_le.setMaximum(65535)
        self.server_port_le.setValue(int(self.server_port))
        self.server_port_le.setSingleStep(1)
            
        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addWidget(self.save_label)
        
        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addWidget(self.start_server_button)
        h_box2.addWidget(self.kill_server_button)

        h_box3 = QtWidgets.QHBoxLayout()
        h_box3.addWidget(self.ss_interval_le)
        h_box3.addWidget(self.server_port_le)

        v_box = QtWidgets.QVBoxLayout()
        v_box.addSpacing(30)
        v_box.addWidget(self.ss_interval_label)
        v_box.addLayout(h_box3)
        v_box.addWidget(self.show_ss_saved_setting)
        v_box.addWidget(self.save_button)
        
        v_box2 = QtWidgets.QVBoxLayout()
        v_box2.addWidget(self.server_info_label)
        v_box2.addWidget(self.server_timer_label)
        v_box2.addLayout(h_box2)
        v_box2.addWidget(self.open_on_browser_button)
        v_box2.addLayout(v_box)
        v_box2.addLayout(h_box)

        self.save_button.clicked.connect(self.save_settings)
        self.start_server_button.clicked.connect(self.start_server)
        self.kill_server_button.clicked.connect(self.kill_server)
        self.open_on_browser_button.clicked.connect(self.redirect)
        
        self.setLayout(v_box2)
        self.show()    
        
    def save_settings(self):
        self.ss_interval = self.ss_interval_le.value()
        self.server_port = self.server_port_le.value()
        self.show_ss_saved = self.show_ss_saved_setting.isChecked()
        
        config.read("capwin.ini")
        config["Screenshot"]["ss_interval"] = str(self.ss_interval)
        config['Server']['server_port'] = str(self.server_port)
        config["Server"]["show_ss_saved"] = str(self.show_ss_saved)

        try:
            with open('capwin.ini', 'w') as configfile:
                config.write(configfile)

            self.save_label.setText("New interval : " + str(self.ss_interval) + " ms | New port : " + str(self.server_port))
        except:
            self.save_label_label.setText("Error while saving settings...")
    
    def start_server(self):
        if not (self.is_online):
            os.system('cls')
            self.ss_interval, self.server_port, self.show_ss_saved = get_settings()
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
            self.server_info_label.setText("Server Status : ONLINE")
            self.server_timer.timeout.connect(self.server_timer_event)
            self.server_timer.start(1000)
        
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.setWindowTitle("Oops!")
            error_dialog.showMessage('Server is already running at localhost:' + str(self.server_port))
            error_dialog.exec()

    def kill_server(self):
        if (self.is_online):
            print("Killing server...")

            self.server_info_label.setText("Server Status : Shutting down...")
            # os.system('taskkill /f /im pythonw.exe & taskkill /f /im python.exe')
            self.server_process.kill()
            self.auto_capper_process.kill()
            self.is_online = False

            self.server_timer.stop()
            self.server_timer.disconnect()
            self.server_time = QtCore.QTime(0, 0, 0)

            self.server_info_label.setText("Server Status : OFFLINE")
            print("Server is offline")

    def server_timer_event(self):
        self.server_time = self.server_time.addSecs(1)
        self.server_timer_label.setText("Online Time : " + self.server_time.toString("hh:mm:ss"))

    def redirect(self):
        webbrowser.open_new_tab('http://localhost:' + str(self.server_port))


app = QtWidgets.QApplication(sys.argv)
capwin_gui = Window()
sys.exit(app.exec_())