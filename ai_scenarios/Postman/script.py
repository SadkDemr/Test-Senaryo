# -*- coding: utf-8 -*-
import pyautogui as _pag
import subprocess as _dsproc
import time

_AI_CONFIG_PATH = r"C:\Users\Sadik Demir\Documents\GitHub\OtomasyoToolFastApi\backend\ai_config.json"
_WINDOW_TITLE   = ""


import base64 as _ib64, tempfile as _itmp, os as _ios, time as _itime

def _find_b64_on_screen(b64_data, threshold=0.80, timeout=10):
    """Base64 görseli ekranda OpenCV ile ara. (x,y) veya None döner."""
    _tmp_path = _ios.path.join(_itmp.gettempdir(), f"_img_find_{id(b64_data)}.png")
    try:
        with open(_tmp_path, "wb") as _f:
            _f.write(_ib64.b64decode(b64_data))
        _start = _itime.time()
        while _itime.time() - _start < timeout:
            _elapsed = _itime.time() - _start
            _conf = max(0.65, threshold - (_elapsed / timeout) * 0.20)
            _coords = _find_image_on_screen(_tmp_path, threshold=_conf)
            if _coords:
                return _coords
            _itime.sleep(0.3)
        return None
    finally:
        try: _ios.unlink(_tmp_path)
        except Exception: pass

def _find_image_on_screen(target_path, threshold=0.80):
    """OpenCV multi-scale template matching. (x,y) veya None döner."""
    try:
        import cv2 as _cv2, numpy as _np
        from PIL import Image as _PILImg2
        _screen = _np.array(__import__("pyautogui").screenshot())
        _screen_bgr  = _cv2.cvtColor(_screen, _cv2.COLOR_RGB2BGR)
        _screen_gray = _cv2.cvtColor(_screen_bgr, _cv2.COLOR_BGR2GRAY)
        _screen_gray = _cv2.GaussianBlur(_screen_gray, (3,3), 0)
        _tmpl_bgr  = _cv2.imread(target_path)
        if _tmpl_bgr is None: return None
        _tmpl_gray = _cv2.cvtColor(_tmpl_bgr, _cv2.COLOR_BGR2GRAY)
        _tmpl_gray = _cv2.GaussianBlur(_tmpl_gray, (3,3), 0)
        _h, _w = _tmpl_gray.shape[:2]
        _best = None; _best_val = -1
        for _sc in _np.linspace(0.7, 1.3, 13):
            _rw, _rh = int(_w*_sc), int(_h*_sc)
            if _rw < 10 or _rh < 10: continue
            _res = _cv2.matchTemplate(_screen_gray, _cv2.resize(_tmpl_gray,(_rw,_rh)), _cv2.TM_CCOEFF_NORMED)
            _, _val, _, _loc = _cv2.minMaxLoc(_res)
            if _val > _best_val: _best_val = _val; _best = (_loc, _rw, _rh)
        if _best_val >= threshold and _best:
            _loc, _rw, _rh = _best
            return (_loc[0] + _rw//2, _loc[1] + _rh//2)
    except ImportError:
        try:
            import pyautogui as _pag2
            _loc2 = _pag2.locateOnScreen(target_path, grayscale=True, confidence=min(0.8, threshold))
            if _loc2: return (_pag2.center(_loc2).x, _pag2.center(_loc2).y)
        except Exception: pass
    except Exception: pass
    return None

def _do_robust_click(x, y, button="left"):
    import pyautogui as _pag3
    _pag3.moveTo(x, y, duration=0.2)
    _itime.sleep(0.3)
    _pag3.mouseDown(button=button)
    _itime.sleep(0.05)
    _pag3.mouseUp(button=button)

def _find_b64_on_screen_web(b64_data, threshold=0.80, timeout=10):
    """Web için: görseli ekranda (tarayıcı penceresinde) ara."""
    return _find_b64_on_screen(b64_data, threshold=threshold, timeout=timeout)


import pyautogui as _pag
import subprocess as _dsproc
import time, base64 as _b64, requests as _req, re as _re3, io as _io

_pag.FAILSAFE = True
_pag.PAUSE    = 0.25

# ── Opsiyonel bağımlılıklar ───────────────────────────────────────────────────
try:
    import pytesseract as _tess
    from PIL import Image as _PILImg
    _TESS_OK = True
except Exception:
    _TESS_OK = False
    print("[DESKTOP] pytesseract kullanılamıyor — OCR devre dışı")

try:
    from pywinauto import Application as _PwApp
    from pywinauto.findwindows import ElementNotFoundError as _PwNotFound
    _PW_OK = True
except Exception:
    _PW_OK = False
    print("[DESKTOP] pywinauto kullanılamıyor — pencere kontrolü devre dışı")


def _screenshot_b64():
    shot = _pag.screenshot()
    buf  = _io.BytesIO()
    shot.save(buf, format="PNG")
    return _b64.b64encode(buf.getvalue()).decode()


def _vision_find_desktop(search_text):
    """Gemini veya Ollama ile ekranda koordinat bul. (x, y) veya (None, None) döner."""
    try:
        shot_b64 = _screenshot_b64()
        try:
            import json as _js, pathlib as _pl
            cfg = {}
            _cp = _pl.Path(_AI_CONFIG_PATH) if "_AI_CONFIG_PATH" in dir() else None
            if _cp and _cp.exists():
                cfg = _js.loads(_cp.read_text(encoding="utf-8"))
            gemini_key = cfg.get("gemini_api_key", "")
        except Exception:
            gemini_key = ""

        _prompt = (f"Windows masaüstü ekranında '{search_text}' yazan veya "
                   f"gösteren tıklanabilir elementi bul. Yanıtı sadece: x=NNN y=NNN")

        if gemini_key:
            resp = _req.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}",
                json={"contents": [{"parts": [
                    {"text": _prompt},
                    {"inline_data": {"mime_type": "image/png", "data": shot_b64}}
                ]}]},
                timeout=15
            )
            answer = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            resp = _req.post("http://localhost:11434/api/generate", json={
                "model": "gemma3:4b", "prompt": _prompt,
                "images": [shot_b64], "stream": False
            }, timeout=60)
            answer = resp.json().get("response", "")

        mx = _re3.search(r"x[=:\s]*(\d+)", answer, _re3.IGNORECASE)
        my = _re3.search(r"y[=:\s]*(\d+)", answer, _re3.IGNORECASE)
        if mx and my:
            x, y = int(mx.group(1)), int(my.group(1))
            print(f"[VISION] Koordinat: ({x}, {y})")
            return x, y
        print(f"[VISION] Koordinat bulunamadı — yanıt: {answer[:80]}")
    except Exception as _ve:
        print(f"[VISION] Hata: {_ve}")
    return None, None


