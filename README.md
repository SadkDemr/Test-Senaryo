  Sonra PowerShell'de şunu çalıştır:
  $file = "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\site-packages\pywinauto\base_wrapper.py"
  (Get-Content $file -Raw) -replace 'import win32ui except \(ImportError, OSError\): win32ui = None', "try:`n    import win32ui`nexcept (ImportError, OSError):`n    win32ui = None" | Set-Content $file
  -Encoding utf8

  ---
  2. Python Sürümünü Değiştirmek (Önerilen)

  Adım 1 — Python 3.11 indir ve kur

  https://www.python.org/downloads/release/python-3119/ — Windows installer (64-bit) seç.
  Kurulum sırasında "Add Python to PATH" kutusunu işaretle.

  Adım 2 — Eski venv'i sil

  rmdir /s /q C:\OtomasyoTool\backend\venv

  Adım 3 — Yeni venv oluştur (Python 3.11 ile)

  py -3.11 -m venv C:\OtomasyoTool\backend\venv

  Adım 4 — Venv'i aktif et ve paketleri kur

  C:\OtomasyoTool\backend\venv\Scripts\activate
  pip install -r C:\OtomasyoTool\backend\requirements.txt

  Adım 5 — Test et

  python -c "import pywinauto; print('OK')"

  ---
  Python 3.14 çok yeni, pywinauto/pywin32 gibi kütüphaneler henüz desteklemiyor. Python 3.11 en stabil seçenek.
