# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
_VARS = {}  # adımlar arası değişken havuzu

from selenium.webdriver.chrome.options import Options as _CrOpts
_cr_opts = _CrOpts()
# _cr_opts.add_argument('--headless')  # Başsız mod için aktif et
try:
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service as _CrSvc
    driver = webdriver.Chrome(service=_CrSvc(ChromeDriverManager().install()), options=_cr_opts)
except Exception:
    driver = webdriver.Chrome(options=_cr_opts)  # Selenium 4.6+ otomatik driver

# ── Tarayıcı başlatılamadıysa net hata ver ───────────────────
if 'driver' not in dir():
    print("[HATA] Tarayıcı sürücüsü başlatılamadı. Chrome/Firefox kurulu mu?")
    raise SystemExit(1)


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
    """Base64 görseli pencere bölgesinde (yoksa tüm ekranda) OpenCV ile ara."""
    _tmp_path = _ios.path.join(_itmp.gettempdir(), f"_img_find_{id(b64_data)}.png")
    try:
        with open(_tmp_path, "wb") as _f:
            _f.write(_ib64.b64decode(b64_data))
        _region = _get_window_region()
        _start = _itime.time()
        while _itime.time() - _start < timeout:
            _elapsed = _itime.time() - _start
            _conf = max(0.65, threshold - (_elapsed / timeout) * 0.20)
            _coords = _find_image_on_screen(_tmp_path, threshold=_conf, region=_region)
            if _coords:
                return _coords
            _itime.sleep(0.3)
        return None
    finally:
        try: _ios.unlink(_tmp_path)
        except Exception: pass

def _find_image_on_screen(target_path, threshold=0.80, region=None):
    """OpenCV multi-scale template matching. region=(x,y,w,h) ile kısıtlı arama yapar."""
    try:
        import cv2 as _cv2, numpy as _np
        import pyautogui as _pag_sc
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
        for _sc in _np.linspace(0.7, 1.3, 13):
            _rw, _rh = int(_w*_sc), int(_h*_sc)
            if _rw < 10 or _rh < 10: continue
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


from selenium.webdriver.support.ui import WebDriverWait as _WDWEB
from selenium.webdriver.support import expected_conditions as _EC_WEB

def _wdwait(driver, timeout=10):
    return _WDWEB(driver, timeout)


def _safe_click_web(driver, text):
    """Web elementi tıkla — WebDriverWait + scroll + çoklu strateji"""
    from selenium.webdriver.common.by import By
    import time
    strategies = [
        (By.XPATH,         f'//*[normalize-space(text())="{text}"]'),
        (By.XPATH,         f'//button[contains(normalize-space(.),"{text}")]'),
        (By.XPATH,         f'//a[contains(normalize-space(.),"{text}")]'),
        (By.XPATH,         f'//input[@value="{text}"]'),
        (By.XPATH,         f'//*[@aria-label="{text}"]'),
        (By.XPATH,         f'//*[contains(text(),"{text}")]'),
        (By.LINK_TEXT,     text),
        (By.PARTIAL_LINK_TEXT, text),
    ]
    for scroll_pass in range(3):
        for by, val in strategies:
            try:
                el = _wdwait(driver, 5).until(_EC_WEB.element_to_be_clickable((by, val)))
                driver.execute_script("arguments[0].scrollIntoView({block:'center',inline:'nearest'});", el)
                time.sleep(0.15)
                el.click()
                print(f"[OK] Tıklandı: {text}")
                return
            except Exception:
                continue
        driver.execute_script(f"window.scrollBy(0, {350 * (scroll_pass + 1)});")
        time.sleep(0.4)
    raise Exception(f"Web elementi bulunamadı: {text}")


def _safe_input_web(driver, field_hint, value, is_password=False):
    """Input alanını placeholder/label/name/id ile bul ve değer gir"""
    from selenium.webdriver.common.by import By
    import time
    hint = (field_hint or "").strip().lower()
    val  = str(value)

    strategies = []
    if is_password:
        strategies += [
            (By.XPATH,       '//input[@type="password"]'),
            (By.CSS_SELECTOR,'input[type="password"]'),
        ]
    if hint:
        strategies += [
            (By.XPATH, f'//input[contains(translate(@placeholder,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"{hint}")]'),
            (By.XPATH, f'//textarea[contains(translate(@placeholder,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"{hint}")]'),
            (By.XPATH, f'//input[@id=//label[contains(translate(.,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"{hint}")]/@for]'),
            (By.XPATH, f'//input[contains(translate(@name,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"{hint}")]'),
            (By.XPATH, f'//input[contains(translate(@id,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"{hint}")]'),
            (By.XPATH, f'//input[contains(translate(@aria-label,"ABCDEFGHIJKLMNOPQRSTUVWXYZ","abcdefghijklmnopqrstuvwxyz"),"{hint}")]'),
        ]
    strategies += [
        (By.XPATH,        '//input[@type="text" or not(@type)]'),
        (By.CSS_SELECTOR, 'input:not([type="hidden"]):not([type="submit"]):not([type="button"]):not([type="checkbox"]):not([type="radio"])'),
    ]

    for by, sel in strategies:
        try:
            el = _wdwait(driver, 5).until(_EC_WEB.visibility_of_element_located((by, sel)))
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            time.sleep(0.2)
            el.clear()
            el.send_keys(val)
            print(f"[OK] Girildi: '{val}' (hint: {hint or 'generic'})")
            return
        except Exception:
            continue
    raise Exception(f"Input alanı bulunamadı: {field_hint}")


def _safe_assert_web(driver, text):
    """Metni sayfada doğrula — kaynak + element + scroll"""
    from selenium.webdriver.common.by import By
    import time
    if text in driver.page_source:
        print(f"[OK] Doğrulandı: {text}"); return
    for xp in [
        f'//*[contains(normalize-space(.),"{text}")]',
        f'//*[contains(@value,"{text}")]',
        f'//*[contains(@placeholder,"{text}")]',
    ]:
        try:
            el = driver.find_element(By.XPATH, xp)
            if el.is_displayed():
                print(f"[OK] Doğrulandı: {text}"); return
        except Exception:
            continue
    driver.execute_script("window.scrollTo(0,0);"); time.sleep(0.5)
    assert text in driver.page_source, f"Beklenen metin yok: {text}"


driver.maximize_window()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.vakifkatilim.com.tr/tr")
    time.sleep(1.5)
    print('STEP_START:0')
    # Aşağı kaydırılır
    driver.execute_script("window.scrollBy(0, 400);")
    time.sleep(0.4)
    print('STEP_DONE:0')

    print('STEP_START:1')
    # "Finansman Hesapl" tıklanır
    _safe_click_web(driver, 'Finansman Hesapl')
    time.sleep(0.5)
    print('STEP_DONE:1')

    print('STEP_START:2')
    # "Finansman Türü" görünmeli
    _safe_assert_web(driver, 'Finansman Türü')
    print('STEP_DONE:2')

    print('STEP_START:3')
    # "İhtiyaç Finansmanı" Tıklanır
    driver.get("https://İhtiyaç Finansmanı")
    time.sleep(1.5)
    print('STEP_DONE:3')

except Exception as e:
    print(f"HATA: {e}")
    raise
finally:
    driver.quit()