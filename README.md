[DESKTOP] pytesseract kullanılamıyor — OCR devre dışı
[DESKTOP] pywinauto kullanılamıyor — pencere kontrolü devre dışı
Başlatılıyor: C:\Program Files (x86)\VK\Preprod\bin\BOA.UI.Container.exe
[CLICK] 'Gelen Kutusu' aranıyor...
[VISION] Hata: HTTPConnectionPool(host='localhost', port=11434): Max retries exceeded with url: /api/generate (Caused by NewConnectionError("HTTPConnection(host='localhost', port=11434): Failed to establish a new connection: [WinError 10061] Hedef makine etkin olarak reddettiğinden bağlantı kurulamadı"))
[FAIL] Element bulunamadı: 'Gelen Kutusu'
HATA: Element bulunamadı: 'Gelen Kutusu'
Traceback (most recent call last):
File "C:\Users\K240C~1.MD2\AppData\Local\Temp\ai_test_7_grjvy0.py", line 561, in <module>
_safe_click_desktop('Gelen Kutusu', _WINDOW_TITLE)
File "C:\Users\K240C~1.MD2\AppData\Local\Temp\ai_test_7_grjvy0.py", line 340, in _safe_click_desktop
raise Exception(f"Element bulunamadı: '{target}'")
Exception: Element bulunamadı: 'Gelen Kutusu'
data: Kosum hata ile bitti. (exit: 1)
