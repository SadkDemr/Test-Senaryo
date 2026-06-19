(venv) C:\OtomasyoTool\backend>copy C:\OtomasyoTool\backend\venv\pywintypes311.dll "C:\Users\k.md200207\AppData\Local\Programs\Python\Python311\"
        1 file(s) copied.

(venv) C:\OtomasyoTool\backend>copy C:\OtomasyoTool\backend\venv\pythoncom311.dll "C:\Users\k.md200207\AppData\Local\Programs\Python\Python311\""
        1 file(s) copied.

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
