PS C:\OtomasyoTool> $file = "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\base_wrapper.py"
PS C:\OtomasyoTool> (Get-Content $file -Raw) -replace 'import win32ui except (ImportError, OSError): win32ui = None', "try:n    import win32uinexcept (ImportError, OSError):`n win32ui = None" | Set-Content $file -Encoding utf8
PS C:\OtomasyoTool> python -c "import pywinauto; print('OK')"
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
  File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\base_wrapper.py", line 46
    except (ImportError, OSError):
                                  ^
IndentationError: unindent does not match any outer indentation level
