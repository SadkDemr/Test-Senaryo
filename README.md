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


(venv) C:\OtomasyoTool>python -c " path = r'C:\OtomasyoTool\backend\venv\Lib\site-packages\pywinauto\base_wrapper.py' with open(path, 'r', encoding='utf-8') as f: content = f.read() old = 'import win32ui' new = 'try:\n import win32ui\nexcept (ImportError, OSError):\n win32ui = None' content = content.replace(old, new, 1) with open(path, 'w', encoding='utf-8') as f: f.write(content) print('Duzeltildi') "
  File "<string>", line 1
    path = r'C:\OtomasyoTool\backend\venv\Lib\site-packages\pywinauto\base_wrapper.py' with open(path, 'r', encoding='utf-8') as f: content = f.read() old = 'import win32ui' new = 'try:\n import win32ui\nexcept (ImportError, OSError):\n win32ui = None' content = content.replace(old, new, 1) with open(path, 'w', encoding='utf-8') as f: f.write(content) print('Duzeltildi')
IndentationError: unexpected indent
