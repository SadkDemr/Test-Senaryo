
(venv) C:\OtomasyoTool\backend>pip.exe install pywin32
Requirement already satisfied: pywin32 in c:\otomasyotool\backend\venv\lib\site-packages (312)

[notice] A new release of pip is available: 24.0 -> 26.1.2
[notice] To update, run: python.exe -m pip install --upgrade pip

(venv) C:\OtomasyoTool\backend>pywin32_postinstall.py -install
Parsed arguments are: Namespace(install=True, remove=False, wait=None, silent=False, quiet=False, destination='C:\\OtomasyoTool\\backend\\venv\\Lib\\site-packages')
Copied pythoncom311.dll to C:\OtomasyoTool\backend\venv\pythoncom311.dll
Copied pywintypes311.dll to C:\OtomasyoTool\backend\venv\pywintypes311.dll
You do not have the permissions to install COM objects.
The sample COM objects were not registered.
-> Software\Python\PythonCore\3.11\Help[None]=None
-> Software\Python\PythonCore\3.11\Help\Pythonwin Reference[None]='C:\\OtomasyoTool\\backend\\venv\\Lib\\site-packages\\PyWin32.chm'
Registered help file
Pythonwin has been registered in context menu
Creating directory C:\OtomasyoTool\backend\venv\Lib\site-packages\win32com\gen_py
Shortcut for Pythonwin created
Shortcut to documentation created
The pywin32 extensions were successfully installed.

(venv) C:\OtomasyoTool\backend>python.exe -c "from pywinauto import Application; print('OK')"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\pywinauto\__init__.py", line 89, in <module>
    from . import findwindows
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\pywinauto\findwindows.py", line 42, in <module>
    from . import controls
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\pywinauto\controls\__init__.py", line 36, in <module>
    from . import uiawrapper # register "uia" back-end (at the end of uiawrapper module)
    ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\pywinauto\controls\uiawrapper.py", line 42, in <module>
    from .. import backend
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\pywinauto\backend.py", line 35, in <module>
    from .base_wrapper import BaseWrapper
  File "C:\OtomasyoTool\backend\venv\Lib\site-packages\pywinauto\base_wrapper.py", line 44, in <module>
    import win32ui
ImportError: DLL load failed while importing win32ui: Belirtilen modül bulunamadı.
