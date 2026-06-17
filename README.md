  powershell

  PowerShell açılınca:

  $fix = @'
  path = r"C:\OtomasyoTool\backend\venv\Lib\site-packages\pywinauto\base_wrapper.py"
  with open(path, "r", encoding="utf-8") as f:
      lines = f.readlines()
  new_lines = []
  for line in lines:
      if line.strip() == "import win32ui":
          new_lines += ["try:\n", "    import win32ui\n", "except (ImportError, OSError):\n", "    win32ui = None\n"]
      else:
          new_lines.append(line)
  with open(path, "w", encoding="utf-8") as f:
      f.writelines(new_lines)
  print("Duzeltildi")
  '@
  $fix | Out-File -FilePath fix.py -Encoding utf8
  python fix.py

  Sonra test et:

  python -c "import pywinauto; print('OK')"
