# -*- coding: utf-8 -*-

"""
UiLoader & loadUi functions are both from github.com/bpabel/pysideuic

loadUiType function is from github.com/jerch/pyside-uicfix
"""
import os
import sys
import inspect
import hashlib

from . import QtModifier
from PySide2 import QtCore, QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QIODevice


qt_modifier = QtModifier()


@qt_modifier.register('ui_wrapper.wrapinstance')
def wrapinstance(*args, **kwargs):
    try:
        import shiboken2
    except Exception as e:
        raise ImportError('This method can not be executed without shiboken2 module.\n{0}'.format(e))
    return shiboken2.wrapInstance(*args, **kwargs)


@qt_modifier.register('ui_wrapper.unwrapinstance')
def unwrapinstance(*args, **kwargs):
    try:
        import shiboken2
    except Exception as e:
        raise ImportError('This method can not be executed without shiboken2 module.\n{0}'.format(e))
    return shiboken2.getCppPointer(*args, **kwargs)[0]


@qt_modifier.register('QtCore.QEvent.__init__')
def event_init(self, event):
    QtCore.QEvent.__init__(self, QtCore.QEvent.Type(event))


@qt_modifier.register('QtWidgets.QTreeWidgetItem.setBackgroundColor')
def setBackgroundColor(self, p_int, QColor):
    QtWidgets.QTreeWidgetItem.setBackground(self, p_int, QColor)


@qt_modifier.register('QtWidgets.QTreeWidgetItem.setTextColor')
def setTextColor(self, p_int, QColor):
    QtWidgets.QTreeWidgetItem.setForeground(self, p_int, QColor)


@qt_modifier.register("QtWidgets.QTreeWidget.setItemHidden")
def setItemHidden(self, QTreeWidgetItem, bool):
    QTreeWidgetItem.setHidden(bool)


@qt_modifier.register("QtWidgets.QHeaderView.setClickable")
def setClickable(self, bool):
    QtWidgets.QHeaderView.setSectionsClickable(self, bool)


@qt_modifier.register("QtWidgets.QHeaderView.setResizeMode")
def setResizeMode(self, mode):
    QtWidgets.QHeaderView.setSectionResizeMode(self, mode)


original_set_focus_policy = QtWidgets.QWidget.setFocusPolicy


@qt_modifier.register('QtWidgets.QWidget.setFocusPolicy')
def setFocusPolicy(self, focus_policy):
    original_set_focus_policy(self, QtCore.Qt.FocusPolicy(focus_policy))


class UiLoader(QUiLoader):
    """
    Subclass :class:`~PySide.QtUiTools.QUiLoader` to create the user interface
    in a base instance.

    Unlike :class:`~PySide.QtUiTools.QUiLoader` itself this class does not
    create a new instance of the top-level widget, but creates the user
    interface in an existing instance of the top-level class.

    This mimics the behaviour of :func:`PyQt4.uic.loadUi`.
    """

    def __init__(self, baseinstance):
        """
        Create a loader for the given "baseinstance".

        The user interface is created in "baseinstance", which must be an
        instance of the top-level class in the user interface to load, or a
        subclass thereof.

        "parent" is the parent object of this loader.
        """
        QUiLoader.__init__(self, baseinstance)
        self.baseinstance = baseinstance

    def createWidget(self, class_name, parent=None, name=''):
        if parent is None and self.baseinstance:
            # supposed to create the top-level widget, return the base instance
            # instead
            return self.baseinstance
        else:
            # create a new widget for child widgets
            widget = QUiLoader.createWidget(self, class_name, parent, name)
            if self.baseinstance:
                # set an attribute for the new child widget on the base
                # instance, just like PyQt4.uic.loadUi does.
                setattr(self.baseinstance, name, widget)
            return widget


