from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedWidget, QLabel, QHBoxLayout, QFrame
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
import sys
import interface

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Welcome message
        title = QLabel("Welcome to ScanOwl - Your network monitoring and protection tool.")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #4B0082;")
        layout.addWidget(title)

        # Network Status
        status_section = QVBoxLayout()
        self.status_label = QLabel("🟢 Everything is fine - No issues detected.")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 18px; color: #006400; font-weight: bold;")
        status_section.addWidget(self.status_label)

        scan_button = QPushButton("Run a quick scan")
        scan_button.setStyleSheet("padding: 10px; font-size: 16px; background-color: #4B0082; color: white; border-radius: 5px;")
        scan_button.clicked.connect(self.quick_scan)
        status_section.addWidget(scan_button, alignment=Qt.AlignCenter)
        layout.addLayout(status_section)

        # Recent Activities
        activities_label = QLabel("Recent activities")
        activities_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4B0082;")
        layout.addWidget(activities_label)

        self.activities_list = QLabel("- Last analysis: 24/12/2024 at 14h.  \n- Devices analyzed: 1. \n- Recent alerts: 0.")
        self.activities_list.setStyleSheet("font-size: 16px; color: #333;")
        layout.addWidget(self.activities_list)

        # Graphs and Visualizations
        visualization_label = QLabel("Safety Visualization")
        visualization_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4B0082;")
        layout.addWidget(visualization_label)

        self.security_status = QLabel("99% sécurisé")
        self.security_status.setAlignment(Qt.AlignCenter)
        self.security_status.setStyleSheet("font-size: 20px; color: #4B0082; font-weight: bold;")
        layout.addWidget(self.security_status)

        # Quick Actions
        quick_actions_label = QLabel("Quick Links")
        quick_actions_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4B0082;")
        layout.addWidget(quick_actions_label)

        quick_actions_layout = QHBoxLayout()

        for text in ["Quick Scan", "Configure the settings", "See the logs"]:
            button = QPushButton(text)
            button.setStyleSheet("padding: 10px; font-size: 16px; background-color: #F0F0F0; border: 1px solid #CCC; border-radius: 5px;")
            quick_actions_layout.addWidget(button)

        layout.addLayout(quick_actions_layout)

        # Tips and Recommendations
        tip_label = QLabel("💡 Tip: Enable continuous network scan for better protection.")
        tip_label.setStyleSheet("font-size: 16px; color: #333; background-color: #E0E0E0; padding: 10px; border-radius: 5px;")
        layout.addWidget(tip_label)

        self.setLayout(layout)

    def quick_scan(self):
        self.status_label.setText("🟡 Attention - Une analyse est en cours...")
        self.status_label.setStyleSheet("font-size: 18px; color: #FFA500; font-weight: bold;")

class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("About ScanOwl")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4B0082;")
        layout.addWidget(label)
        self.setLayout(layout)

class InterfacePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Network Scan")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4B0082;")
        layout.addWidget(label)

        self.launch_button = QPushButton("Launch Network Scan")
        self.launch_button.setStyleSheet("padding: 10px; font-size: 16px; background-color: #4B0082; color: white; border-radius: 5px;")
        self.launch_button.clicked.connect(self.launch_interface)
        layout.addWidget(self.launch_button)

        self.setLayout(layout)

    def launch_interface(self):
        self.interface_window = interface.Interface()
        self.interface_window.show()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ScanOwl")
        self.resize(1200, 800)
        self.showMaximized()  # Automatically set the window to full-screen mode

        # Colors and styles
        self.setStyleSheet("""
            QPushButton {
                background-color: #F0F0F0;
                border: none;
                padding: 15px;
                text-align: left;
                font-size: 16px;
                color: #333;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
            QPushButton:checked {
                background-color: #4B0082;
                color: white;
            }
        """)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(169, 169, 169))  # Set a gray opaque background color
        self.setPalette(palette)

        # Main layout
        main_layout = QHBoxLayout()

        # Sidebar (Navigation)
        sidebar = QVBoxLayout()
        sidebar.setSpacing(0)

        self.nav_buttons = []

        for i, (text, page_class) in enumerate([
            ("Home", HomePage),
            ("Network Scan", InterfacePage),
            ("About", AboutPage)
        ]):
            button = QPushButton(text)
            button.setCheckable(True)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #F5F5F5;
                    border: none;
                    padding: 15px;
                    text-align: left;
                    font-size: 16px;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: #E0E0E0;
                }
                QPushButton:checked {
                    background-color: #4B0082;  /* Make selected tab purple */
                    color: white;
                }
            """)
            button.clicked.connect(lambda checked, idx=i: self.switch_page(idx))
            self.nav_buttons.append(button)
            sidebar.addWidget(button)

        sidebar.addStretch()

        # Content area (Stacked Widget)
        self.pages = QStackedWidget()
        self.pages.addWidget(HomePage())
        self.pages.addWidget(InterfacePage())
        self.pages.addWidget(AboutPage())

        # Highlight first button by default
        self.nav_buttons[0].setChecked(True)

        # Add widgets to main layout
        sidebar_frame = QFrame()
        sidebar_frame.setLayout(sidebar)
        sidebar_frame.setFixedWidth(200)
        sidebar_frame.setStyleSheet("background-color: #D3D3D3; border-right: 1px solid #DDD;")  # Adjusted sidebar color

        main_layout.addWidget(sidebar_frame)
        main_layout.addWidget(self.pages)

        self.setLayout(main_layout)

    def switch_page(self, index):
        for button in self.nav_buttons:
            button.setChecked(False)
        self.nav_buttons[index].setChecked(True)
        self.pages.setCurrentIndex(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
