# Copyright (c) 2023 Amulya Paritosh
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import contextlib
import os
import re

from PyQt6.QtCore import Qt, pyqtSignal, QEvent
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QCompleter, QDialog, QHBoxLayout, QLineEdit

from .config import Config


class Completer(QCompleter):


	def __init__(self):
		with Config.HISTORY.open('rb') as file:
			history = set()
			for line in file:
				with contextlib.suppress(Exception):
					history.add(line.decode(Config.HISTORY_ENCODING).rsplit(';',1)[-1].strip())
		super().__init__(history)

		self.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
		self.setModelSorting(QCompleter.ModelSorting.CaseInsensitivelySortedModel)

	def event(self, event) -> None:
		if event.type() == QEvent.Type.KeyPress and event.key() == Qt.Key.Key_Tab:
			pass


class CommandLineEdit(QLineEdit):
	tabPressed = pyqtSignal()
	def __init__(self, parent) -> None:
		super().__init__(parent)

		self.tabPressed.connect(self.nextWordCompletion)

		font = QFont()
		font.setPointSize(12)
		self.setFont(font)

		with Config.HISTORY.open('rb') as file:
			history = set()
			for line in file:
				with contextlib.suppress(Exception):
					history.add(line.decode(Config.HISTORY_ENCODING).rsplit(';',1)[-1].strip())

		completer = Completer()
		self.setCompleter(completer)
		self.returnPressed.connect(self.onEnterKeyPressed)

	@staticmethod
	def executeCommand(command: str) -> None:
		os.system(command)
		print("executing:", command)

	def nextWordCompletion(self) -> None:
		curr_text: str = self.text()[:self.cursorPosition()]
		curr_words: list[str] = [word for word in re.split(Config.SPLIT_REX, curr_text) if word]

		top_txt: str = self.completer().currentCompletion()
		sugg_words: list[str] = [word for word in re.split(Config.SPLIT_REX, top_txt) if word]

		next_word: str = sugg_words[len(curr_words)-1]
		new_command: str = re.sub(f"{curr_words[-1]}$", next_word, curr_text)
		self.setText(new_command)


	def keyPressEvent(self, event) -> None:
		if event.key() == Qt.Key.Key_Tab:
			# self.nextWordCompletion()
			self.tabPressed.emit()
		else:
			super().keyPressEvent(event)

	def onEnterKeyPressed(self) -> None:
		if not self.text(): return
		self.executeCommand(self.text())
		self.parent().close()

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
