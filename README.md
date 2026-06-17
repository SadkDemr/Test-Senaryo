Windows Firewall engelliyorsa şu komutla 8000 portunu aç:
  netsh advfirewall firewall add rule name="OtomasyoTool" dir=in action=allow protocol=TCP localport=8000
