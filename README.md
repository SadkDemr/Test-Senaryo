Sunucuda Python'u yeniden yüklemen gerekiyor. Adımlar:

  1. Python 3.11 indir ve kur

  Tarayıcıdan: https://www.python.org/downloads/release/python-3119/

  Windows installer (64-bit) dosyasını indir.

  Kurulum sırasında mutlaka şunu işaretle:
  - ✅ Add Python to PATH
  - ✅ Install for all users (tüm Windows kullanıcıları görsün)

  2. Kurulum sonrası kontrol et:
  python --version
  Python 3.11.x çıkması lazım.

  3. Eski venv'i sil ve yeniden oluştur:
  cd C:\OtomasyoTool\backend
  rmdir /s /q venv
  setup.bat

  4. Sonra çalıştır:
  run.bat

  ---
  "Install for all users" seçmezsen yeni kullanıcı (k.md200207) Python'u görmeyebilir — bunu atlamaman önemli.
