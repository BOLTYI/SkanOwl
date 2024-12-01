from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QFileDialog, QLabel, QHBoxLayout, QFrame, QTextEdit
import sys
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QObject
import main_program
import io

class TerminalOutput(io.StringIO):
    """
    This class captures the output of print() and directs it to QTextEdit in the GUI.
    """
    def __init__(self, text_edit_widget, update_signal, previous_output):
        super().__init__()
        self.text_edit = text_edit_widget
        self.update_signal = update_signal
        self.previous_output = previous_output

    def write(self, text):
        if text != '\n':  # Avoid emitting empty lines
            if text != self.previous_output:
                self.previous_output = text
                self.update_signal.emit(f"\t{text}")

class Interface(QWidget):
    update_output_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.last_output = ""
        self.redirect_print()
        self.update_output_signal.connect(self.update_output)
        self.monitoring_running = False
        self.acquisition_running = False

    def init_ui(self):
        self.setWindowTitle("ScanOwl")
        self.showMaximized()

        # Colors
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(204, 169, 221))  
        self.setPalette(palette)

        # Main layout
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("ScanOwl")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 40px; font-weight: bold; color: #4B0082;")  
        layout.addWidget(title)
        
        # File selection sections
        for label_text, button_text, line_edit_attr, button_attr, callback in [
            ("Known MAC addresses:", "Select Known MAC File", "known_mac_path", "btn_select_known_mac", self.select_known_mac),
            ("Unknown MAC addresses:", "Select Unknown MAC File", "unknown_mac_path", "btn_select_unknown_mac", self.select_unknown_mac)
        ]:
            section = QVBoxLayout()
            label = QLabel(label_text)
            label.setStyleSheet("font-size: 14px; font-weight: bold; color: #4B0082;")
            section.addWidget(label)
            
            setattr(self, line_edit_attr, QLineEdit(self))
            line_edit = getattr(self, line_edit_attr)
            line_edit.setPlaceholderText(f"{label_text} File Path")
            line_edit.setStyleSheet("padding: 5px; border: 1px solid #D3D3D3; border-radius: 5px; min-width: 230px;")
            section.addWidget(line_edit, 0, Qt.AlignLeft)

            setattr(self, button_attr, QPushButton(button_text, self))
            button = getattr(self, button_attr)
            button.setStyleSheet("background-color: #a87abe; padding: 10px; border-radius: 5px;")
            button.clicked.connect(callback)
            section.addWidget(button, 0, Qt.AlignLeft)
            
            layout.addLayout(section)
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setStyleSheet("color: #A9A9A9;")
            layout.addWidget(line)

        # Control buttons
        control_section = QHBoxLayout()
        self.btn_mac_acquisition = QPushButton("Acquisition of MAC addresses", self)
        self.btn_mac_acquisition.setStyleSheet("background-color: #FFB6C1; padding: 10px; border-radius: 5px;")
        self.btn_mac_acquisition.clicked.connect(self.toggle_mac_acquisition)
        control_section.addWidget(self.btn_mac_acquisition)

        self.btn_network_monitoring = QPushButton("Network Monitoring", self)
        self.btn_network_monitoring.setStyleSheet("background-color: #87CEFA; padding: 10px; border-radius: 5px;")
        self.btn_network_monitoring.clicked.connect(self.toggle_network_monitoring)
        control_section.addWidget(self.btn_network_monitoring)

        self.btn_stop_program = QPushButton("Stop the program", self)
        self.btn_stop_program.setStyleSheet("background-color: #FF6347; padding: 10px; border-radius: 5px; color: white;")
        self.btn_stop_program.clicked.connect(main_program.stop_all_threads)
        control_section.addWidget(self.btn_stop_program)

        layout.addLayout(control_section)

        # Text display
        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.text_display.setPlaceholderText("The file content will appear here...")
        layout.addWidget(self.text_display)

        self.setLayout(layout)

    def toggle_mac_acquisition(self):
        if self.acquisition_running:
            main_program.stop_all_threads()
            self.acquisition_running = False
            self.btn_mac_acquisition.setText("Acquisition of MAC addresses")
        else:
            main_program.start_mac_acquisition_thread()
            self.acquisition_running = True
            self.btn_mac_acquisition.setText("Stop MAC Acquisition")

    def toggle_network_monitoring(self):
        if self.monitoring_running:
            main_program.stop_network_monitoring()
            self.monitoring_running = False
            self.btn_network_monitoring.setText("Network Monitoring")
        else:
            main_program.start_network_monitoring_threads()
            self.monitoring_running = True
            self.btn_network_monitoring.setText("Stop Monitoring")

    def select_known_mac(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select the file of known MAC addresses", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.known_mac_path.setText(file_path)
            main_program.select_known_mac(file_path)
            self.display_file_content(file_path)

    def select_unknown_mac(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select the file of unknown MAC addresses", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            self.unknown_mac_path.setText(file_path)
            main_program.select_unknown_mac(file_path)
            self.display_file_content(file_path)

    def display_file_content(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_display.setText(content)
        except Exception as e:
            self.text_display.setText(f"Error while opening the file: {e}")

    def update_output(self, text):
        cursor = self.text_display.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(text)
        self.text_display.setTextCursor(cursor)
        self.text_display.ensureCursorVisible()

    def redirect_print(self):
        sys.stdout = TerminalOutput(self.text_display, self.update_output_signal, self.last_output)
        sys.stderr = TerminalOutput(self.text_display, self.update_output_signal, self.last_output)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec_())
