 PS C:\OtomasyoTool> $fix = @' path = r"C:\OtomasyoTool\backend\venv\Lib\site-packages\pywinauto\base_wrapper.py" with open(path, "r", encoding="utf-8") as f: lines = f.readlines() new_lines = [] for line in lines: if line.strip() == "import win32ui": new_lines += ["try:\n", " import win32ui\n", "except (ImportError, OSError):\n", " win32ui = None\n"] else: new_lines.append(line) with open(path, "w", encoding="utf-8") as f: f.writelines(new_lines) print("Duzeltildi") '@ $fix | Out-File -FilePath fix.py -Encoding utf8 python fix.py
At line:1 char:11
+ $fix = @' path = r"C:\OtomasyoTool\backend\venv\Lib\site-packages\pyw ...
+           ~
No characters are allowed after a here-string header but before the end of the line.
At line:1 char:455
+ ... 8") as f: f.writelines(new_lines) print("Duzeltildi") '@ $fix | Out-F ...
+                                                              ~~~~
Unexpected token '$fix' in expression or statement.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
    + FullyQualifiedErrorId : UnexpectedCharactersAfterHereStringHeader

  Sonra test et:

  python -c "import pywinauto; print('OK')"
