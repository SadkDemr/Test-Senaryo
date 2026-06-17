(venv) C:\OtomasyoTool\backend>C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\python.exe C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Scripts\pywin32_postinstall.py -install
Parsed arguments are: Namespace(install=True, remove=False, wait=None, silent=False, quiet=False, destination='C:\\Users\\kftte\\AppData\\Local\\Python\\pythoncore-3.14-64\\Lib\\site-packages')
Copied pythoncom314.dll to C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\pythoncom314.dll
Copied pywintypes314.dll to C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\pywintypes314.dll
You do not have the permissions to install COM objects.
The sample COM objects were not registered.
-> Software\Python\PythonCore\3.14\Help[None]=None
-> Software\Python\PythonCore\3.14\Help\Pythonwin Reference[None]='C:\\Users\\kftte\\AppData\\Local\\Python\\pythoncore-3.14-64\\Lib\\site-packages\\PyWin32.chm'
Registered help file
Pythonwin has been registered in context menu
Creating directory C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\win32com\gen_py
Can't install shortcuts - 'C:\\Users\\kftte\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Python 3.14' is not a folder
The pywin32 extensions were successfully installed.

(venv) C:\OtomasyoTool\backend>python -c "import pywinauto; print('OK')"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import pywinauto; print('OK')
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
