# -*- coding: utf-8 -*-

"""
Usage:
    >> import sys
    >> from QtSide import QtWidgets
    >> app = QtWidgets.QApplication(sys.argv)
    >> button = QtWidgets.QPushButton('Hello World')
    >> button.show()
    >> app.exec_()
"""

__package__ = 'QtSide'
__version__ = '1.0.0'

import sys
from .builder import setup


setup(sys.modules[__name__])
