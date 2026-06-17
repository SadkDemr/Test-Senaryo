  Remove-Item fix.py -ErrorAction SilentlyContinue; Add-Content fix.py 'path = r"C:\OtomasyoTool\backend\venv\Lib\site-packages\pywinauto\base_wrapper.py"'; Add-Content fix.py 'with open(path, "r", encoding="utf-8") as f:'; Add-Content fix.py 'lines = f.readlines()'; Add-Content fix.py 'new_lines = []'; Add-Content fix.py 'for line in lines:'; Add-Content fix.py '    if line.strip() == "import win32ui":'; Add-Content fix.py 'new_lines += ["try:\n", "    import win32ui\n", "except (ImportError, OSError):\n", "win32ui = None\n"]'; Add-Content fix.py ' else:'; Add-Content fix.py ' new_lines.append(line)'; Add-Content fix.py 'with open(path, "w", encoding="utf-8") as f:'; Add-Content fix.py ' f.writelines(new_lines)'; Add-Content fix.py 'print("Duzeltildi")'; python fix.py

  python -c "import pywinauto; print('OK')"

  PS C:\OtomasyoTool> Remove-Item fix.py -ErrorAction SilentlyContinue; Add-Content fix.py 'path = r"C:\OtomasyoTool\backend\venv\Lib\site-packages\pywinauto\base_wrapper.py"'; Add-Content fix.py 'with open(path, "r", encoding="utf-8") as f:'; Add-Content fix.py 'lines = f.readlines()'; Add-Content fix.py 'new_lines = []'; Add-Content fix.py 'for line in lines:'; Add-Content fix.py '    if line.strip() == "import win32ui":'; Add-Content fix.py 'new_lines += ["try:\n", "    import win32ui\n", "except (ImportError, OSError):\n", "win32ui = None\n"]'; Add-Content fix.py ' else:'; Add-Content fix.py ' new_lines.append(line)'; Add-Content fix.py 'with open(path, "w", encoding="utf-8") as f:'; Add-Content fix.py ' f.writelines(new_lines)'; Add-Content fix.py 'print("Duzeltildi")'; python fix.py
  File "C:\OtomasyoTool\fix.py", line 3
    lines = f.readlines()
    ^
IndentationError: expected an indented block after 'with' statement on line 2
