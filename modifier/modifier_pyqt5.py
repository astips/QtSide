# -*- coding: utf-8 -*-

from . import QtModifier
from PyQt5 import QtWidgets, QtGui


qt_modifier = QtModifier()


@qt_modifier.register('ui_wrapper.wrapinstance')
def wrapinstance(*args, **kwargs):
    try:
        import sip
    except Exception as e:
        raise ImportError('This method can not be executed without sip module.\n{0}'.format(e))
    return sip.wrapinstance(*args, **kwargs)


@qt_modifier.register('ui_wrapper.unwrapinstance')
def unwrapinstance(*args, **kwargs):
    try:
        import sip
    except Exception as e:
        raise ImportError('This method can not be executed without sip module.\n{0}'.format(e))
    return sip.unwrapinstance(*args, **kwargs)


@qt_modifier.register('QtWidgets.QTreeWidgetItem.setBackgroundColor')
def setBackgroundColor(self, p_int, QColor):
    QtWidgets.QTreeWidgetItem.setBackgroundColor(self, p_int, QColor)


@qt_modifier.register('QtWidgets.QTreeWidgetItem.setTextColor')
def setTextColor(self, p_int, QColor):
    QtWidgets.QTreeWidgetItem.setForeground(self, p_int, QColor)


@qt_modifier.register('QtWidgets.QTableWidgetItem.setBackgroundColor')
def setBackgroundColor(self, QColor):
    QtWidgets.QTableWidgetItem.setBackgroundColor(self, QColor)


@qt_modifier.register("QtWidgets.QTableWidgetItem.setTextColor")
def setTextColor(self, QColor):
    QtWidgets.QTableWidgetItem.setForeground(self, QColor)


@qt_modifier.register("QtWidgets.QTreeWidget.setItemHidden")
def setItemHidden(self, QTreeWidgetItem, bool):
    QTreeWidgetItem.setHidden(bool)


@qt_modifier.register("QtGui.QWheelEvent.delta")
def delta(self):
    return QtGui.QWheelEvent.angleDelta(self).y()


@qt_modifier.register("QtGui.QDrag.start")
def start(self, supportedActions=None):
    QtGui.QDrag.exec_(self, supportedActions)
