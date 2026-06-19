  venv\Scripts\pip.exe install pywin32
  venv\Scripts\python.exe venv\Scripts\pywin32_postinstall.py -install

  Sonra tekrar test et:
  venv\Scripts\python.exe -c "from pywinauto import Application; print('OK')"
