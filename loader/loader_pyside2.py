# -*- coding: utf-8 -*-

import os
import types
from ..utils import load_module, seek_module


def load(path):
    """
    Loading some PySide2 sub-modules into the following module from the input path.
    This import function works with path argument rather than search from sys.path
    """
    _dynamic_modules = [
        'QtGui',
        'QtCore',
        'QtXml',
        'QtTest',
        'QtSvg',
        'QtNetwork',
        'QtSql',
        'QtUiTools'
    ]

    # import shiboken2
    shiboken2_file = seek_module(path, 'shiboken2', 'dynamic')
    if shiboken2_file:
        load_module('shiboken2', shiboken2_file, 'dynamic')

    # import pyside2uic
    pyside2uic_package = seek_module(path, 'pyside2uic', 'package')
    if pyside2uic_package:
        load_module('pyside2uic', pyside2uic_package, 'package')

    # import PySide2
    qt_dir = os.path.join(path, 'PySide2')
    module = load_module('PySide2', qt_dir, 'package')

    # import PySide2 sub-modules
    for sub_module in _dynamic_modules:
        setattr(
            module,
            sub_module,
            load_module(
                'PySide2.{0}'.format(sub_module),
                seek_module(qt_dir, sub_module, 'dynamic'),
                'dynamic'
            )
        )

    # add custom _wrapper module
    setattr(module, 'ui_wrapper', types.ModuleType('ui_wrapper'))

    # add custom uic module
    setattr(module, 'uic', types.ModuleType('uic'))

    # fix
    module.QtCore.QStringListModel = module.QtGui.QStringListModel
    # module.QtCore.QAbstractProxyModel = module.QtGui.QAbstractProxyModel
    # module.QtCore.QSortFilterProxyModel = module.QtGui.QSortFilterProxyModel
    # module.QtCore.QItemSelection = module.QtGui.QItemSelection
    # module.QtCore.QItemSelectionModel = module.QtGui.QItemSelectionModel

    module.QtCore.pyqtProperty = module.QtCore.Property
    module.QtCore.pyqtSignal = module.QtCore.Signal
    module.QtCore.pyqtSlot = module.QtCore.Slot

    return module
