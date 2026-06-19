● win32ui.pyd kendi dizininde DLL arıyor. Oraya kopyala:

  copy C:\OtomasyoTool\backend\venv\pywintypes311.dll C:\OtomasyoTool\backend\venv\Lib\site-packages\win32\
  copy C:\OtomasyoTool\backend\venv\pythoncom311.dll C:\OtomasyoTool\backend\venv\Lib\site-packages\win32\

  Sonra tekrar:
  python.exe -c "from pywinauto import Application; print('OK')"
