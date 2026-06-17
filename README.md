(venv) C:\OtomasyoTool\backend>copy "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\pywintypes314.dll" "C:\OtomasyoTool\backend\venv\Scripts"
        1 file(s) copied.

(venv) C:\OtomasyoTool\backend>copy "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\pythoncom314.dll" "C:\OtomasyoTool\backend\venv\Scripts"
        1 file(s) copied.

(venv) C:\OtomasyoTool\backend> python -c "import pywinauto; print('OK')"
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

(venv) C:\OtomasyoTool\backend>dir "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywin32_system32"
 Volume in drive C has no label.
 Volume Serial Number is C6A7-0EE3

 Directory of C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywin32_system32

17/06/2026  11:46    <DIR>          .
17/06/2026  11:46    <DIR>          ..
17/06/2026  11:46           694,272 pythoncom314.dll
17/06/2026  11:46           136,704 pywintypes314.dll
               2 File(s)        830,976 bytes
               2 Dir(s)  40,871,321,600 bytes free

(venv) C:\OtomasyoTool\backend> python -c "import pywinauto; print('OK')"
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

(venv) C:\OtomasyoTool\backend>