def _get_active_window():
    """Aktif pencereyi pywinauto ile döndür."""
    if not _PW_OK:
        return None
    try:
        import ctypes
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        return _PwApp(backend="uia").connect(handle=hwnd).top_window()
    except Exception:
        return None


def _safe_click_desktop(target, window_title=""):
    """
    Desktop tıklama — 4 strateji:
    1. pywinauto pencere içi element
    2. pytesseract OCR koordinatı
    3. pyautogui.locateOnScreen() görsel eşleşme
    4. Gemini / Ollama vision
    """
    print(f"[CLICK] '{target}' aranıyor...")

    # 1. pywinauto ─────────────────────────────────────────────────────────────
    if _PW_OK:
        try:
            if window_title:
                _win = _PwApp(backend="uia").connect(title_re=f".*{window_title}.*", timeout=3).top_window()
            else:
                _win = _get_active_window()

            if _win:
                for _ctrl in [
                    lambda: _win.child_window(title=target, found_index=0),
                    lambda: _win.child_window(title_re=f".*{target}.*", found_index=0),
                ]:
                    try:
                        _el = _ctrl()
                        if _el.exists(timeout=1):
                            _el.set_focus()
                            _el.click_input()
                            print(f"[OK] pywinauto: '{target}'")
                            return True
                    except Exception:
                        continue
        except Exception as _e:
            print(f"[CLICK] pywinauto başarısız: {_e}")

    # 2. OCR ──────────────────────────────────────────────────────────────────
    if _TESS_OK:
        try:
            shot = _pag.screenshot()
            data = _tess.image_to_data(shot, lang="tur+eng", output_type=_tess.Output.DICT)
            _tl  = target.lower()
            for _i, _w in enumerate(data["text"]):
                if _w and _tl in _w.lower() and data["conf"][_i] > 30:
                    _cx = data["left"][_i] + data["width"][_i]  // 2
                    _cy = data["top"][_i]  + data["height"][_i] // 2
                    _pag.click(_cx, _cy)
                    print(f"[OK] OCR: '{_w}' @ ({_cx},{_cy})")
                    return True
        except Exception as _e:
            print(f"[CLICK] OCR başarısız: {_e}")

    # 3. locateOnScreen (görsel dosya yoluysa) ──────────────────────────────────
    import os as _os2
    if _os2.path.isfile(target):
        try:
            loc = _pag.locateCenterOnScreen(target, confidence=0.8)
            if loc:
                _pag.click(loc)
                print(f"[OK] Görsel eşleşme: {target}")
                return True
        except Exception as _e:
            print(f"[CLICK] locateOnScreen başarısız: {_e}")

    # 4. Vision AI ─────────────────────────────────────────────────────────────
    print(f"[VISION] '{target}' için AI analiz...")
    _vx, _vy = _vision_find_desktop(target)
    if _vx and _vy:
        _pag.click(_vx, _vy)
        print(f"[OK] Vision: '{target}' @ ({_vx},{_vy})")
        return True

    raise Exception(f"Element bulunamadı: '{target}'")


