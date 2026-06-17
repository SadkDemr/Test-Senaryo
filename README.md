  pip install pywin32 pywinauto pyautogui pyperclip --prefer-binary --force-reinstall

  --force-reinstall olmadan pip "zaten var" deyip sistem Python'undaki paketi görüyor, venv'e kurmuyor.

  Kurulduktan sonra test et:
  python -c "import pywinauto; import pyautogui; import pyperclip; print('OK')"
