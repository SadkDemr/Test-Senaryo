 Dosya farklı makinede. Şu Python scriptini çalıştır — dosyayı otomatik düzeltir:

  python -c "
  path = r'C:\OtomasyoTool\backend\venv\Lib\site-packages\pywinauto\base_wrapper.py'
  with open(path, 'r', encoding='utf-8') as f:
      content = f.read()
  old = 'import win32ui'
  new = 'try:\n    import win32ui\nexcept (ImportError, OSError):\n    win32ui = None'
  content = content.replace(old, new, 1)
  with open(path, 'w', encoding='utf-8') as f:
      f.write(content)
  print('Duzeltildi')
  "

  Sonra test et:

  python -c "import pywinauto; print('OK')"


  echo path = r"C:\OtomasyoTool\backend\venv\Lib\site-packages\pywinauto\base_wrapper.py" > fix.py
  echo f = open(path, "r", encoding="utf-8") >> fix.py
  echo content = f.read() >> fix.py
  echo f.close() >> fix.py
  echo content = content.replace("import win32ui", "try:\n    import win32ui\nexcept (ImportError, OSError):\n    win32ui = None", 1) >> fix.py
  echo f = open(path, "w", encoding="utf-8") >> fix.py
  echo f.write(content) >> fix.py
  echo f.close() >> fix.py
  echo print("Duzeltildi") >> fix.py
  python fix.py