def _safe_type_desktop(text):
    """Aktif alana metin yaz — clipboard ile (Türkçe karakter desteği), fallback pyautogui."""
    print(f"[TYPE] '{text}'")
    try:
        import pyperclip as _clip
        _clip.copy(str(text))
        _pag.hotkey("ctrl", "v")
        print(f"[OK] Clipboard paste: '{text}'")
    except Exception:
        _pag.write(str(text), interval=0.04)
    time.sleep(0.2)


def _safe_double_click_desktop(target, window_title=""):
    """Desktop çift tıklama — pywinauto → OCR → vision."""
    print(f"[DBLCLICK] '{target}' aranıyor...")

    if _PW_OK:
        try:
            if window_title:
                _win = _PwApp(backend="uia").connect(title_re=f".*{window_title}.*", timeout=3).top_window()
            else:
                _win = _get_active_window()
            if _win:
                for _ctrl in [
                    lambda: _win.child_window(title=target, found_index=0),
                    lambda: _win.child_window(title_re=f".*{target}.*", found_index=0),
                ]:
                    try:
                        _el = _ctrl()
                        if _el.exists(timeout=1):
                            _el.set_focus()
                            _el.double_click_input()
                            print(f"[OK] pywinauto çift tıkla: '{target}'")
                            return True
                    except Exception:
                        continue
        except Exception as _e:
            print(f"[DBLCLICK] pywinauto başarısız: {_e}")

    if _TESS_OK:
        try:
            shot = _pag.screenshot()
            data = _tess.image_to_data(shot, lang="tur+eng", output_type=_tess.Output.DICT)
            for _i, _w in enumerate(data["text"]):
                if _w and target.lower() in _w.lower() and data["conf"][_i] > 30:
                    _cx = data["left"][_i] + data["width"][_i] // 2
                    _cy = data["top"][_i]  + data["height"][_i] // 2
                    _pag.doubleClick(_cx, _cy)
                    print(f"[OK] OCR çift tıkla: '{_w}' @ ({_cx},{_cy})")
                    return True
        except Exception as _e:
            print(f"[DBLCLICK] OCR başarısız: {_e}")

    _vx, _vy = _vision_find_desktop(target)
    if _vx and _vy:
        _pag.doubleClick(_vx, _vy)
        print(f"[OK] Vision çift tıkla: '{target}' @ ({_vx},{_vy})")
        return True

    raise Exception(f"Element bulunamadı (çift tıkla): '{target}'")


def _safe_right_click_desktop(target, window_title=""):
    """Desktop sağ tıklama — pywinauto → OCR → vision."""
    print(f"[RCLICK] '{target}' aranıyor...")

    if _PW_OK:
        try:
            if window_title:
                _win = _PwApp(backend="uia").connect(title_re=f".*{window_title}.*", timeout=3).top_window()
            else:
                _win = _get_active_window()
            if _win:
                for _ctrl in [
                    lambda: _win.child_window(title=target, found_index=0),
                    lambda: _win.child_window(title_re=f".*{target}.*", found_index=0),
                ]:
                    try:
                        _el = _ctrl()
                        if _el.exists(timeout=1):
                            _el.set_focus()
                            _el.right_click_input()
                            print(f"[OK] pywinauto sağ tıkla: '{target}'")
                            return True
                    except Exception:
                        continue
        except Exception as _e:
            print(f"[RCLICK] pywinauto başarısız: {_e}")

    if _TESS_OK:
        try:
            shot = _pag.screenshot()
            data = _tess.image_to_data(shot, lang="tur+eng", output_type=_tess.Output.DICT)
            for _i, _w in enumerate(data["text"]):
                if _w and target.lower() in _w.lower() and data["conf"][_i] > 30:
                    _cx = data["left"][_i] + data["width"][_i] // 2
                    _cy = data["top"][_i]  + data["height"][_i] // 2
                    _pag.rightClick(_cx, _cy)
                    print(f"[OK] OCR sağ tıkla: '{_w}' @ ({_cx},{_cy})")
                    return True
        except Exception as _e:
            print(f"[RCLICK] OCR başarısız: {_e}")

    _vx, _vy = _vision_find_desktop(target)
    if _vx and _vy:
        _pag.rightClick(_vx, _vy)
        print(f"[OK] Vision sağ tıkla: '{target}' @ ({_vx},{_vy})")
        return True

    raise Exception(f"Element bulunamadı (sağ tıkla): '{target}'")


