(venv) C:\OtomasyoTool>pip install pywinauto pywin32
Collecting pywinauto
  Using cached pywinauto-0.6.9-py2.py3-none-any.whl.metadata (2.0 kB)
Collecting pywin32
  Downloading pywin32-312-cp311-cp311-win_amd64.whl.metadata (11 kB)
Requirement already satisfied: six in c:\otomasyotool\backend\venv\lib\site-packages (from pywinauto) (1.17.0)
Collecting comtypes (from pywinauto)
  Using cached comtypes-1.4.16-py3-none-any.whl.metadata (7.8 kB)
Using cached pywinauto-0.6.9-py2.py3-none-any.whl (363 kB)
Downloading pywin32-312-cp311-cp311-win_amd64.whl (6.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.9/6.9 MB 364.7 kB/s eta 0:00:00
Using cached comtypes-1.4.16-py3-none-any.whl (296 kB)
Installing collected packages: pywin32, comtypes, pywinauto
Successfully installed comtypes-1.4.16 pywin32-312 pywinauto-0.6.9

[notice] A new release of pip is available: 24.0 -> 26.1.2
[notice] To update, run: python.exe -m pip install --upgrade pip

(venv) C:\OtomasyoTool>python -c "import pywin32; print('OK')"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'pywin32'

(venv) C:\OtomasyoTool>python -c "import pywinauto; print('OK')"
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

(venv) C:\OtomasyoTool>python -c "import pywinauto; print('OK')"
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
