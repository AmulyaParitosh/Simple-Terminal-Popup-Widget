#!/home/encryptedbee/programfiles/anaconda3/bin/python

# Copyright (c) 2023 Amulya Paritosh
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import sys

from PyQt6.QtWidgets import QApplication

from src import OneLineTerminal

app = QApplication([])
terminal = OneLineTerminal()
sys.exit(app.exec())
