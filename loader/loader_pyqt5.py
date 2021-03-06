# -*- coding: utf-8 -*-

import os
import types
from ..utils import load_module, seek_module


def load(path):
    """
    Loading some PyQt5 sub-modules into the following module from the input path.
    This import function works with path argument rather than search from sys.path
    """
    _dynamic_modules = [
        'QtGui',
        'QtWidgets',
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
        load_module('sip', sip_file, 'dynamic')

    # import pyqt5
    qt_dir = os.path.join(path, 'PyQt5')
    module = load_module('PyQt5', qt_dir, 'package')

    # import pyqt5 sub-modules
    for sub_module in _dynamic_modules:
        setattr(
            module,
            sub_module,
            load_module(
                'PyQt5.{0}'.format(sub_module),
                seek_module(qt_dir, sub_module, 'dynamic'),
                'dynamic'
            )
        )
    for sub_module in _package_modules:
        setattr(
            module,
            sub_module,
            load_module(
                'PyQt5.{0}'.format(sub_module),
                seek_module(qt_dir, sub_module, 'package'),
                'package'
            )
        )

    # add custom _wrapper module
    setattr(module, 'ui_wrapper', types.ModuleType('ui_wrapper'))

    return module
