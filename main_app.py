#!/usr/bin/env python3

# Filename: main_app.py

import sys
from PyQt5.QtWidgets import QApplication, QStyleFactory
# from model.model import Model
# from controllers.main_ctrl import MainController
from views.main_view import MainView

__version__ = "1.0"
__author__ = 'Ram Saavedra'

class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.main_view = MainView()
        self.main_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion')) # <- Choose the style
    sys.exit(app.exec_())
