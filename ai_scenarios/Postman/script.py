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
    # [GÖRSEL TIKLAMA] Nokta 1 tıkla
    print('STEP_START:8')
    try:
        _refocus_window()
        _img_b64_8 = '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'
        _coords_8 = _find_b64_on_screen(_img_b64_8, timeout=10)
        if not _coords_8: raise Exception('Gorsel bulunamadi: Nokta 1 tıkla')
        _do_robust_click(_coords_8[0], _coords_8[1])
        print('[OK] Gorsel tiklandi: Nokta 1 tıkla')
        time.sleep(0.5)
        print('STEP_DONE:8')
    except Exception as _e_8:
        print(f'[FAIL] {_e_8}')
        print('STEP_FAIL:8')
        raise

    _check_stop()
    # [GÖRSEL TIKLAMA] Nokta 2 tıkla
    print('STEP_START:9')
    try:
        _refocus_window()
        _img_b64_9 = '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'
        _coords_9 = _find_b64_on_screen(_img_b64_9, timeout=10)
        if not _coords_9: raise Exception('Gorsel bulunamadi: Nokta 2 tıkla')
        _do_robust_click(_coords_9[0], _coords_9[1])
        print('[OK] Gorsel tiklandi: Nokta 2 tıkla')
        time.sleep(0.5)
        print('STEP_DONE:9')
    except Exception as _e_9:
        print(f'[FAIL] {_e_9}')
        print('STEP_FAIL:9')
        raise

except Exception as e:
    print(f"HATA: {e}")
    raise

sys.exit(0)