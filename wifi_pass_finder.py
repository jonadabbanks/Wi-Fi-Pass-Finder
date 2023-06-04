import subprocess
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QScrollArea, QVBoxLayout, QWidget, QLabel, QMessageBox, QLineEdit, QDesktopWidget
from PyQt5.QtGui import QIcon, QClipboard, QGuiApplication, QFont, QColor
import sys
import os


# Function to get the absolute path to a resource file
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# Main class for the Wi-Fi scanner application
class WifiScanner(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window icon
        icon = QIcon(resource_path("img/logo.png"))
        self.setWindowIcon(icon)

        # Create a button to scan Wi-Fi profiles
        self.scan_button = QPushButton("Scan Saved Wi-Fi", self)
        self.scan_button.clicked.connect(self.scan_wifi_profiles)
        icon = QIcon(resource_path("img/logo.png"))
        self.scan_button.setIcon(icon)

        # Set the window size
        self.resize(600, 400)

        # Center the window on the screen
        self.center_window()

        # Set up the user interface elements
        self.setup_ui()

    def center_window(self):
        # Get the screen's geometry
        screen_geometry = QDesktopWidget().screenGeometry()

        # Calculate the center point
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2

        # Move the window to the center
        self.move(x, y)

    def setup_ui(self):
        # Create a search box for filtering Wi-Fi profiles
        self.search_box = QLineEdit(self)
        self.search_box.setPlaceholderText("Search Wi-Fi profiles...")
        self.search_box.textChanged.connect(self.filter_wifi_profiles)
        self.search_box.setEnabled(False)

        # Create a scroll area to display Wi-Fi profiles
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # Create a main widget to hold the scan button, search box, and scroll area
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        main_layout.addWidget(self.scan_button)
        main_layout.addWidget(self.search_box)
        main_layout.addWidget(self.scroll_area)

        # Set the main widget as the central widget of the window
        self.setCentralWidget(main_widget)

        self.setWindowTitle("Wi-Fi Pass Finder")

        # Apply stylesheet to customize the appearance
        self.setStyleSheet("""
            QMainWindow {
                background-color: #d3d3d3;
                border-radius: 7px;
            }
            QPushButton {
                background-color: #007BFF;
                color: #FFFFFF;
                border-radius: 7px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit {
                background-color: #EFEFEF;
                border: 1px solid #999999;
                border-radius: 5px;
                padding: 5px;
            }
            QLabel {
                color: #007BFF;
            }
            QScrollArea {
                background-color: #c4c3d0
            }
        """)

    def scan_wifi_profiles(self):
        # Disable the scan button while scanning is in progress
        self.scan_button.setEnabled(False)

        # Create a QLabel for the scanning message
        scanning_label = QLabel("Scanning for Wi-Fi passwords...")
        scanning_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scanning_label.setFont(QFont("Arial", 16, QFont.Bold))

        # Set the scanning label as the central widget of the scroll area
        self.scroll_area.setWidget(scanning_label)
        self.search_box.setEnabled(False)
        self.repaint()

        # Create a worker thread for scanning Wi-Fi profiles
        self.worker = WifiScanWorker()
        self.worker.finished.connect(self.on_wifi_scan_finished)
        self.worker.start()

    def on_wifi_scan_finished(self, wifi_profiles):
        if wifi_profiles is None:
            # If no Wi-Fi card is found, output a message on the screen
            label = QLabel("No Wi-Fi card found on this system")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFont(QFont("Arial", 16, QFont.Bold))
            self.scroll_area.setWidget(label)
            self.search_box.setEnabled(False)
        else:
            # Create a widget to hold the list of Wi-Fi profiles
            self.widget = QWidget()
            self.layout = QVBoxLayout(self.widget)

            # Loop through each Wi-Fi profile and retrieve its password
            for profile_name, wifi_password in wifi_profiles.items():
                if wifi_password != "Password not found":
                    # Create a label for each Wi-Fi profile and add it to the layout
                    label = QLabel(profile_name)
                    label.setCursor(Qt.PointingHandCursor)  # Change cursor to hand when hovering over the label
                    label.setToolTip(wifi_password)  # Set the password as a tooltip
                    label.mousePressEvent = lambda event, name=profile_name, password=wifi_password: self.copy_password_to_clipboard(
                        name, password, event)  # Assign a mouse press event to copy the password to clipboard
                    self.layout.addWidget(label)

            # Set the widget with the Wi-Fi profile labels as the widget of the scroll area
            self.scroll_area.setWidget(self.widget)
            self.search_box.setEnabled(True)

        # Re-enable the scan button
        self.scan_button.setEnabled(True)

    def filter_wifi_profiles(self, text):
        # Loop through each label in the layout and hide or show it based on whether the search text is in its name
        for i in range(self.layout.count()):
            label = self.layout.itemAt(i).widget()
            if text.lower() in label.text().lower():
                label.show()
            else:
                label.hide()

    def copy_password_to_clipboard(self, name, password, event):
        # Copy the password to clipboard when the label is clicked
        clipboard = QApplication.clipboard()
        clipboard.setText(password, mode=QClipboard.Clipboard)
        QMessageBox.information(self, f"{name} Password Copied", "The password has been copied to clipboard.")


# Worker thread class for scanning Wi-Fi profiles
class WifiScanWorker(QThread):
    finished = pyqtSignal(dict)

    def run(self):
        wifi_profiles = {}

        # Check if the system has a Wi-Fi card
        try:
            subprocess.check_output(['netsh', 'wlan', 'show', 'drivers'])
        except subprocess.CalledProcessError:
            # If no Wi-Fi card is found, return None
            self.finished.emit(None)
            return

        # Retrieve all Wi-Fi profiles saved on the computer
        wifi_profiles_output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
        wifi_profile_names = [line.split(":")[1].strip() for line in wifi_profiles_output if "All User Profile" in line]

        # Loop through each Wi-Fi profile and retrieve its password
        for profile_name in wifi_profile_names:
            try:
                wifi_password_output = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile_name, 'key=clear']).decode('utf-8').split('\n')
                wifi_password = [line.split(":")[1].strip() for line in wifi_password_output if "Key Content" in line]
                if wifi_password:
                    wifi_password = wifi_password[0]
                else:
                    wifi_password = "Password not found"

                wifi_profiles[profile_name] = wifi_password

            except subprocess.CalledProcessError:
                pass

        self.finished.emit(wifi_profiles)


if __name__ == '__main__':
    app = QApplication([])
    wifi_scanner = WifiScanner()
    wifi_scanner.show()
    app.exec()
