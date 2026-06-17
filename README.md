  Satır 1:
  $file = "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\base_wrapper.py"

  Satır 2:
  (Get-Content $file -Raw) -replace 'import win32ui except \(ImportError, OSError\): win32ui = None', "try:`n    import win32ui`nexcept (ImportError, OSError):`n    win32ui = None" | Set-Content $file
  -Encoding utf8

  Sonra test et:
  python -c "import pywinauto; print('OK')"
