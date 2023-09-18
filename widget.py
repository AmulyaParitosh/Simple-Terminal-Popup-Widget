import contextlib
import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCompleter, QDialog, QHBoxLayout, QLineEdit
from PyQt6.QtGui import QFont

class CommandLineEdit(QLineEdit):
	def __init__(self) -> None:
		super().__init__()

		self.execute = False

		font = QFont()
		font.setPointSize(12)
		self.setFont(font)

		with open('/home/encryptedbee/.zsh_history', 'rb') as file:
			history = set()
			for line in file:
				with contextlib.suppress(Exception):
					history.add(line.decode('utf-8').rsplit(';',1)[-1].strip())

		completer = QCompleter(history)
		self.setCompleter(completer)
		self.returnPressed.connect(self.onEnterKeyPressed)

	@staticmethod
	def executeCommand(command: str) -> None:
		print("executing:", command)
		os.system(command)

	def onEnterKeyPressed(self) -> None:
		if not self.text(): return

		if self.execute:
			self.executeCommand(self.text())
			self.execute = False
			self.parent().close()
		else:
			self.execute = True

		self.clear()

class OneLineTerminal(QDialog):
	def __init__(self, pwd: str) -> None:
		super().__init__()
		os.chdir(pwd)

		self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
		self.resize(400,20)

		self.setLayout(QHBoxLayout())

		command_line = CommandLineEdit()
		self.layout().addWidget(command_line)
		self.show()

	def keyPressEvent(self, event) -> None:
		if event.key() == Qt.Key.Key_Escape:
			self.close()
		else:
			super().keyPressEvent(event)