def _safe_menu_click_desktop(items, window_title=""):
    """Menü zinciri tıkla: ['Dosya', 'Yeni'] sırayla tıklar."""
    print(f"[MENU] {' > '.join(items)}")
    for _item in items:
        _safe_click_desktop(_item, window_title)
        time.sleep(0.4)
    print(f"[OK] Menü tamamlandı: {' > '.join(items)}")


def _safe_wait_for_desktop(target, timeout=10):
    """Element ekranda görünene kadar bekle (polling)."""
    import time as _tw
    print(f"[WAIT] '{target}' bekleniyor (max {timeout}s)...")
    _start = _tw.time()
    while _tw.time() - _start < timeout:
        if _PW_OK:
            try:
                _win = _get_active_window()
                if _win:
                    _el = _win.child_window(title_re=f".*{target}.*", found_index=0)
                    if _el.exists(timeout=1):
                        print(f"[OK] pywinauto görüldü: '{target}'")
                        return True
            except Exception:
                pass
        if _TESS_OK:
            try:
                _txt = _tess.image_to_string(_pag.screenshot(), lang="tur+eng")
                if target.lower() in _txt.lower():
                    print(f"[OK] OCR görüldü: '{target}'")
                    return True
            except Exception:
                pass
        _tw.sleep(1)
    print(f"[WARN] '{target}' {timeout}s içinde görünmedi")
    return False


def _safe_assert_desktop(target):
    """Ekranda element / metin doğrula."""
    print(f"[ASSERT] '{target}' kontrol ediliyor...")

    # pywinauto
    if _PW_OK:
        try:
            _win = _get_active_window()
            if _win:
                _el = _win.child_window(title_re=f".*{target}.*", found_index=0)
                if _el.exists(timeout=1):
                    print(f"[OK] pywinauto: '{target}'"); return
        except Exception:
            pass

    # OCR
    if _TESS_OK:
        try:
            shot = _pag.screenshot()
            _txt = _tess.image_to_string(shot, lang="tur+eng")
            if target.lower() in _txt.lower():
                print(f"[OK] OCR: '{target}'"); return
        except Exception:
            pass

    # Vision
    _vx, _vy = _vision_find_desktop(target)
    if _vx and _vy:
        print(f"[OK] Vision: '{target}'"); return

    print(f"[WARN] '{target}' ekranda bulunamadı — adım geçiliyor")


# ── Uygulama başlat ─────────────────────────────────────────
print("Başlatılıyor: C:\\Users\\Sadik Demir\\AppData\\Local\\Postman\\Postman.exe")
_app_proc = _dsproc.Popen([r"C:\Users\Sadik Demir\AppData\Local\Postman\Postman.exe"])
time.sleep(2)

try:
    print('STEP_START:0')
    # 3 saniye bekle
    time.sleep(3)
    print('STEP_DONE:0')

    print('STEP_START:1')
    # "Ctrl+T" bas
    _pag.hotkey('ctrl', 't')
    time.sleep(0.3)
    print('STEP_DONE:1')

    print('STEP_START:2')
    # 2 saniye bekle
    time.sleep(2)
    print('STEP_DONE:2')

    print('STEP_START:3')
    # "Enter URL or paste text" tıkla
    _pag.press("enter")
    time.sleep(0.3)
    print('STEP_DONE:3')

    print('STEP_START:4')
    # "https://jsonplaceholder.typicode.com/posts/1" yaz
    _safe_type_desktop('https://jsonplaceholder.typicode.com/posts/1')
    time.sleep(0.3)
    print('STEP_DONE:4')

    # [GÖRSEL TIKLAMA] Görsel element
    print('STEP_START:5')
    try:
        _img_b64_5 = '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'
        _coords_5 = _find_b64_on_screen(_img_b64_5, timeout=10)
        if not _coords_5: raise Exception('Gorsel bulunamadi: Görsel element')
        _do_robust_click(_coords_5[0], _coords_5[1])
        print('[OK] Gorsel tiklandi: Görsel element')
        time.sleep(0.5)
        print('STEP_DONE:5')
    except Exception as _e_5:
        print(f'[FAIL] {_e_5}')
        print('STEP_FAIL:5')
        raise

    print('STEP_START:6')
    # 4 saniye bekle
    time.sleep(4)
    print('STEP_DONE:6')

except Exception as e:
    print(f"HATA: {e}")
    raise