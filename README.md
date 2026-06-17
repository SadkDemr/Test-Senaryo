[DESKTOP] pytesseract kullanılamıyor — OCR devre dışı
[DESKTOP] pywinauto kullanılamıyor — pencere kontrolü devre dışı
Başlatılıyor: C:\Users\kftte\OneDrive\Desktop\bin\BOA.UI.Container.exe k.ah200209
Traceback (most recent call last):
File "C:\Users\kftte\AppData\Local\Temp\ai_test_1mnq2qic.py", line 464, in <module>
_dsproc.Popen([r"C:\Users\kftte\OneDrive\Desktop\bin\BOA.UI.Container.exe k.ah200209"])
~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\subprocess.py", line 1039, in __init__
self._execute_child(args, executable, preexec_fn, close_fds,
~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
pass_fds, cwd, env,
^^^^^^^^^^^^^^^^^^^
...<5 lines>...
gid, gids, uid, umask,
^^^^^^^^^^^^^^^^^^^^^^
start_new_session, process_group)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\kftte\AppData\Local\Python\pythoncore-3.14-64\Lib\subprocess.py", line 1553, in _execute_child
hp, ht, pid, tid = _winapi.CreateProcess(executable, args,
~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^
# no special security
^^^^^^^^^^^^^^^^^^^^^
...<4 lines>...
cwd,
^^^^
startupinfo)
^^^^^^^^^^^^
FileNotFoundError: [WinError 2] Sistem belirtilen dosyayı bulamıyor
data: Kosum hata ile bitti. (exit: 1)
