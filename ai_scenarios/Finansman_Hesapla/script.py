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
    # "Finansman Hesapla" tıklanır
    _safe_click_web(driver, 'Finansman Hesapla')
    time.sleep(0.5)
    print('STEP_DONE:1')

    print('STEP_START:2')
    # "Finansman Türü" görünmeli
    _safe_assert_web(driver, 'Finansman Türü')
    print('STEP_DONE:2')

    # [GÖRSEL TIKLAMA] Görsel element
    print('STEP_START:3')
    try:
        _img_b64_3 = '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E6fN1uINM9UXSTWl0yJN62THjh00efJktmPdtWtXqq2tpbPPPrv43IxBdNxxx9Hll19On3zyCXXo0IHQBv3GG28kFAy4UaNG0aWXXhraJHvmmWeoX79+tGXzZobn+++/p7POOosOP/xw6tqlK6uHDR9G77//PvXq1YsNTjBi1h86dCjrBy7wn3vuuQ6u1ehWlqiLCawoEH7kkUcI+h566KFI38GHv91+9dVXqUuXLnTkkUcSsHR0dvcRM8ia6vvyyy/pfyedRCeccAJbGXTq1ImGDRvGHnEQU8T2qaeeYtcA18JvD8l89913s2sAOmLCZYEVBQn72GOP0aGHHkq4waJAz8yZM+mGG24g+A0+4MbjkUofx/POO+9AZKcqSMq16za5iaxILiTwjFkLafqsRQR+8yCVRmtN6dRMzbx58+j111+nd999l3755Rea4zz7/vXXX4RlKWaC/fffn7D5hV1sDLzPPvuMtUHnlgqFAl144YX07bff0qpVqziZfRnYm2++yZIY3y20bOkyOu+88wiyCxYsYLPE0qVLac8996SbbrqJMAAhjFnqggsuoD/++INgD7hQQ8dQJ7ExI4JPVuDPG2+8Qf4CW1G8Kt8hM23aVLr++uvZYwN8w80FCTFlyhR69tlnwVIssK3Sh0cSJM1g52aHL0tDQn/99dcsTv5EwbN7//79WCxXrVzFYjN69Gi6+OKLaf78+QR/EJOXX36Znd92220sdriZYuPygQceYI8UiCP4nnzyScJNVtzce+211wg31QUL5rNrL+orOpb6RMyC1AozVzBm5CDq2a0jS8zeQ+UzMk/gNq2aE/hRF4FpuRxkqikKG57g+34effRRdtfGsy3u3LiTr1y5khYtWsSed5F0SKDddtuNDjzwQJaE4PWbwizVqlUr+vDDD4tkJCi+CnTAgAFsB3zsuLF07LHHspm/Xbt2jK9FixY0duxYZp9vmk2bNo322msvmjzJXSHAFma/p59+mt5++21mnwlLDlOnTqU77rgjUDCTSlgpznfs4o8bN47uv/9+uuWWW9iruUKhwGZjJMbvv/8eUBunD8vftWvXsg/cwCcII7bPPfccDR48GE1WrrjiChoxwrXXtFlTQpKec8457KtxMfsjdjVNmrCVC579586dy/qQ4M8//zxh9YOE33XXXdn169OnD4sxbsrMgHfATI7Yt2vXnvH1clZCfn0em4Uq6RRjwXRCFUhIJGYxkYWltZjA4AuY0nI5yJQ4ibFMbOclFAeBNpISCchpcTUGMAYLZinMOODH7IKv6sRyDjPYwoUL2dIR76vRzwval1xyCWvi+Qw3gssuu4xatGzOaPyAQYkbCW/LaqwYFi9eTIt9BbOTjDfO9yVLlrDExeOFKI9l8GmnnRYgx+lr2bIlnXzyyWxWR6KJScWV9e7dmwqF0gWG38cccwwhjrhRgo/3wia+BnXNmjX08ccfU/fu3ekkZ7kOHn8BHTpEGr550U+DvmbNmhFmcD99Zzxv482wSFAslfkzcmwCJwxW4iSOsodBwpe3UTwifcCAgfTDDz/QihUraPPmzWzZ3b9/f0KSYpMF76MxkEU5tPfee29U7BUWZqvWrVs7baBwqjL8wnf4gkGOJBEh7LLLLoTBLtJD7YJLgT7IjBkzhu666y56/PHH6YgjjiDEB48KLle643fffcdWSoi3qAk3ApkfIh/aWJbjWuG8akp9NkjFRO48cDRNd56B/XRblq0nMY8JrzlQb0zyZqCure3MNlTmOjMCZl08u2JTC0wHH3wwm9U2bNiAZqjg+RdEDLQ2bdpYnAlED2BFr2BWAl6+zPdLYZBj1eCnSc8F81hGn3/++fTpp58Skg5LZ2wa4jFBKm9ABF6sePhKyC+Km4jMDz9PVZ+rBmZKx8SEbeuboeNV63NYT2JuWoyNMCY5G6sxA2BmmensZr7yyit04oknEhISnc2bN6cePXoQnr/FZ0kMupdeeglsbHY7/fTTCc+J4nITA/Hff/9lfLKDiNXlkVPdPvURMyVsvvDCC6HXbviXHB999JFaQai3nrBpWFe3g/XgEQRJjJhhY5ERUxywVP/iiy/YCkhUg5sq+kR6Y1svAjyRB/XrzjaxsMTWk9TnyiyJpRAUmYwExLPkiy++yF4lYQkJHahHjhxJeHbDqw5sGoGORMXGzc8//8xmatAwM/3555+EnWhsjuG9KpboV199NQ0cOJAww4NPLApYjDWunzH5DrgBYVf4wQcfpIcffpgt9bHUxK7yddddR1hd+NhjT1esWMk2tcaPH8d0QQC709jVxl+XoR1XCgqGbt26sVd+eH2EnWbcgBC72bNns42+tm3bKqQbu+IiwBO5h7NrbTqW4nSjP8MklsBVjCS8nzzjjDPY+91TTz0V2IrlkEMOIczQWFIef/zx7N9Z1DrvpfH+87777iM8t4EZyYEdZexcQ0fr1q3ZLI7n7ClTpih3pyEfVRSwo0QIu8JYFaC0b9+ePXNi5rzyyivpoosuipSTdWCHHRtab731FkEXnrfPPPNMGjJkCLMjkxFpkqtRZCkUCux12IQJE+j2229nNxnEDq8L8WoLM3WRufEkcQQwjlASK4gQ1Epi7E5i1xY19OBzz3hXKG7QoA06+olcuHhNBBr6yPvBTjCK1yxWmAEwI+P1SZHonSBBkYh4hYUZDc+F+OAE+D/44APiu694lQW+SZMmEXZrwYt3v9g591QFKsjhlRhwBjp8DWBFAQm+if6ADv9ARz/ahUKBsAuNzSesCoCDrwpGjBjB/goMfOCHHOTR5gVt0NEP2tFHH034YAv8xyy8ynmvjpkTNzCVD5CHHuiDHl5EGdwgBw0aRFjuf/PNNwQbwN23T1+GFXogizig4Nxf/Pr8534e03PVjcdUV+XzJ/dWK4mzDACHjh1dfJwQn8oqFNwbgMwuBiMGyb777ut2S451O+rooIMOYrMw3n9KWHIjFQoFwsoAmHfffffUduE/ZmIkb2plEgVIZtxEizaiL4VE2i6pjKbtOqKlLbm3NVr6lUw8DZVMkZ0cOt7x4tkLHx+MZNbsWLN6DT3xxBNsFxcJFCsmuCA0Y8UbGZJHoDHWyWPHJS0ksZOGKa8EXrlgDlkffwAAAghJREFUyYsPfWDnlYNLWuO58d5772UfO8RmV6wexwU/j9D0d0WcpwxAhNZqIafx3jzWZY5KGmdNoBvYsZDEDjKNK6HChI0nvFbin74i1Z8nOeZifx1j2CHG+08sD2P5jRgc5SF+jQCEZBISZOYTqrIllqP3tiAn15OXswZ27CSxRkhUmJBweCXToUMHT5OK22NRVSnFVarJ2bArWx6R88N9yxKERLeE5IBp/A1HIP9I5ZbEYWerl8LzqKweZAlColtCCrif/9ANmK+ghixSEdGJIJs6Y5bEloyagqx6/rzilpcdyQWRDV0JW9lJ9kJkoikiOn6yQl2wK9hCQJVJHGL3G4V0Y9GLQF5xy8JOaBA4LstoDjnuN6FYnFqjfh6i9Fi4JiPz0cwKdcGuYAsKlUkcZodINZT0l6gavMwDY71sEMhoGmCMxDT0pWGpJCxp/ICsMonBUJ0Fl6gxkW1cO0SS62mwEa00xwzx+JJYIYkvjOJXslgL/EKzyFa2E//wKxuIBmU4l4hmPI6k6nNxzGAoGOLxJbFCsiDrE2hCMwxZGr4wmw4lSlUUXUdnQ+BpCP7HjqN0nyLg6htCqPiQdZM4F494+LjpFHWUqih6ClNVJbqT+C9302wQy3VkfbUjMKY0635lbXk8Sgl9Zxe3OSAkuiSkyo548kGcn6vJMSL2+JroQiGs4/8AAAD///SJKK8AAAAGSURBVAMAAkeo3xkMwQQAAAAASUVORK5CYII='
        _coords_3 = _find_b64_on_screen_web(_img_b64_3, timeout=10)
        if not _coords_3: raise Exception('Gorsel bulunamadi: Görsel element')
        import pyautogui as _pag_web; _pag_web.click(_coords_3[0], _coords_3[1])
        print('[OK] Gorsel tiklandi: Görsel element')
        time.sleep(0.5)
        print('STEP_DONE:3')
    except Exception as _e_3:
        print(f'[FAIL] {_e_3}')
        print('STEP_FAIL:3')
        raise

    print('STEP_START:4')
    # "Taşıt Finansmanı 0 km" tıklanır
    _safe_click_web(driver, 'Taşıt Finansmanı 0 km')
    time.sleep(0.5)
    print('STEP_DONE:4')

    print('STEP_START:5')
    # "Tutar" görünmeli
    _safe_assert_web(driver, 'Tutar')
    print('STEP_DONE:5')

    print('STEP_START:6')
    # "100.00" Tıklanır
    _safe_click_web(driver, '100.00')
    time.sleep(0.5)
    print('STEP_DONE:6')

    print('STEP_START:7')
    # "Ctrl+A" Bas
    _safe_click_web(driver, 'Ctrl+A')
    time.sleep(0.5)
    print('STEP_DONE:7')

    print('STEP_START:8')
    # "Delete" Bas
    _safe_click_web(driver, 'Delete')
    time.sleep(0.5)
    print('STEP_DONE:8')

    print('STEP_START:9')
    # "400000" yaz
    _safe_input_web(driver, '', '400000', is_password=False)
    time.sleep(0.3)
    print('STEP_DONE:9')

except Exception as e:
    print(f"HATA: {e}")
    raise
finally:
    driver.quit()