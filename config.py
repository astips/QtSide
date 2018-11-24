# -*- coding: utf-8 -*-

import os


QT_SIDE_PREFERRED_BINDING = os.environ.get('QT_SIDE_BINDING')
if not QT_SIDE_PREFERRED_BINDING:
    QT_SIDE_PREFERRED_BINDING = 'pyqt4'
QT_SIDE_PREFERRED_BINDING = QT_SIDE_PREFERRED_BINDING.lower()
if QT_SIDE_PREFERRED_BINDING not in ('pyqt4', 'pyqt5', 'pyside', 'pyside2'):
    raise EnvironmentError('Invalid QT_SIDE_BINDING env: {0}'.format(QT_SIDE_PREFERRED_BINDING))

QT_SIDE_PYQT4_DIR = os.getenv('QT_SIDE_PYQT4_DIR')
QT_SIDE_PYQT5_DIR = os.getenv('QT_SIDE_PYQT5_DIR')
QT_SIDE_PYSIDE_DIR = os.getenv('QT_SIDE_PYSIDE_DIR')
QT_SIDE_PYSIDE2_DIR = os.getenv('QT_SIDE_PYSIDE2_DIR')
