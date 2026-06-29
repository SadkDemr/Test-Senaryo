# -*- coding: utf-8 -*-
import pyautogui as _pag
import subprocess as _dsproc
import sys
import time

_AI_CONFIG_PATH = r"C:\Users\Sadik Demir\Documents\GitHub\OtomasyoToolFastApi\backend\ai_config.json"
_WINDOW_TITLE   = ""
_VARS = {}  # adımlar arası değişken havuzu

import os as _os_s, sys as _sys_s
_STOP_FILE = _os_s.environ.get("_AI_STOP_FILE", "")
def _check_stop():
    if _STOP_FILE and _os_s.path.exists(_STOP_FILE):
        try: _os_s.unlink(_STOP_FILE)
        except: pass
        raise SystemExit(0)


import base64 as _ib64, tempfile as _itmp, os as _ios, time as _itime

def _get_window_region():
    """_WINDOW_TITLE penceresinin ekran bölgesini (x,y,w,h) döndürür. Bulamazsa None."""
    try:
        _wt = _WINDOW_TITLE  # generated script globals'ta tanımlı
    except NameError:
        return None
    if not _wt:
        return None
    # pywinauto ile pencere dikdörtgeni al
    try:
        import pywinauto as _pwr
        _app = _pwr.Application(backend="uia").connect(title_re=f".*{_wt}.*", timeout=2)
        _rect = _app.top_window().rectangle()
        _x, _y = max(0, _rect.left), max(0, _rect.top)
        _w, _h = _rect.width(), _rect.height()
        if _w > 10 and _h > 10:
            return (_x, _y, _w, _h)
    except Exception:
        pass
    # win32gui fallback
    try:
        import win32gui as _wg
        def _cb(h, acc):
            if _wt.lower() in _wg.GetWindowText(h).lower():
                acc.append(h)
        _hs = []; _wg.EnumWindows(_cb, _hs)
        if _hs:
            _x1,_y1,_x2,_y2 = _wg.GetWindowRect(_hs[0])
            _w, _h = _x2-_x1, _y2-_y1
            if _w > 10 and _h > 10:
                return (max(0,_x1), max(0,_y1), _w, _h)
    except Exception:
        pass
    return None

def _find_b64_on_screen(b64_data, threshold=0.80, timeout=10):
    """Base64 gorsel arar — _WINDOW_TITLE varsa yalnizca o pencere icinde."""
    _tmp_path = _ios.path.join(_itmp.gettempdir(), f"_img_find_{id(b64_data)}.png")
    try:
        with open(_tmp_path, "wb") as _f:
            _f.write(_ib64.b64decode(b64_data))
        # Pencere bolgesi — _WINDOW_TITLE varsa tam ekran aramaz
        _region = _get_window_region()
        if _WINDOW_TITLE and _region is None:
            _wt_end = _itime.time() + 3
            while _itime.time() < _wt_end:
                _itime.sleep(0.3)
                _region = _get_window_region()
                if _region: break
            if _region is None:
                print(f"[HATA] '{_WINDOW_TITLE}' penceresi bulunamadi — gorsel aranamaz.")
                return None
        _start = _itime.time()
        while _itime.time() - _start < timeout:
            if _WINDOW_TITLE:
                _upd = _get_window_region()
                if _upd: _region = _upd
            _elapsed = _itime.time() - _start
            _conf = max(0.50, threshold - (_elapsed / timeout) * 0.30)
            _coords = _find_image_on_screen(_tmp_path, threshold=_conf, region=_region)
            if _coords:
                return _coords
            _itime.sleep(0.3)
        print(f"[DEBUG] Gorsel {timeout}s icinde bulunamadi. Farkli bir bolgeyi kroplayip tekrar deneyin.")
        return None
    finally:
        try: _ios.unlink(_tmp_path)
        except Exception: pass

