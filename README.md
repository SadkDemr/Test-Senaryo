C:\OtomasyoTool\backend\venv\Scripts\python.exe --version

  Eğer Python 3.11.9 çıkarsa sorun aktivasyonda. Şunu dene — deactivate edip CMD'de yeniden aktive et:

  deactivate
  C:\OtomasyoTool\backend\venv\Scripts\activate.bat
  python --version

  Hâlâ 3.14 çıkarsa venv'i tamamen silip yeniden oluştur, bu sefer PowerShell değil CMD'de:

  deactivate
  rmdir /s /q C:\OtomasyoTool\backend\venv
  py -3.11 -m venv C:\OtomasyoTool\backend\venv
  C:\OtomasyoTool\backend\venv\Scripts\activate.bat
  python --version

  Python 3.11.9 çıkınca paketleri kur:

  pip install -r C:\OtomasyoTool\backend\requirements.txt

  C:\OtomasyoTool\backend\venv\Scripts\python.exe --version çıktısını paylaş.
