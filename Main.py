import subprocess
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtWidgets import QTextEdit, QMessageBox


class ScrollableMessageBox(QtWidgets.QDialog):
    def __init__(self, text):
        super().__init__()

        self.setWindowTitle('Wi-Fi Passwords')
        self.setModal(True)

        # Create a label to display the text
        lbl_text = QtWidgets.QLabel(text)
        lbl_text.setWordWrap(True)
        lbl_text.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        # Create a scroll area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(lbl_text)

        # Create a vertical layout and add the scroll area to it
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(scroll_area)
        self.setLayout(layout)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Wi-Fi Pass Finder')
        self.setFixedSize(300, 150)
        self.center()

        

    # Create a label to display "Please wait..." message
        self.lbl_wait = QtWidgets.QLabel(self)
        self.lbl_wait.setGeometry(0, 50, 300, 100)
        self.lbl_wait.setAlignment(QtCore.Qt.AlignCenter)

        # Create a button to display Wi-Fi passwords
        btn_display = QtWidgets.QPushButton('Display Saved Wi-Fi Passwords', self)
        btn_display.setGeometry(50, 10, 200, 30)
        btn_display.clicked.connect(self.display_wifi_passwords)
        # Add an icon to the button
        icon_display = QtGui.QIcon('path/to/icon.png')
        btn_display.setIcon(icon_display)

        # Create a button to open Github
        btn_github = QtWidgets.QPushButton('Github', self)
        btn_github.setGeometry(50, 50, 200, 30)
        btn_github.clicked.connect(self.open_link)
        # Add an icon to the button
        icon_github = QtGui.QIcon("C:\\Users\\Jonadab Emeribe\\Downloads\\github.png")
        btn_github.setIcon(icon_github)

     
                    

        # Add some styling
        self.setStyleSheet('''
            QWidget {
                background-color: #FFFFFF;
            }
            QPushButton {
                background-color: #4CAF50;
                color: #FFFFFF;
                border: none;
                border-radius: 5px;
                padding: 7px 7px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #3E8E41;
            }
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #4CAF50;
            }
        ''')

    def display_wifi_passwords(self):
        self.lbl_wait.setText('Fetching Wi-Fi passwords...')
        self.lbl_wait.repaint()
        cmd = 'powershell.exe -Command "$networkList = netsh wlan show profiles; foreach ($network in $networkList) {if ($network -match \'All User Profile\s*: (.*)\') {$profileName = $matches[1].Trim(); $keyMaterial = netsh wlan show profile name=$profileName key=clear | Select-String \'Key Content\'; if ($keyMaterial) {$password = $keyMaterial -replace \'Key Content\s*: \', \'\'; Write-Host \"$profileName : $password\"}}}"'
        output = subprocess.check_output(cmd, shell=True, text=True)
        self.lbl_wait.setText('Wi-Fi passwords:')
        msg_box = ScrollableMessageBox(output)
        msg_box.setStyleSheet("background-color: white : darkblue;")
        # Create a "Save to Text" button
        btn_save = QtWidgets.QPushButton('Save to Text', msg_box)
      


        # Set button style
        btn_save.setStyleSheet('''
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 4px;
                font-size: 12px;
            }
            
            QPushButton:hover {
                background-color: #005DA5;
            }
            
            QPushButton:pressed {
                background-color: #004884;
            }
        ''')

        # Connect button to save_to_text method
        btn_save.clicked.connect(lambda: self.save_to_text(output))


        # Add the button to the layout
        layout = msg_box.layout()
        layout.addWidget(btn_save)


        
        msg_box.exec_()


    from PyQt5.QtWidgets import QTextEdit, QMessageBox

    def save_to_text(self, text):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save to Text', '', 'Text Files (*.txt)')
        if file_path:
            with open(file_path, 'w') as f:
                f.write(text)
            # Display a message box with the saved file's contents
            with open(file_path, 'r') as f:
                saved_text = f.read()
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Text Saved")
            msg_box.setText("The following Wi-fi PassWord has been saved to file:\n\n{}".format(saved_text))
            msg_box.exec_()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtWidgets.QApplication.desktop().screenNumber(QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def open_link(self):
        url = QUrl("https://github.com/jonadabbanks/Wi-Fi-Pass-Finder")
        QDesktopServices.openUrl(url)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    app.setWindowIcon(QtGui.QIcon("C:\\Users\\Jonadab Emeribe\\Downloads\\wifi.png"))
    window.show()
    sys.exit(app.exec_())
