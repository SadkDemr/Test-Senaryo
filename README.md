(venv) C:\OtomasyoTool>python C:\OtomasyoTool\backend\venv\Scripts\pywin32_postinstall.py -install
Parsed arguments are: Namespace(install=True, remove=False, wait=None, silent=False, quiet=False, destination='C:\\OtomasyoTool\\backend\\venv\\Lib\\site-packages')
Copied pythoncom311.dll to C:\OtomasyoTool\backend\venv\pythoncom311.dll
Copied pywintypes311.dll to C:\OtomasyoTool\backend\venv\pywintypes311.dll
You do not have the permissions to install COM objects.
The sample COM objects were not registered.
-> Software\Python\PythonCore\3.11\Help[None]=None
-> Software\Python\PythonCore\3.11\Help\Pythonwin Reference[None]='C:\\OtomasyoTool\\backend\\venv\\Lib\\site-packages\\PyWin32.chm'
Registered help file
Pythonwin has been registered in context menu
Creating directory C:\OtomasyoTool\backend\venv\Lib\site-packages\win32com\gen_py
Shortcut for Pythonwin created
Shortcut to documentation created
The pywin32 extensions were successfully installed.

(venv) C:\OtomasyoTool>python -c "import win32api; print('OK')" python -c "import pywinauto; print('OK')"
OK
