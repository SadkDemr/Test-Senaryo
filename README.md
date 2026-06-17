
  Önce pythonwin'deki DLL'leri arama yoluna ekleyerek dene:

  python -c "import os; os.add_dll_directory(r'C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pythonwin'); import pywinauto; print('OK')"

  ---
  Bu da çalışmazsa (MFC DLL'leri orada yoksa) en güvenilir çözüm: base_wrapper.py patch'i. Biz sadece UIA backend kullanıyoruz, win32ui win32 backend için gerekli.

  Şu dosyayı aç ve 44. satırı düzenle:
  
  notepad "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\base_wrapper.py"

  Mevcut (satır 44):
  import win32ui

  Değiştir:
  try:
      import win32ui
  except (ImportError, OSError):
      win32ui = None

  Kaydedip test et:
  python -c "import pywinauto; print('OK')"

  Önce os.add_dll_directory denemesinin sonucunu at.
