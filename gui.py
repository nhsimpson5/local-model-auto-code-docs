import sys
import os

from PySide6.QtCore import QObject, QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QLabel,
    QComboBox,
    QCheckBox,
    QProgressBar,
)
from pipeline import run_pipeline, CONVENTION_BY_LANGUAGE

app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()


def open_file_directory(prompt: str):
    file_path = QFileDialog.getExistingDirectory(window, prompt)
    return file_path


class button:
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
    def __init__(self, title: str, style=QVBoxLayout()):
        super().__init__(title, style)
        self.chosen_folder_file_path = ""
        self.chosen_folder_name = ""
        self.chosen_folder_display = QLabel("No folder selected")
        self.set_layout()

    def get_chosen_folder_file_path(self):
        return (
            self.chosen_folder_file_path if self.chosen_folder_file_path != "" else None
        )

    def set_layout(self):
        self.layout.addWidget(self.main)
        self.layout.addWidget(self.chosen_folder_display)
        self.layout.addStretch()
        layout.addLayout(self.layout)

    def button_function(self):
        self.chosen_folder_file_path = open_file_directory("Select a folder")
        self.chosen_folder_name = os.path.basename(self.chosen_folder_file_path)
        self.chosen_folder_display.setText(f"Folder: {self.chosen_folder_name}")


class PipelineWorker(QObject):
    finished = Signal()
    progress = Signal(int, int, str)
    error = Signal(str)

    def __init__(self, target_folder, format_check, convention_by_language):
        super().__init__()
        self.target_folder = target_folder
        self.format_check = format_check
        self.convention_by_language = convention_by_language

    def run(self):
        try:
            run_pipeline(
                self.target_folder, self.format_check, self.convention_by_language, on_progress=self.progress.emit
            )
        except Exception as e:
            self.error.emit(str(e))
        self.finished.emit()


class run_button(button):
    def __init__(
        self,
        title: str,
        format_check,
        folder_button,
        python_dropdown,
        c_dropdown,
        cpp_dropdown,
        style=QVBoxLayout(),
    ):
        super().__init__(title, style)
        self.format_check = format_check
        self.folder_button = folder_button
        self.python_dropdown = python_dropdown
        self.c_dropdown = c_dropdown
        self.cpp_dropdown = cpp_dropdown
        self.docstring_progress_bar = None
        self.set_layout()

    def disable_button(self):
        self.main.setEnabled(False)
        self.main.setText("Running...")
        
    def enable_button(self):
        self.main.setEnabled(True)
        self.main.setText("Run")

    def button_function(self):
        self.disable_button()
        self.docstring_progress_bar = docstring_progress_bar
        self.docstring_progress_bar.reset_bar()
        self.docstring_progress_bar.show_bar()
        folder = self.folder_button.get_chosen_folder_file_path()
        format_check = self.format_check.get_status()
        conventions = {
            "python": self.python_dropdown.get_convention(),
            "c": self.c_dropdown.get_convention(),
            "cpp": self.cpp_dropdown.get_convention(),
        }

        self.thread = QThread()
        self.worker = PipelineWorker(folder, format_check, conventions)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.docstring_progress_bar.update)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.enable_button)
        self.worker.finished.connect(self.docstring_progress_bar.hide_bar)
        self.worker.error.connect(lambda msg: print(f"Pipeline failed: {msg}"))

        self.thread.start()

 
class convention_drop_down_menu:
    def __init__(self, title: str, items: tuple, style=None):
        style = QHBoxLayout()
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


class format_check_box:
    def __init__(self, style=None):
        style = QHBoxLayout()
        self.main = QCheckBox()
        self.title = QLabel(f"Format code ? ")
        self.layout = style
        self.set_layout(self.title, self.main)

    def set_layout(self, *widgets):
        for widget in widgets:
            self.layout.addWidget(widget)
        self.layout.addStretch()
        layout.addLayout(self.layout)

    def get_status(self):
        return self.main.isChecked()


class progress_bar:
    def __init__(self, style=None):
        style = QVBoxLayout()
        self.main = QProgressBar()
        self.title = QLabel("Progress: ")
        self.main.setValue(0)
        self.layout = style
        self.set_layout(self.title, self.main)

    def set_layout(self, *widgets):
        for widget in widgets:
            self.layout.addWidget(widget)
        self.layout.addStretch()
        layout.addLayout(self.layout)
        self.hide_bar()

    def hide_bar(self):
        self.title.hide()
        self.main.hide()

    def show_bar(self):
        self.title.show()  
        self.main.show()

    def reset_bar(self):
        self.update(0, 1, "")

    def update(self, current: int, total: int, message: str):
        self.main.setRange(0, total)
        self.main.setValue(current)
        self.title.setText(f"Progress: {message}")

        
window.setWindowTitle("Auto Code Documentation & Formatting")
folder_search_button = folder_button("Select Folder")
format_code_check_box = format_check_box()
python_convention_drop_down_menu = convention_drop_down_menu(
    "Python", CONVENTION_BY_LANGUAGE["python"]
)
c_convention_drop_down_menu = convention_drop_down_menu(
    "C", CONVENTION_BY_LANGUAGE["c"]
)
cpp_convention_drop_down_menu = convention_drop_down_menu(
    "C++", CONVENTION_BY_LANGUAGE["cpp"]
)

run_pipeline_button = run_button(
    "Run",
    format_code_check_box,
    folder_search_button,
    python_convention_drop_down_menu,
    c_convention_drop_down_menu,
    cpp_convention_drop_down_menu,
)
docstring_progress_bar = progress_bar()
window.resize(400, 300)
window.setLayout(layout)
window.show()

sys.exit(app.exec())