def _find_image_on_screen(target_path, threshold=0.80, region=None):
    """OpenCV multi-scale template matching. region=(x,y,w,h) ile kısıtlı arama yapar."""
    try:
        import cv2 as _cv2, numpy as _np
        import pyautogui as _pag_sc
        # Windows DPI ölçeğini tespit et — template farklı DPI'da alınmış olabilir
        _dpi_scale = 1.0
        try:
            import ctypes as _ct
            _dpi_scale = _ct.windll.user32.GetDpiForSystem() / 96.0
        except Exception:
            pass
        _screenshot = _pag_sc.screenshot(region=region) if region else _pag_sc.screenshot()
        _screen      = _np.array(_screenshot)
        _ox, _oy     = (region[0], region[1]) if region else (0, 0)
        _screen_bgr  = _cv2.cvtColor(_screen, _cv2.COLOR_RGB2BGR)
        _screen_gray = _cv2.cvtColor(_screen_bgr, _cv2.COLOR_BGR2GRAY)
        _screen_gray = _cv2.GaussianBlur(_screen_gray, (3,3), 0)
        _tmpl_bgr  = _cv2.imread(target_path)
        if _tmpl_bgr is None: return None
        _tmpl_gray = _cv2.cvtColor(_tmpl_bgr, _cv2.COLOR_BGR2GRAY)
        _tmpl_gray = _cv2.GaussianBlur(_tmpl_gray, (3,3), 0)
        _h, _w = _tmpl_gray.shape[:2]
        _best = None; _best_val = -1
        # DPI farklılıklarını (125%/150%/200%) karşılamak için geniş scale aralığı
        # Merkez: 1/dpi_scale (fiziksel px template → mantıksal px ekran)
        _center = 1.0 / _dpi_scale
        _lo = max(0.3, _center * 0.6)
        _hi = min(2.5, _center * 1.7)
        for _sc in _np.linspace(_lo, _hi, 25):
            _rw, _rh = int(_w*_sc), int(_h*_sc)
            if _rw < 8 or _rh < 8: continue
            if _rw > _screen_gray.shape[1] or _rh > _screen_gray.shape[0]: continue
            _res = _cv2.matchTemplate(_screen_gray, _cv2.resize(_tmpl_gray,(_rw,_rh)), _cv2.TM_CCOEFF_NORMED)
            _, _val, _, _loc = _cv2.minMaxLoc(_res)
            if _val > _best_val: _best_val = _val; _best = (_loc, _rw, _rh)
        if _best_val >= threshold and _best:
            _loc, _rw, _rh = _best
            return (_loc[0] + _rw//2 + _ox, _loc[1] + _rh//2 + _oy)
    except ImportError:
        try:
            import pyautogui as _pag2
            _loc2 = _pag2.locateOnScreen(target_path, grayscale=True,
                                          confidence=min(0.8, threshold), region=region)
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
    """Web için: görseli ekranda ara (pencere kısıtlaması olmadan)."""
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


def _ollama_url():
    try:
        import json as _js2, pathlib as _pl2
        _cp2 = _pl2.Path(_AI_CONFIG_PATH) if "_AI_CONFIG_PATH" in globals() else None
        if _cp2 and _cp2.exists():
            return _js2.loads(_cp2.read_text(encoding="utf-8")).get("ollama_url", "http://localhost:11434/api/generate")
    except Exception:
        pass
    return "http://localhost:11434/api/generate"

def _ollama_model():
    try:
        import json as _js2, pathlib as _pl2
        _cp2 = _pl2.Path(_AI_CONFIG_PATH) if "_AI_CONFIG_PATH" in globals() else None
        if _cp2 and _cp2.exists():
            return _js2.loads(_cp2.read_text(encoding="utf-8")).get("ollama_model", "gemma3:4b")
    except Exception:
        pass
    return "gemma3:4b"


def _screenshot_b64(region=None):
    """Ekran (veya belirtilen bölge) fotoğrafı → base64 PNG."""
    shot = _pag.screenshot(region=region) if region else _pag.screenshot()
    buf  = _io.BytesIO()
    shot.save(buf, format="PNG")
    return _b64.b64encode(buf.getvalue()).decode()


def _vision_find_desktop(search_text):
    """Gemini veya Ollama ile pencere icinde koordinat bul. (x, y) veya (None, None) doner.
    _WINDOW_TITLE varsa yalnizca o pencerenin kroplamasini AI'ye gonderir; donus koordinatlari
    pencere orijinine gore offsetlenir — pencere disina tiklamaz."""
    try:
        _region = _get_window_region()  # (wx, wy, ww, wh) veya None
        _wx, _wy = (_region[0], _region[1]) if _region else (0, 0)
        shot_b64 = _screenshot_b64(region=_region)  # sadece pencere alanini cek

        try:
            import json as _js, pathlib as _pl
            cfg = {}
            _cp = _pl.Path(_AI_CONFIG_PATH) if "_AI_CONFIG_PATH" in dir() else None
            if _cp and _cp.exists():
                cfg = _js.loads(_cp.read_text(encoding="utf-8"))
            gemini_key = cfg.get("gemini_api_key", "")
        except Exception:
            gemini_key = ""

        _prompt = (f"Bu ekran goruntusunde '{search_text}' yazan veya gosteren "
                   f"tiklanabilir elementi bul. Yaniti sadece: x=NNN y=NNN "
                   f"(koordinatlar bu goruntunun sol ust kosesindendir)")

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
            resp = _req.post(_ollama_url(), json={
                "model": _ollama_model(), "prompt": _prompt,
                "images": [shot_b64], "stream": False
            }, timeout=60)
            answer = resp.json().get("response", "")

        mx = _re3.search(r"x[=:\s]*(\d+)", answer, _re3.IGNORECASE)
        my = _re3.search(r"y[=:\s]*(\d+)", answer, _re3.IGNORECASE)
        if mx and my:
            # Krop koordinatlarindan ekran koordinatina donustur
            x, y = int(mx.group(1)) + _wx, int(my.group(1)) + _wy
            print(f"[VISION] Koordinat (pencere ofseti {_wx},{_wy}): ({x}, {y})")
            return x, y
        print(f"[VISION] Koordinat bulunamadi — yanit: {answer[:80]}")
    except Exception as _ve:
        print(f"[VISION] Hata: {_ve}")
    return None, None


def _in_window(x, y):
    """Koordinatlar pencere siniri icinde mi? _WINDOW_TITLE yoksa her zaman True."""
    _r = _get_window_region()
    if not _r:
        return True
    _wx, _wy, _ww, _wh = _r
    return _wx <= x <= _wx + _ww and _wy <= y <= _wy + _wh


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
    1. pywinauto uia backend
    2. pywinauto win32 backend (Java/Delphi/özel UI için)
    3. pytesseract OCR (kuruluysa)
    4. Vision AI / locateOnScreen
    """
    print(f"[CLICK] '{target}' aranıyor...")

    def _pw_try(backend):
        try:
            if window_title:
                _win = _PwApp(backend=backend).connect(title_re=f".*{window_title}.*", timeout=3).top_window()
            else:
                _win = _get_active_window()
            if not _win:
                return False
            for _ctrl in [
                lambda: _win.child_window(title=target, found_index=0),
                lambda: _win.child_window(title_re=f".*{target}.*", found_index=0),
            ]:
                try:
                    _el = _ctrl()
                    if _el.exists(timeout=1):
                        _el.set_focus()
                        _el.click_input()
                        print(f"[OK] pywinauto({backend}): '{target}'")
                        return True
                except Exception:
                    continue
        except Exception as _e:
            print(f"[CLICK] pywinauto({backend}) başarısız: {_e}")
        return False

    # 1. pywinauto uia ─────────────────────────────────────────────────────────
    if _PW_OK and _pw_try("uia"):
        return True

    # 2. pywinauto win32 ───────────────────────────────────────────────────────
    if _PW_OK and _pw_try("win32"):
        return True

    # 3. pytesseract OCR — yalnizca pencere bolgesi ───────────────────────────
    if _TESS_OK:
        try:
            _ocr_region = _get_window_region()
            _ocr_ox, _ocr_oy = (_ocr_region[0], _ocr_region[1]) if _ocr_region else (0, 0)
            shot = _pag.screenshot(region=_ocr_region) if _ocr_region else _pag.screenshot()
            data = _tess.image_to_data(shot, lang="tur+eng", output_type=_tess.Output.DICT)
            _tl  = target.lower()
            for _i, _w in enumerate(data["text"]):
                if _w and _tl in _w.lower() and data["conf"][_i] > 30:
                    _cx = data["left"][_i] + data["width"][_i] // 2 + _ocr_ox
                    _cy = data["top"][_i]  + data["height"][_i] // 2 + _ocr_oy
                    if _in_window(_cx, _cy):
                        _pag.click(_cx, _cy)
                        print(f"[OK] OCR: '{_w}' @ ({_cx},{_cy})")
                        return True
        except Exception as _e:
            print(f"[CLICK] OCR basarisiz: {_e}")

    # 4. locateOnScreen / Vision AI — pencere ile sinirli ────────────────────
    import os as _os2
    if _os2.path.isfile(target):
        try:
            _ls_region = _get_window_region()
            loc = _pag.locateCenterOnScreen(target, confidence=0.8, region=_ls_region)
            if loc and _in_window(loc.x, loc.y):
                _pag.click(loc)
                print(f"[OK] locateOnScreen: {target}")
                return True
        except Exception: pass

    _vx, _vy = _vision_find_desktop(target)
    if _vx and _vy and _in_window(_vx, _vy):
        _pag.click(_vx, _vy)
        print(f"[OK] Vision AI: '{target}' @ ({_vx},{_vy})")
        return True
    elif _vx and _vy:
        print(f"[HATA] Vision AI koordinati ({_vx},{_vy}) pencere disinda — tiklanmadi.")

    raise Exception(f"Element bulunamadi: '{target}'")


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
    """Desktop çift tıklama — uia → win32 → OCR → vision."""
    print(f"[DBLCLICK] '{target}' aranıyor...")

    def _pw_dbl(backend):
        try:
            _win = _PwApp(backend=backend).connect(title_re=f".*{window_title}.*", timeout=3).top_window() if window_title else _get_active_window()
            if not _win: return False
            for _ctrl in [lambda: _win.child_window(title=target, found_index=0), lambda: _win.child_window(title_re=f".*{target}.*", found_index=0)]:
                try:
                    _el = _ctrl()
                    if _el.exists(timeout=1):
                        _el.set_focus(); _el.double_click_input()
                        print(f"[OK] pywinauto({backend}) çift tıkla: '{target}'"); return True
                except Exception: continue
        except Exception as _e:
            print(f"[DBLCLICK] pywinauto({backend}) başarısız: {_e}")
        return False

    if _PW_OK and _pw_dbl("uia"): return True
    if _PW_OK and _pw_dbl("win32"): return True

    if _TESS_OK:
        try:
            _ocr_region = _get_window_region()
            _ocr_ox, _ocr_oy = (_ocr_region[0], _ocr_region[1]) if _ocr_region else (0, 0)
            shot = _pag.screenshot(region=_ocr_region) if _ocr_region else _pag.screenshot()
            data = _tess.image_to_data(shot, lang="tur+eng", output_type=_tess.Output.DICT)
            for _i, _w in enumerate(data["text"]):
                if _w and target.lower() in _w.lower() and data["conf"][_i] > 30:
                    _cx = data["left"][_i] + data["width"][_i] // 2 + _ocr_ox
                    _cy = data["top"][_i]  + data["height"][_i] // 2 + _ocr_oy
                    if _in_window(_cx, _cy):
                        _pag.doubleClick(_cx, _cy)
                        print(f"[OK] OCR cift tikla: '{_w}' @ ({_cx},{_cy})"); return True
        except Exception as _e:
            print(f"[DBLCLICK] OCR basarisiz: {_e}")

    _vx, _vy = _vision_find_desktop(target)
    if _vx and _vy and _in_window(_vx, _vy):
        _pag.doubleClick(_vx, _vy); print(f"[OK] Vision cift tikla: '{target}' @ ({_vx},{_vy})"); return True
    raise Exception(f"Element bulunamadi (cift tikla): '{target}'")


def _safe_right_click_desktop(target, window_title=""):
    """Desktop sağ tıklama — uia → win32 → OCR → vision."""
    print(f"[RCLICK] '{target}' aranıyor...")

    def _pw_right(backend):
        try:
            _win = _PwApp(backend=backend).connect(title_re=f".*{window_title}.*", timeout=3).top_window() if window_title else _get_active_window()
            if not _win: return False
            for _ctrl in [lambda: _win.child_window(title=target, found_index=0), lambda: _win.child_window(title_re=f".*{target}.*", found_index=0)]:
                try:
                    _el = _ctrl()
                    if _el.exists(timeout=1):
                        _el.set_focus(); _el.right_click_input()
                        print(f"[OK] pywinauto({backend}) sağ tıkla: '{target}'"); return True
                except Exception: continue
        except Exception as _e:
            print(f"[RCLICK] pywinauto({backend}) başarısız: {_e}")
        return False

    if _PW_OK and _pw_right("uia"): return True
    if _PW_OK and _pw_right("win32"): return True

    if _TESS_OK:
        try:
            _ocr_region = _get_window_region()
            _ocr_ox, _ocr_oy = (_ocr_region[0], _ocr_region[1]) if _ocr_region else (0, 0)
            shot = _pag.screenshot(region=_ocr_region) if _ocr_region else _pag.screenshot()
            data = _tess.image_to_data(shot, lang="tur+eng", output_type=_tess.Output.DICT)
            for _i, _w in enumerate(data["text"]):
                if _w and target.lower() in _w.lower() and data["conf"][_i] > 30:
                    _cx = data["left"][_i] + data["width"][_i] // 2 + _ocr_ox
                    _cy = data["top"][_i]  + data["height"][_i] // 2 + _ocr_oy
                    if _in_window(_cx, _cy):
                        _pag.rightClick(_cx, _cy)
                        print(f"[OK] OCR sag tikla: '{_w}' @ ({_cx},{_cy})"); return True
        except Exception as _e:
            print(f"[RCLICK] OCR basarisiz: {_e}")

    _vx, _vy = _vision_find_desktop(target)
    if _vx and _vy and _in_window(_vx, _vy):
        _pag.rightClick(_vx, _vy); print(f"[OK] Vision sag tikla: '{target}' @ ({_vx},{_vy})"); return True
    raise Exception(f"Element bulunamadi (sag tikla): '{target}'")


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
                _wait_region = _get_window_region()
                _wtxt = _tess.image_to_string(
                    _pag.screenshot(region=_wait_region) if _wait_region else _pag.screenshot(),
                    lang="tur+eng"
                )
                if target.lower() in _wtxt.lower():
                    print(f"[OK] OCR goruldu: '{target}'")
                    return True
            except Exception:
                pass
        _tw.sleep(1)
    print(f"[WARN] '{target}' {timeout}s icinde gorunmedi")
    return False


def _safe_assert_desktop(target):
    """Ekranda element / metin doğrula. Bulamazsa AssertionError fırlatır."""
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

    # OCR — sadece uygulama penceresiyle sınırlı
    if _TESS_OK:
        try:
            _region = _get_window_region()
            shot = _pag.screenshot(region=_region) if _region else _pag.screenshot()
            _txt = _tess.image_to_string(shot, lang="tur+eng")
            if target.lower() in _txt.lower():
                print(f"[OK] OCR: '{target}'"); return
        except Exception:
            pass

    # Vision
    _vx, _vy = _vision_find_desktop(target)
    if _vx and _vy:
        print(f"[OK] Vision: '{target}'"); return

    raise AssertionError(f"[FAIL] '{target}' ekranda bulunamadi")

def _refocus_window():
    """Her adım öncesi pencereyi öne getirir — başlık veya süreç adıyla bulur."""
    import os as _os_rf
    _exe_name = _os_rf.path.basename(_APP_PATH).lower() if "_APP_PATH" in globals() and _APP_PATH else ""

    def _bring_hwnd(hwnd):
        try:
            import win32gui as _wg_r, win32con as _wc_r
            _wg_r.ShowWindow(hwnd, _wc_r.SW_RESTORE)
            _wg_r.SetForegroundWindow(hwnd)
            return True
        except Exception:
            return False

    # 1. Pencere başlığıyla bul ──────────────────────────────────────────────
    if _WINDOW_TITLE:
        try:
            import win32gui as _wg, win32con as _wc
            _found_hwnd = None
            def _cb(hwnd, _):
                nonlocal _found_hwnd
                t = _wg.GetWindowText(hwnd)
                if _WINDOW_TITLE.lower() in t.lower() and _wg.IsWindowVisible(hwnd):
                    _found_hwnd = hwnd
                    return False
                return True
            _wg.EnumWindows(_cb, None)
            if _found_hwnd:
                _wg.ShowWindow(_found_hwnd, _wc.SW_RESTORE)
                _wg.SetForegroundWindow(_found_hwnd)
                return
        except Exception:
            pass
        if _PW_OK:
            try:
                _PwApp(backend="uia").connect(title_re=".*" + _WINDOW_TITLE + ".*", timeout=3).top_window().set_focus()
                return
            except Exception:
                pass

    # 2. Süreç adıyla pencere bul (window_title boşsa) ──────────────────────
    if _exe_name:
        try:
            import win32gui as _wg2, win32process as _wp2, win32con as _wc2
            import psutil as _psu_rf
            _pids = {p.pid for p in _psu_rf.process_iter(["name"]) if p.info["name"].lower() == _exe_name}
            _wins = []
            def _cb2(hwnd, _):
                if _wg2.IsWindowVisible(hwnd) and _wg2.GetWindowText(hwnd):
                    _, _pid = _wp2.GetWindowThreadProcessId(hwnd)
                    if _pid in _pids:
                        _wins.append(hwnd)
                return True
            _wg2.EnumWindows(_cb2, None)
            if _wins:
                _wg2.ShowWindow(_wins[0], _wc2.SW_RESTORE)
                _wg2.SetForegroundWindow(_wins[0])
                return
        except Exception:
            pass


# ── Uygulama başlat (zaten açıksa geç + öne getir) ──────────
def _is_app_running():
    """Uygulama çalışıyorsa True döner ve penceresini öne getirir."""
    # 1) Pencere başlığıyla kontrol (win32gui) ─────────────────
    _wtitle = ""
    if _wtitle:
        try:
            import win32gui as _wg2
            _fnd = []
            def _cb2(hwnd, _):
                t = _wg2.GetWindowText(hwnd)
                if _wtitle.lower() in t.lower() and _wg2.IsWindowVisible(hwnd):
                    _fnd.append(hwnd)
                return True
            _wg2.EnumWindows(_cb2, None)
            if _fnd:
                try: _wg2.SetForegroundWindow(_fnd[0])
                except Exception: pass
                return True
        except Exception: pass
        # pywinauto fallback ─────────────────────────────────
        if _PW_OK:
            try:
                _PwApp(backend="uia").connect(title_re=".*.*", timeout=2).top_window().set_focus()
                return True
            except Exception: pass
    # 2) Surec adiyla kontrol + PID bazli pencere odakla ───────
    try:
        import os as _os2, subprocess as _sp2
        _exe2 = _os2.path.basename(r"C:\\Users\\Sadik Demir\\AppData\\Local\\Postman\\Postman.exe")
        if not _exe2: return False
        _proc_found = False
        _boa_pids: set = set()
        # psutil varsa kullan (daha güvenilir) ─────────────────
        try:
            import psutil as _psu2
            for _p2 in _psu2.process_iter(["name", "pid"]):
                if _exe2.lower() == _p2.info["name"].lower():
                    _boa_pids.add(_p2.info["pid"]); _proc_found = True
        except ImportError:
            # tasklist fallback ──────────────────────────────
            _r2 = _sp2.run(["tasklist", "/FI", f"IMAGENAME eq {_exe2}", "/NH"],
                           capture_output=True, text=True, timeout=3)
            _proc_found = _exe2.lower() in _r2.stdout.lower()
        if not _proc_found: return False
        # Sürece ait pencereyi bul ve öne getir ─────────────────
        try:
            import win32gui as _wg3, win32process as _wp3
            _boa_wins = []
            def _cb3(hwnd, _):
                if _wg3.IsWindowVisible(hwnd) and _wg3.GetWindowText(hwnd):
                    _tid, _pid = _wp3.GetWindowThreadProcessId(hwnd)
                    if not _boa_pids or _pid in _boa_pids:
                        _boa_wins.append(hwnd)
                return True
            _wg3.EnumWindows(_cb3, None)
            if _boa_wins: _wg3.SetForegroundWindow(_boa_wins[0])
        except Exception: pass
        return True
    except Exception: pass
    return False
if _is_app_running():
    print("[OK] Uygulama zaten açık — mevcut pencere öne getirildi")
else:
    print("Başlatılıyor: C:\\Users\\Sadik Demir\\AppData\\Local\\Postman\\Postman.exe")
    _dsproc.Popen(r"C:\\Users\\Sadik Demir\\AppData\\Local\\Postman\\Postman.exe", shell=True, stdout=_dsproc.DEVNULL, stderr=_dsproc.DEVNULL, stdin=_dsproc.DEVNULL)
    # BOA penceresini bekle (max 30 saniye)
    _wait_start = time.time()
    _win_found = False
    _wait_exe = "postman.exe"
    _wait_title = ""
    while time.time() - _wait_start < 30:
        try:
            import win32gui as _wg_w, win32process as _wp_w, win32con as _wc_w
            # Süreç PID'lerini bul
            _pids_w = set()
            try:
                import psutil as _psu_w
                _pids_w = {p.pid for p in _psu_w.process_iter(["name"]) if p.info["name"].lower() == _wait_exe}
            except ImportError:
                import subprocess as _sp_w
                _r_w = _sp_w.run(["tasklist", "/FI", f"IMAGENAME eq {_wait_exe}", "/FO", "CSV", "/NH"], capture_output=True, text=True, timeout=5)
                for _ln_w in _r_w.stdout.splitlines():
                    _parts_w = _ln_w.strip('"').split('","')
                    if len(_parts_w) > 1:
                        try: _pids_w.add(int(_parts_w[1]))
                        except: pass
            if not _pids_w:
                time.sleep(1); continue
            _wins_w = []
            def _cb_w(hwnd, _):
                if _wg_w.IsWindowVisible(hwnd) and _wg_w.GetWindowText(hwnd):
                    _, _pid_w = _wp_w.GetWindowThreadProcessId(hwnd)
                    if _pid_w in _pids_w:
                        _t_w = _wg_w.GetWindowText(hwnd)
                        if not _wait_title or _wait_title.lower() in _t_w.lower():
                            _wins_w.append(hwnd)
                return True
            _wg_w.EnumWindows(_cb_w, None)
            if _wins_w:
                _wg_w.ShowWindow(_wins_w[0], _wc_w.SW_RESTORE)
                _wg_w.SetForegroundWindow(_wins_w[0])
                _win_found = True
                print(f"[OK] Pencere {time.time()-_wait_start:.1f}s sonra görüldü")
                break
        except Exception: pass
        time.sleep(1)
    if not _win_found: print("[WARN] Uygulama penceresi 30s içinde görünmedi, devam ediliyor")
    time.sleep(2)

try:
    _check_stop()
    print('STEP_START:0')
    try:
        # 3 saniye bekle
        time.sleep(3)
        print('STEP_DONE:0')
    except Exception as _e_0:
        print(f'[FAIL] {_e_0}')
        print('STEP_FAIL:0')
        raise

    _check_stop()
    print('STEP_START:1')
    try:
        # "Ctrl+T" bas
        _pag.hotkey('ctrl', 't')
        time.sleep(0.3)
        print('STEP_DONE:1')
    except Exception as _e_1:
        print(f'[FAIL] {_e_1}')
        print('STEP_FAIL:1')
        raise

    _check_stop()
    print('STEP_START:2')
    try:
        # 2 saniye bekle
        time.sleep(2)
        print('STEP_DONE:2')
    except Exception as _e_2:
        print(f'[FAIL] {_e_2}')
        print('STEP_FAIL:2')
        raise

    _check_stop()
    print('STEP_START:3')
    try:
        # "Enter URL or paste text" tıkla
        _pag.press("enter")
        time.sleep(0.3)
        print('STEP_DONE:3')
    except Exception as _e_3:
        print(f'[FAIL] {_e_3}')
        print('STEP_FAIL:3')
        raise

    _check_stop()
    # [SQL] SQL 5
    print('STEP_START:4')
    try:
        import pyodbc as _pyodbc_4
        _db_4 = _pyodbc_4.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-NV3TGCG;DATABASE=LifeCoachDb;Trusted_Connection=yes')
        _cur_4 = _db_4.cursor()
        _cur_4.execute('SELECT StudentWeight FROM Students WHERE StudentID = 2')
        _rows_4 = _cur_4.fetchall()
        print(f'[SQL] {len(_rows_4)} kayit:')
        for _r in _rows_4: print('  ', list(_r))
        _VARS['agirlik'] = str(_rows_4[0][0] if _rows_4 else '')
        print(f'[SQL→_VARS] agirlik = {_VARS['agirlik']}')
        _db_4.close()
        print('STEP_DONE:4')
    except Exception as _e_4:
        print(f'[FAIL] {_e_4}')
        print('STEP_FAIL:4')
        raise

    _check_stop()
    # [API] GET  https://jsonplaceholder.typicode.com/posts/1 — API 6
    print('STEP_START:5')
    try:
        import requests as _rm
        _hdrs_5 = {}
        _resp_5 = _rm.get(' https://jsonplaceholder.typicode.com/posts/1', headers=_hdrs_5, timeout=30)
        _resp_5.raise_for_status()
        print(f'[API] Status: {_resp_5.status_code}')
        print(f'[API] Yanit: {_resp_5.text[:500]}')
        _api_json_5 = _resp_5.json()
        def _jpath_5(d, p):
            for k in p.split('.'):
                if isinstance(d, dict): d = d.get(k)
                elif isinstance(d, list):
                    try: d = d[int(k)]
                    except: return None
                else: return None
            return d
        _extracted_5 = _jpath_5(_api_json_5, 'title')
        print(f'[API.title] {_extracted_5}')
        _VARS['postId'] = str(_extracted_5 if _extracted_5 is not None else '')
        print(f'[API→_VARS] postId = {_VARS['postId']}')
        print('STEP_DONE:5')
    except Exception as _e_5:
        print(f'[FAIL] {_e_5}')
        print('STEP_FAIL:5')
        raise

    _check_stop()
    print('STEP_START:6')
    try:
        # {{ agirlik }} yaz
        _safe_type_desktop(str(_VARS.get('agirlik', '')))
        print('STEP_DONE:6')
    except Exception as _e_6:
        print(f'[FAIL] {_e_6}')
        print('STEP_FAIL:6')
        raise

    _check_stop()
    print('STEP_START:7')
    try:
        # {{ postId }} yaz
        _safe_type_desktop(str(_VARS.get('postId', '')))
        print('STEP_DONE:7')
    except Exception as _e_7:
        print(f'[FAIL] {_e_7}')
        print('STEP_FAIL:7')
        raise

    _check_stop()
    # [KOORDİNAT TIKLAMA] Nokta 1 tıkla → (997, 201)
    print('STEP_START:8')
    try:
        _refocus_window()
        _do_robust_click(997, 201)
        time.sleep(0.3)
        print('[OK] Koordinat tiklandi: (997, 201)')
        print('STEP_DONE:8')
    except Exception as _e_8:
        print(f'[FAIL] {_e_8}')
        print('STEP_FAIL:8')
        raise

    _check_stop()
    # [KOORDİNAT TIKLAMA] Nokta 2 tıkla → (291, 100)
    print('STEP_START:9')
    try:
        _refocus_window()
        _do_robust_click(291, 100)
        time.sleep(0.3)
        print('[OK] Koordinat tiklandi: (291, 100)')
        print('STEP_DONE:9')
    except Exception as _e_9:
        print(f'[FAIL] {_e_9}')
        print('STEP_FAIL:9')
        raise

    _check_stop()
    # [KOORDİNAT TIKLAMA] Nokta 1 tıkla → (460, 307)
    print('STEP_START:10')
    try:
        _refocus_window()
        _do_robust_click(460, 307)
        time.sleep(0.3)
        print('[OK] Koordinat tiklandi: (460, 307)')
        print('STEP_DONE:10')
    except Exception as _e_10:
        print(f'[FAIL] {_e_10}')
        print('STEP_FAIL:10')
        raise

except Exception as e:
    print(f"HATA: {e}")
    raise

sys.exit(0)