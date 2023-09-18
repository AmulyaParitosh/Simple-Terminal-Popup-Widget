# Copyright (c) 2023 Amulya Paritosh
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import contextlib
import os
import re

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QCompleter, QDialog, QHBoxLayout, QLineEdit

from .config import Config


class CommandLineEdit(QLineEdit):
	def __init__(self, parent) -> None:
		super().__init__(parent)

		self.execute = False

		font = QFont()
		font.setPointSize(12)
		self.setFont(font)

		with Config.HISTORY.open('rb') as file:
			history = set()
			for line in file:
				with contextlib.suppress(Exception):
					history.add(line.decode(Config.HISTORY_ENCODING).rsplit(';',1)[-1].strip())

		completer = QCompleter(history)
		self.setCompleter(completer)
		self.returnPressed.connect(self.onEnterKeyPressed)

	@staticmethod
	def executeCommand(command: str) -> None:
		os.system(command)

	def autoComplete(self) -> None:
		curr_words: list[str] = [word for word in re.split(Config.SPLIT_REX, self.text()) if word]

		top_txt: str = self.completer().currentCompletion()
		sugg_words: list[str] = [word for word in re.split(Config.SPLIT_REX, top_txt) if word]

		next_word: str = sugg_words[len(curr_words)-1]
		new_command: str = re.sub(f"{curr_words[-1]}$", next_word, self.text())
		self.setText(new_command)


	def keyPressEvent(self, event) -> None:
		if event.key() == Qt.Key.Key_Tab:
			self.autoComplete()
		else:
			super().keyPressEvent(event)

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
	def __init__(self) -> None:
		super().__init__()
		os.chdir(Config.PWD)

		self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
		self.resize(400,20)

		self.setLayout(QHBoxLayout())

		command_line = CommandLineEdit(self)
		self.layout().addWidget(command_line)
		self.show()

	def keyPressEvent(self, event) -> None:
		if event.key() == Qt.Key.Key_Escape:
			self.close()
		else:
			super().keyPressEvent(event)
