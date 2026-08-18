import sys
import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QComboBox
from pipeline import run_pipeline, CONVENTION_BY_LANGUAGE

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()

def open_file_directory(prompt: str):
    file_path = QFileDialog.getExistingDirectory(window, prompt)
    return file_path


class button():
    def __init__(self, title: str, style):
        self.main = QPushButton(title)
        self.main.clicked.connect(self.button_function)
        self.layout = style

    def set_layout(self):
        self.layout.addWidget(self.main)
        self.layout.addStretch()
        layout.addLayout(self.layout)

    def button_function(self):
        pass


class folder_button(button):
    def __init__(self, title: str, style = QVBoxLayout()):
        super().__init__(title, style)
        self.chosen_folder_file_path = ""
        self.chosen_folder_name = ""
        self.chosen_folder_display = QLabel("No folder selected")
        self.set_layout()

    def get_chosen_folder_file_path(self):
        return self.chosen_folder_file_path if self.chosen_folder_file_path != "" else None
    
    def set_layout(self):
        self.layout.addWidget(self.main)
        self.layout.addWidget(self.chosen_folder_display)
        self.layout.addStretch()
        layout.addLayout(self.layout)

    def button_function(self):
        self.chosen_folder_file_path = open_file_directory("Select a folder")
        self.chosen_folder_name = os.path.basename(self.chosen_folder_file_path)
        self.chosen_folder_display.setText(f"Folder: {self.chosen_folder_name}")


class run_button(button):
    def __init__(self, title:str, folder_button, python_dropdown, c_dropdown, cpp_dropdown, style=QVBoxLayout()):
        super().__init__(title, style)
        self.folder_button = folder_button
        self.python_dropdown = python_dropdown
        self.c_dropdown = c_dropdown
        self.cpp_dropdown = cpp_dropdown
        self.set_layout()

    def button_function(self):
        try:
            run_pipeline(self.folder_button.get_chosen_folder_file_path(), {
                                                                            "python": self.python_dropdown.get_convention(), 
                                                                            "c": self.c_dropdown.get_convention(), 
                                                                            "cpp": self.cpp_dropdown.get_convention()
                                                                            })
        except Exception as e:
            print(f"Pipeline failed: {e}")



class convention_drop_down_menu():
    def __init__(self, title: str, items: tuple, style=QHBoxLayout()):
        self.main = QComboBox()
        self.title = QLabel(f"{title} conventions: ")
        self.main.addItems(items)
        self.layout = style
        self.set_layout(self.title, self.main)

    def get_convention(self):
        print(self.main.currentText())
        return self.main.currentText()

    def set_layout(self, *widgets):
        for widget in widgets:
            self.layout.addWidget(widget)
        self.layout.addStretch()
        layout.addLayout(self.layout)
        
        
window.setWindowTitle("Auto Code Documentation & Formatting")
folder_search_button = folder_button("Select Folder")
python_convention_drop_down_menu = convention_drop_down_menu("Python", CONVENTION_BY_LANGUAGE["python"])
c_convention_drop_down_menu = convention_drop_down_menu("C", CONVENTION_BY_LANGUAGE["c"])
cpp_convention_drop_down_menu = convention_drop_down_menu("C++", CONVENTION_BY_LANGUAGE["cpp"])
generate_docstring_button = run_button("Generate Docstrings", folder_search_button, python_convention_drop_down_menu, c_convention_drop_down_menu, cpp_convention_drop_down_menu)
window.resize(250, 200)
window.setLayout(layout)
window.show()

sys.exit(app.exec())
