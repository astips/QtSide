# -*- coding: utf-8 -*-

import os
import types
from ..utils import load_module, seek_module


def load(path):
    """
    Loading some PySide sub-modules into the following module from the input path.
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

    # import shiboken
    shiboken_file = seek_module(path, 'shiboken', 'dynamic')
    if shiboken_file:
        load_module('shiboken', shiboken_file, 'dynamic')

    # import pysideuic
    pysideuic_package = seek_module(path, 'pysideuic', 'package')
    if pysideuic_package:
        load_module('pysideuic', pysideuic_package, 'package')

    # import PySide
    qt_dir = os.path.join(path, 'PySide')
    module = load_module('PySide', qt_dir, 'package')

    # import PySide sub-modules
    for sub_module in _dynamic_modules:
        setattr(
            module,
            sub_module,
            load_module(
                'PySide.{0}'.format(sub_module),
                seek_module(qt_dir, sub_module, 'dynamic'),
                'dynamic'
            )
        )

    # make QtWidgets module
    setattr(module, 'QtWidgets', getattr(module, 'QtGui'))

    # add custom _wrapper module
    setattr(module, 'ui_wrapper', types.ModuleType('ui_wrapper'))

    # add custom uic module
    setattr(module, 'uic', types.ModuleType('uic'))

    # fix
    module.QtCore.QStringListModel = module.QtGui.QStringListModel
    module.QtCore.QAbstractProxyModel = module.QtGui.QAbstractProxyModel
    module.QtCore.QSortFilterProxyModel = module.QtGui.QSortFilterProxyModel
    module.QtCore.QItemSelection = module.QtGui.QItemSelection
    module.QtCore.QItemSelectionModel = module.QtGui.QItemSelectionModel

    module.QtCore.pyqtProperty = module.QtCore.Property
    module.QtCore.pyqtSignal = module.QtCore.Signal
    module.QtCore.pyqtSlot = module.QtCore.Slot

    return module
