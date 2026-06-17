(venv) C:\OtomasyoTool\backend>python -c "import ctypes; ctypes.WinDLL(r'C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\win32\win32ui.pyd')"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import ctypes; ctypes.WinDLL(r'C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\win32\win32ui.pyd')
                   ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\ctypes\__init__.py", line 433, in __init__
    self._handle = self._load_library(name, mode, handle, winmode)
                   ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\ctypes\__init__.py", line 451, in _load_library
    return _LoadLibrary(self._name, winmode)
FileNotFoundError: Could not find module 'C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\win32\win32ui.pyd' (or one of its dependencies). Try using the full path with constructor syntax.

(venv) C:\OtomasyoTool\backend>dir "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\win32\win32ui*"
 Volume in drive C has no label.
 Volume Serial Number is C6A7-0EE3

 Directory of C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\win32

File Not Found

(venv) C:\OtomasyoTool\backend>python -c "import os; os.add_dll_directory(r'C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64'); os.add_dll_directory(r'C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywin32_system32'); import pywinauto; print('OK')"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import os; os.add_dll_directory(r'C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64'); os.add_dll_directory(r'C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywin32_system32'); import pywinauto; print('OK')

                                                                                            ^^^^^^^^^^^^^^^^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\__init__.py", line 89, in <module>
    from . import findwindows
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\findwindows.py", line 42, in <module>
    from . import controls
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\controls\__init__.py", line 36, in <module>
    from . import uiawrapper # register "uia" back-end (at the end of uiawrapper module)
    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\controls\uiawrapper.py", line
 42, in <module>
    from .. import backend
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\backend.py", line 35, in <module>
    from .base_wrapper import BaseWrapper
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\base_wrapper.py", line 44, in
 <module>
    import win32ui
ImportError: DLL load failed while importing win32ui: Belirtilen modül bulunamadı.

(venv) C:\OtomasyoTool\backend>
