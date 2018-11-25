# QtSide
Wrap PyQt4 PyQt5 PySide PySide2 together.

### INSTALLATION
1. Download the latest release and unzip to a folder with the name '**QtSide**' where you want to live.
2. Add parent folder to the **_PYTHONPATH_** env var.

### HOW DOES IT WORK
QtSide replaces itself with whatever Python binding is available (or preferred) in the Python environment your script runs in. 
However, QtSide will first take care of remappings of calls so that the Qt5 style syntax of PySide2 will work even if you run 
this code in an environment with a Python binding for Qt4.

#### Environment variables.
* **_QT_SIDE_BINDING_**
* **_QT_SIDE_PYQT4_DIR_**
* **_QT_SIDE_PYQT5_DIR_**
* **_QT_SIDE_PYSIDE_DIR_**
* **_QT_SIDE_PYSIDE2_DIR_**

Before open your custom apps or vfx-dccs, you need to set these environment variable first.
- You need tell QtSide which binding to prefer by setting the **_QT_SIDE_BINDING_** environment variable.
- You need tell QtSide prefer-binding's folder locations by setting the **_QT_SIDE\_\*\_DIR_** environment variable.

#### For example:
```
Maya 2016 with PyQt4
- linux:
    export QT_SIDE_BINDING=pyqt4
    export QT_SIDE_PYQT4_DIR=/mnt/mount/lib/pyqt4_parent_folder  # ignore this if PyQt4 package already exists in PYTHONPATH/sys.path
- windows:
    set QT_SIDE_BINDING=pyqt4
    set QT_SIDE_PYQT4_DIR=c:/mount/lib/pyqt4_parent_folder  # ignore this if PyQt4 package already exists in PYTHONPATH/sys.path

Maya 2016 with PySide
- linux:
    export QT_SIDE_BINDING=pyside
- windows:
    set QT_SIDE_BINDING=pyside

Maya 2017 with PyQt5
- linux:
    export QT_SIDE_BINDING=pyqt5
    export QT_SIDE_PYQT5_DIR=/mnt/mount/lib/pyqt5_parent_folder  # ignore this if PyQt5 package already setted into PYTHONPATH or sys.path
- windows:
    set QT_SIDE_BINDING=pyqt5
    set QT_SIDE_PYQT5_DIR=c:/mount/lib/pyqt5_parent_folder  # ignore this if PyQt5 package already setted into PYTHONPATH or sys.path

Maya 2017 with PySide2
- linux:
    export QT_SIDE_BINDING=pyside2
- windows:
    set QT_SIDE_BINDING=pyside2
```  
### USAGE
For those of you new to Qt5 (and PySide2 or PyQt5), all widget classes of QtGui were moved into its own module called QtWidgets. 
I had to say this is one of the largest backwards compatibility breaking changes you will have to deal with 
when changing existing scripts to use QtSide.

```python
import sys
from QtSide import QtWidgets, QtGui, QtCore
app = QtWidgets.QApplication(sys.argv)
button = QtWidgets.QPushButton('Hello World')
font = QtGui.QFont()
font.setPointSize(11)
font.setBold(True)
button.setFont(font)
button.setMinimumSize(QtCore.QSize(0, 22))
button.setMaximumSize(QtCore.QSize(168, 22))
button.show()
app.exec_()
```

```python
# VFX DCC - Maya
from QtSide import QtWidgets, ui_wrapper
import maya.OpenMayaUI as OpenMayaUI
connector = ui_wrapper.wrapinstance(
    long(OpenMayaUI.MQtUtil.mainWindow()),
    QtWidgets.QMainWindow
)
```
