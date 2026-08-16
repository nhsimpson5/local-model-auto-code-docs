import sys
import os

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

def open_file_directory(prompt: str):
    file_path = QFileDialog.getExistingDirectory(window, prompt)
    return file_path

class button():
    def __init__(self, name: str):
        self.title = QPushButton("")
        self.title.clicked.connect(self.button_function)

    def button_function(self):
        pass


class folder_search_button(button):
    def __init__(self, name: str):
        self.main = QPushButton(name)
        self.chosen_folder_file_path = ""
        self.chosen_folder_name = ""
        self.chosen_folder_display = QLabel("No folder selected")
        self.main.clicked.connect(self.button_function)
        layout.addWidget(self.main)
        layout.addWidget(self.chosen_folder_display)
        
    def button_function(self):
        self.chosen_folder_file_path = open_file_directory("Select a folder")
        self.chosen_folder_name = os.path.basename(self.chosen_folder_file_path)
        self.chosen_folder_display.setText(self.chosen_folder_name)


window.setWindowTitle("Auto Code Documentation & Formatting")
folder_search_button_a = folder_search_button("Select Folder")
window.resize(400, 300)
window.setLayout(layout)
window.show()

sys.exit(app.exec())
