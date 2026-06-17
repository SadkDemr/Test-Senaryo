  python -c "p=r'C:\OtomasyoTool\backend\venv\Lib\site-packages\pywinauto\base_wrapper.py';lines=open(p,encoding='utf-8').readlines();i=next(n for n,l in enumerate(lines) if l.strip()=='import
  win32ui');lines[i:i+1]=['try:\n','    import win32ui\n','except (ImportError, OSError):\n','    win32ui = None\n'];open(p,'w',encoding='utf-8').writelines(lines);print('Duzeltildi')"

  Sonra test et:

  python -c "import pywinauto; print('OK')"
