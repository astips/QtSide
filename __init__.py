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
__version__ = '1.0.2'

import logging
import sys
from .builder import setup

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

setup(sys.modules[__name__])
