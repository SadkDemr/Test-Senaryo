(venv) C:\OtomasyoTool\backend>python -c "import pywinauto; print('OK')"
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import pywinauto; print('OK')
    ^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'pywinauto'

(venv) C:\OtomasyoTool\backend>pip install pinwinauto comtyes --prefer-binary --timeout 120
ERROR: Could not find a version that satisfies the requirement pinwinauto (from versions: none)
ERROR: No matching distribution found for pinwinauto

(venv) C:\OtomasyoTool\backend>pip install pywinauto comtyes --prefer-binary --timeout 120
Collecting pywinauto
  Downloading pywinauto-0.6.9-py2.py3-none-any.whl.metadata (2.0 kB)
ERROR: Could not find a version that satisfies the requirement comtyes (from versions: none)
ERROR: No matching distribution found for comtyes

(venv) C:\OtomasyoTool\backend>pip install pywinauto comtyes --prefer-binary --timeout 120
Collecting pywinauto
  Using cached pywinauto-0.6.9-py2.py3-none-any.whl.metadata (2.0 kB)
ERROR: Could not find a version that satisfies the requirement comtyes (from versions: none)
ERROR: No matching distribution found for comtyes
