import asyncio
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class WifiScanner:
    def __init__(self):
        self.widget = None
        self.layout = None
        self.scroll_area = None
        self.search_box = None

    async def scan_wifi_profiles(self):
        # Retrieve all Wi-Fi profiles saved on the computer
        wifi_profiles = await asyncio.create_subprocess_shell('netsh wlan show profiles', stdout=asyncio.subprocess.PIPE)
        wifi_profiles = await wifi_profiles.stdout.read()
        wifi_profiles = wifi_profiles.decode('utf-8').split('\n')

        wifi_profile_names = [line.split(":")[1].strip() for line in wifi_profiles if "All User Profile" in line]

        # Create a widget to hold the list of Wi-Fi profiles
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)

        # Loop through each Wi-Fi profile and retrieve its password
        for profile_name in wifi_profile_names:
            try:
                wifi_password = await asyncio.create_subprocess_shell(f'netsh wlan show profile "{profile_name}" key=clear', stdout=asyncio.subprocess.PIPE)
                wifi_password = await wifi_password.stdout.read()
                wifi_password = wifi_password.decode('utf-8').split('\n')

                wifi_password = [line.split(":")[1].strip() for line in wifi_password if "Key Content" in line]

                if wifi_password:
                    wifi_password = wifi_password[0]
                else:
                    wifi_password = "Password not found"

                if wifi_password != "Password not found":
                    # Create a label for each Wi-Fi profile and add it to the layout
                    label = QLabel(profile_name)
                    label.setCursor(Qt.PointingHandCursor)
                    # Change cursor to hand when hovering over the label
                    label.setToolTip(wifi_password) # Set the password as a tooltip
                    label.mousePressEvent = lambda event, name=profile_name, password=wifi_password: self.copy_password_to_clipboard(name, password, event) # Assign a mouse press event to copy the password to clipboard
                    self.layout.addWidget(label)

            except asyncio.subprocess.CalledProcessError:
                pass

        # Set the widget with the Wi-Fi profile labels as the widget of the scroll area
        self.scroll_area.setWidget(self.widget)
        self.search_box.setEnabled(True)

    def copy_password_to_clipboard(self, name, password, event):
        # Copy the password to the clipboard when the label is clicked
        clipboard = QApplication.clipboard()
        clipboard.setText(password)

if __name__ == '__main__':
    async def main():
        app = QApplication([])
        scanner = WifiScanner()
        scanner.scroll_area = None  # Replace None with your scroll area widget
        scanner.search_box = None  # Replace None with your search box widget
        await scanner.scan_wifi_profiles()
        app.exec()

    asyncio.run(main())
