from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
import sys

def launch_gui():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("JARVIS AI Assistant")
    window.setGeometry(100, 100, 600, 400)
    window.setStyleSheet("background-color: #222244;")
    label = QLabel("JARVIS ONLINE\nListening...", window)
    label.setAlignment(Qt.AlignCenter)
    label.setStyleSheet("color: #55FFFF; font-size: 26px; font-family: Consolas;")
    window.setCentralWidget(label)
    window.show()
    app.exec_()
