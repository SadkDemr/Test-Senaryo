  copy "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\pywintypes314.dll" "C:\OtomasyoTool\backend\venv\Scripts\"
  
  copy "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\pythoncom314.dll" "C:\OtomasyoTool\backend\venv\Scripts\"


  Sonra tekrar test et:
  python -c "import pywinauto; print('OK')"

  

  Çalışmazsa ek olarak win32ui.pyd'nin bağımlılıklarını da kontrol edelim:

  
  dir "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywin32_system32"
