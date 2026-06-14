# -*- coding: utf-8 -*-
import pyautogui as _pag
import subprocess as _dsproc
import time

_AI_CONFIG_PATH = r"C:\Users\Sadik Demir\Documents\GitHub\OtomasyoToolFastApi\backend\ai_config.json"
_WINDOW_TITLE   = ""
_VARS = {}  # adımlar arası değişken havuzu


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

    print('STEP_START:6')
    # {{ agirlik }} yaz
    _safe_type_desktop(str(_VARS.get('agirlik', '')))
    print('STEP_DONE:6')

    print('STEP_START:7')
    # {{ postId }} yaz
    _safe_type_desktop(str(_VARS.get('postId', '')))
    print('STEP_DONE:7')

    # [GÖRSEL DOĞRULA] Görsel element
    print('STEP_START:8')
    try:
        _img_b64_8 = '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'
        _res_8 = _find_b64_on_screen(_img_b64_8, timeout=8)
        if not _res_8: raise Exception('Gorsel bulunamadi: Görsel element')
        print('[OK] Gorsel dogrulandi: Görsel element')
        print('STEP_DONE:8')
    except Exception as _e_8:
        print(f'[FAIL] {_e_8}')
        print('STEP_FAIL:8')
        raise

except Exception as e:
    print(f"HATA: {e}")
    raise