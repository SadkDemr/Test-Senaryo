  try:
      import win32ui
  except (ImportError, OSError):
      win32ui = None
