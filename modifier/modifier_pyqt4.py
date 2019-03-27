# -*- coding: utf-8 -*-

from . import QtModifier
from PyQt4 import QtGui


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


@qt_modifier.register('QtCore.QString.__str__')
def to_string(self):
    return str(self.toUtf8)


@qt_modifier.register("QtWidgets.QColorDialog.set_custom_color")
def set_custom_color(self, index, color):
    QtGui.QColorDialog.setCustomColor(index, color.rgb())
