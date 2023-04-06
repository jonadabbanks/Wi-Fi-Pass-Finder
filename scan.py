import subprocess
from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget

class NetworkWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.text_edit = QTextEdit()
        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        self.setLayout(layout)
        
        # Run the netsh command and display the output in the window
        process = subprocess.Popen("netsh wlan show networks mode=bssid", stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        self.text_edit.setText(output.decode())

if __name__ == "__main__":
    app = QApplication([])
    window = NetworkWindow()
    window.show()
    app.exec_()
