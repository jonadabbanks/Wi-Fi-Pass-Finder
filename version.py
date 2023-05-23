import os

from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout

import os

# Define the path to search for virtual environments
path_to_search = "/"

# Define a list to store the paths of virtual environments
venv_paths = []

# Define a function to check if a directory is a virtual environment
def is_venv(directory):
    return os.path.isfile(os.path.join(directory, "pyvenv.cfg"))

# Recursively search for virtual environments in the specified path
for root, dirs, files in os.walk(path_to_search):
    for directory in dirs:
        if is_venv(os.path.join(root, directory)):
            venv_paths.append(os.path.join(root, directory))

class EnvironmentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Virtual Environment Selector')
        self.setGeometry(100, 100, 300, 100)
        
        # Create a label for the dropdown list
        self.label = QLabel('Select a virtual environment:', self)
        self.label.move(20, 20)
        
        # Create a dropdown list of virtual environments found
        self.dropdown = QComboBox(self)
        self.dropdown.move(20, 50)
        if len(venv_paths) == 0:
            self.dropdown.addItem('No virtual environments found.')
        else:
            self.dropdown.addItem('Select a virtual environment')
            for venv_path in venv_paths:
                self.dropdown.addItem(venv_path)
        self.dropdown.currentIndexChanged.connect(self.update_system_path)

        # Create a button to activate the selected virtual environment
        self.activate_button = QPushButton('Activate', self)
        self.activate_button.move(180, 50)
        self.activate_button.clicked.connect(self.activate_venv)
        
        # Create a layout for the widget
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.dropdown)
        layout.addWidget(self.activate_button)
        
    def update_system_path(self):
        # Update the system path to the selected virtual environment
        selected_path = self.dropdown.currentText()
        if selected_path in venv_paths:
            os.environ['PATH'] = os.path.join(selected_path, 'bin') + os.pathsep + os.environ['PATH']
            print(f'System path updated to {selected_path}')
    
    def activate_venv(self):
        # Activate the selected virtual environment
        selected_path = self.dropdown.currentText()
        if selected_path in venv_paths:
            activate_script = os.path.join(selected_path, 'Scripts', 'activate')
            os.system(f'cmd /k {activate_script}')
            print(f'{selected_path} activated.')
    
if __name__ == '__main__':
    app = QApplication([])
    window = EnvironmentWindow()
    window.show()
    app.exec()
