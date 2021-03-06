# -*- coding: utf-8 -*-

import types


class QtModifier(object):
    """
    Easily register custom function to QtSide package.
    """
    def __init__(self):
        self.changes = dict()

    def register(self, full_name):
        def receiver(function):
            self.changes[full_name] = function
            return function
        return receiver

    def modify(self, root_module):
        assert isinstance(root_module, types.ModuleType)
        root_name = root_module.__name__

        for full_name, function in self.changes.items():
            module = root_module
            current_name = root_name
            name_list = full_name.split('.')
            for name in name_list[:-1]:
                module = getattr(module, name, None)
                if not module:
                    raise AttributeError('{0} do not have attribute {1}'.format(current_name, name))
                current_name = '.'.join([current_name, name])
            setattr(module, name_list[-1], function)


def qt_modifier(binding='pyqt4'):
    binding = binding.lower()
    if binding == 'pyqt4':
        from .modifier_pyqt4 import qt_modifier
    elif binding == 'pyqt5':
        from .modifier_pyqt5 import qt_modifier
    elif binding == 'pyside':
        from .modifier_pyside import qt_modifier
    elif binding == 'pyside2':
        from .modifier_pyside2 import qt_modifier
    else:
        raise Exception('Invalid binding: {0}'.format(binding))
    return qt_modifier
