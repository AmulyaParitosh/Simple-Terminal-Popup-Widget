import contextlib

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLineEdit, QCompleter


class OneLineTerminal(QLineEdit):
	def __init__(self) -> None:
		super().__init__()
		self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
		self.resize(400,20)

		with open('/home/encryptedbee/.zsh_history', 'rb') as file:
			history = set()
			for line in file:
				with contextlib.suppress(Exception):
					history.add(line.decode('utf-8').rsplit(';',1)[-1].strip())

		completer = QCompleter(history)
		self.setCompleter(completer)
		self.returnPressed.connect(self.onEnterKeyPressed)
		self.show()

	def keyPressEvent(self, event) -> None:
		if event.key() == Qt.Key.Key_Escape:
			self.close()
		else:
			super().keyPressEvent(event)

	def onEnterKeyPressed(self):
		if not self.text(): return
		print(self.text())
		self.clear()
