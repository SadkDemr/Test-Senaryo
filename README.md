(venv) C:\OtomasyoTool\backend>$file = "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\base_wrapper.py" (Get-Content $file -Raw) -replace 'import win32ui except (ImportError, OSError): win32ui = None', "try:n    import win32uinexcept (ImportError, OSError):`n win32ui = None" | Set-Content $file -Encoding utf8
'$file' is not recognized as an internal or external command,
operable program or batch file.
