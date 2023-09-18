import sys

from PyQt6.QtWidgets import QApplication

from widget import OneLineTerminal

app = QApplication([])
terminal = OneLineTerminal("/home/encryptedbee")
sys.exit(app.exec())
