# -*- coding: utf-8 -*-

import os
import types
from ..utils import load_module, seek_module


def load(path):
    """
    Loading some PyQt4 sub-modules into the following module from the input path.
    This import function works with path argument rather than search from sys.path
    """
    _dynamic_modules = [
        'QtGui',
        'QtCore',
        'QtXml',
        'QtTest',
        'QtSvg',
        'QtNetwork',
        'QtSql'
    ]

    _package_modules = [
        'uic'
    ]

    # import sip
    sip_file = seek_module(path, 'sip', 'dynamic')
    if sip_file:
        # sip = load_module('sip', 'sip_file', 'dynamic')
        load_module('sip', sip_file, 'dynamic')

    # import pyqt4
    qt_dir = os.path.join(path, 'PyQt4')
    module = load_module('PyQt4', qt_dir, 'package')

    # import pyqt4 sub-modules
    for sub_module in _dynamic_modules:
        setattr(
            module,
            sub_module,
            load_module(
                'PyQt4.{0}'.format(sub_module),
                seek_module(qt_dir, sub_module, 'dynamic'),
                'dynamic'
            )
        )
    for sub_module in _package_modules:
        setattr(
            module,
            sub_module,
            load_module(
                'PyQt4.{0}'.format(sub_module),
                seek_module(qt_dir, sub_module, 'package'),
                'package'
            )
        )

    # make QtWidgets module
    setattr(module, 'QtWidgets', getattr(module, 'QtGui'))

    # add custom _wrapper module
    setattr(module, 'ui_wrapper', types.ModuleType('ui_wrapper'))

    # fix
    module.QtCore.QStringListModel = module.QtGui.QStringListModel
    module.QtCore.QAbstractProxyModel = module.QtGui.QAbstractProxyModel
    module.QtCore.QSortFilterProxyModel = module.QtGui.QSortFilterProxyModel
    module.QtCore.QItemSelection = module.QtGui.QItemSelection
    module.QtCore.QItemSelectionModel = module.QtGui.QItemSelectionModel

    return module
