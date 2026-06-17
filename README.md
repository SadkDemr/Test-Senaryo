  Adım 1 — Python 3.11 İndir

  Tarayıcıdan şu adreste "Windows installer (64-bit)" indir:
  https://www.python.org/downloads/release/python-3119/
  Kurulumda "Add Python to PATH" kutusunu işaretle, "Install Now" de.

  ---
  Adım 2 — Kurulumu Doğrula

  py -3.11 --version
  Python 3.11.9 çıkmalı.

  ---
  Adım 3 — Eski venv'i Sil ve Yenisini Kur

  Remove-Item -Recurse -Force C:\OtomasyoTool\backend\venv
  py -3.11 -m venv C:\OtomasyoTool\backend\venv

  ---
  Adım 4 — Venv Aktif Et ve Paketleri Kur

  C:\OtomasyoTool\backend\venv\Scripts\activate
  pip install -r C:\OtomasyoTool\backend\requirements.txt

  ---
  Adım 5 — Test Et

  python -c "import pywinauto; print('OK')"
  python -c "import pywin32; print('OK')"

  ---
  Adım 1'i tamamlayınca diğerlerine geçelim. Hangi adımda takıldıysan söyle.