@qt_modifier.register('uic.loadUi')
def loadUi(uifile, baseinstance=None):
    """
    Dynamically load a user interface from the given "uifile".

    "uifile" is a string containing a file name of the UI file to load.

    If "baseinstance" is "None", the a new instance of the top-level widget
    will be created.  Otherwise, the user interface is created within the given
    "baseinstance".  In this case "baseinstance" must be an instance of the
    top-level widget class in the UI file to load, or a subclass thereof.  In
    other words, if you've created a "QMainWindow" interface in the designer,
    "baseinstance" must be a "QMainWindow" or a subclass thereof, too.  You
    cannot load a "QMainWindow" UI file with a plain
    :class:`~PySide.QtGui.QWidget` as "baseinstance".

    :method:`~PySide.QtCore.QMetaObject.connectSlotsByName()` is called on the
    created user interface, so you can implemented your slots according to its
    conventions in your widget class.

    Return "baseinstance", if "baseinstance" is not "None".  Otherwise
    return the newly created instance of the user interface.
    """
    loader = UiLoader(baseinstance)
    if not os.path.isfile(uifile) and baseinstance is not None:
        fp = inspect.getfile(baseinstance)
        uifile = os.path.join(os.path.dirname(fp), uifile)
        if not os.path.isfile(uifile):
            uifile = os.path.join(os.path.dirname(fp), 'ui', uifile)

    widget = loader.load(uifile)
    QtCore.QMetaObject.connectSlotsByName(widget)
    return widget


_cls_cache = {}


@qt_modifier.register('uic.loadUiType')
def loadUiType(uifile):
    """
    Load form and base classes from ui file.
    """

    try:
        from pyside2uic.Compiler.compiler import UICompiler
    except ImportError:
        raise RuntimeError("This method isn't executable without pyside2uic module.")

    try:
        from cStringIO import StringIO
    except ImportError:
        from io import StringIO
        unicode_ = str
    else:
        # We cannot use the name `unicode` here as it a buitin function and
        # when we assign it a value, for example, unicode = str, then python
        # interpreter will see this as a variable `unicode` rather than the
        # python built-in type `unicode`. This throws an `UnboundLocalError`
        # exception. To fix this, we use a new variable name `unicode_` (as
        # suggested by PEP8, add a trailing '_' after a python keyword, if you
        # absolutely need it). The variable `unicode_` can now be assigned any
        # values, and it will not overwrite the built-type `unicode`
        unicode_ = unicode

    key = ''

    # python and Qt file like objects
    if hasattr(uifile, 'read'):
        if isinstance(uifile, QIODevice):
            # always copy Qt objects' content over to StringIO
            if not (uifile.openMode() & QIODevice.ReadOnly):
                raise IOError('file %s not open for reading' % uifile)
            io_in = StringIO()
            data = uifile.readAll().data()
            if sys.version_info >= (3, 0):
                data = str(data, encoding='utf-8')
            io_in.write(data)

            # use QFile's fileName as key
            if hasattr(uifile, 'fileName') and uifile.fileName():
                key = os.path.abspath(uifile.fileName())
        else:
            # normal python file object and StringIO objects
            if hasattr(uifile, 'name') and uifile.name:
                key = os.path.abspath(uifile.name)
            io_in = uifile

        # if we got no key so far, build key from content hash
        if not key:
            io_in.seek(0)
            data = io_in.read()
            if sys.version_info >= (3, 0):
                data = bytes(data, 'utf-8')
            key = hashlib.sha1(data).hexdigest()
        io_in.seek(0)

    elif isinstance(uifile, (str, bytes, unicode_)):
        io_in = os.path.abspath(uifile)
        key = io_in
    else:
        raise TypeError('wrong type for uifile')

    # lookup requested ui file in cache first
    classes = _cls_cache.get(key)
    if classes:
        return classes

    # compile ui file to python code
    io_out = StringIO()
    winfo = UICompiler().compileUi(io_in, io_out, False)

    # compile python code and extract form class
    pyc = compile(io_out.getvalue(), '<string>', 'exec')
    frame = {}
    exec (pyc, frame)
    form_class = frame[winfo['uiclass']]

    # lookup base class in global QtGui module
    base_class = getattr(QtWidgets, winfo['baseclass'])

    # save classes in cache
    _cls_cache[key] = (form_class, base_class)
    return form_class, base_class
