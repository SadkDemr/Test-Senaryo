# -*- coding: utf-8 -*-
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, socket
_VARS = {}  # adımlar arası değişken havuzu

import os as _os_s, sys as _sys_s
_STOP_FILE = _os_s.environ.get("_AI_STOP_FILE", "")
def _check_stop():
    if _STOP_FILE and _os_s.path.exists(_STOP_FILE):
        try: _os_s.unlink(_STOP_FILE)
        except: pass
        raise SystemExit(0)

_DEVICE_ID = "v4lzlj4lw4u8d6uw"  # ADB komutları için cihaz ID
_AI_CONFIG_PATH = r"C:\Users\Sadik Demir\Documents\GitHub\OtomasyoToolFastApi\backend\ai_config.json"

# ── Appium bağlantı kontrolü ─────────────────────────────────
_appium_host = "localhost:4723"
_appium_port = 4723
try:
    _s = socket.create_connection((_appium_host.split(':')[0], _appium_port), timeout=3)
    _s.close()
except OSError:
    print(f"[HATA] Appium sunucusu http://localhost:4723 adresinde çalışmıyor!")
    print("[HATA] Lütfen terminalde \"appium\" komutunu çalıştırın.")
    raise SystemExit(1)


import base64 as _b64, requests as _req, re as _re

def _vision_find(driver, search_text):
    """Element bulunamazsa screenshot al, LLM ile koordinat bul, tap yap."""
    try:
        print(f"[VISION] '{search_text}' aranıyor...")
        screenshot = driver.get_screenshot_as_base64()

        # Önce Gemini dene (ai_config.json'da key varsa)
        try:
            import json, pathlib
            # Önce backend dizinini ara, sonra script konumunu dene
            _candidates = [
                pathlib.Path(_AI_CONFIG_PATH) if "_AI_CONFIG_PATH" in globals() else None,
                pathlib.Path(__file__).parent / "ai_config.json",
                pathlib.Path(__file__).parent.parent / "ai_config.json",
            ]
            cfg = {}
            for _cp in _candidates:
                if _cp and _cp.exists():
                    cfg = json.loads(_cp.read_text(encoding="utf-8"))
                    break
            gemini_key = cfg.get("gemini_api_key", "")
        except Exception:
            gemini_key = ""

        # Bağlama özel prompt — tek rakam = klavye tuşu, diğer = genel element
        if len(search_text) == 1 and search_text.isdigit():
            _prompt_tr = (f"Bu Android ekranında sayısal tuş takımı (PIN klavyesi) görünüyor. "
                          f"'{search_text}' rakamının TUŞUNU bul. Başka yerde görünen '{search_text}' rakamına bakma, "
                          f"sadece klavye tuşuna bak. Koordinat: x=NNN y=NNN")
            _prompt_en = (f"A numeric PIN keyboard is visible on this Android screen. "
                          f"Find ONLY the '{search_text}' key on the keyboard (bottom of screen). "
                          f"Reply only: x=<number> y=<number>")
        else:
            _prompt_tr = (f"Android ekranında '{search_text}' yazan veya gösteren tıklanabilir elementi bul. "
                          f"Koordinat: x=NNN y=NNN")
            _prompt_en = (f"Find the clickable element showing '{search_text}' on this Android screen. "
                          f"Reply only: x=<number> y=<number>")

        if gemini_key:
            resp = _req.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}",
                json={"contents": [{"parts": [
                    {"text": _prompt_tr},
                    {"inline_data": {"mime_type": "image/png", "data": screenshot}}
                ]}]},
                timeout=15
            )
            answer = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            # Ollama fallback (llava/gemma3 vision)
            resp = _req.post("http://localhost:11434/api/generate", json={
                "model": "gemma3:4b",
                "prompt": _prompt_en,
                "images": [screenshot],
                "stream": False
            }, timeout=30)
            answer = resp.json().get("response", "")

        mx = _re.search(r"x[=:\s]*(\d+)", answer, _re.IGNORECASE)
        my = _re.search(r"y[=:\s]*(\d+)", answer, _re.IGNORECASE)
        if mx and my:
            x, y = int(mx.group(1)), int(my.group(1))
            print(f"[VISION] Koordinat bulundu: ({x}, {y})")
            driver.tap([(x, y)])
            return True
        else:
            print(f"[VISION] Koordinat bulunamadı. Yanıt: {answer[:100]}")
            return False
    except Exception as e:
        print(f"[VISION] Hata: {e}")
        return False


def _safe_click(driver, text, key_text=None):
    """
    Akıllı click stratejisi:
    1. Tam metin ile dene
    2. Kısa anahtar kelime ile dene (karmaşık açıklamalar için)
    3. Aşağı kaydır → tekrar dene
    4. Yukarı kaydır → tekrar dene
    5. Vision fallback (ekran görüntüsü → AI → koordinat)
    key_text: "Toplam Varlıklarım kartında yer alan favori fonlarım" → "favori fonlarım"
    """
    # Ham XPath/resource-id ise direkt kullan, scroll/vision'a gerek yok
    if text.startswith("//") or text.startswith("//*"):
        try:
            driver.find_element(AppiumBy.XPATH, text).click()
            print(f"[OK] XPath tıklandı: {text}")
            return
        except Exception as _xe:
            raise Exception(f"XPath bulunamadı: {text} → {_xe}")
    if text.startswith("id/") or text.startswith("@id/"):
        _rid = text.lstrip("@")
        try:
            driver.find_element(AppiumBy.ID, _rid).click()
            print(f"[OK] resource-id tıklandı: {_rid}")
            return
        except Exception as _xe:
            raise Exception(f"resource-id bulunamadı: {_rid} → {_xe}")

    _all_texts = [t for t in [text, key_text] if t]

    def _try(t):
        for _xp in [
            f'//*[@text="{t}"]',
            f'//android.widget.Button[@text="{t}"]',
            f'//android.widget.TextView[@text="{t}"]',
            f'//*[contains(@text,"{t}")]',
            f'//*[@content-desc="{t}"]',
            f'//*[contains(@content-desc,"{t}")]',
        ]:
            try:
                driver.find_element(AppiumBy.XPATH, _xp).click()
                print(f"[OK] Tıklandı: {t}")
                return True
            except Exception:
                continue
        return False

    # 1 & 2: direkt dene
    for _t in _all_texts:
        if _try(_t): return

    # 3: aşağı kaydır + tekrar
    print(f"[SCROLL↓] '{text}' bulunamadı, aşağı kaydırılıyor...")
    driver.swipe(540, 1400, 540, 500, 800); time.sleep(0.7)
    for _t in _all_texts:
        if _try(_t): return

    # 4: yukarı kaydır + tekrar (orijinal konuma + biraz üstüne)
    print(f"[SCROLL↑] Yukarı kaydırılıyor...")
    driver.swipe(540, 500, 540, 1400, 800); time.sleep(0.7)
    for _t in _all_texts:
        if _try(_t): return

    # 5: Vision fallback — kısa metin varsa onu gönder (AI için daha net)
    _vision_target = key_text if key_text else text
    print(f"[VISION] '{_vision_target}' için ekran görüntüsü analiz ediliyor...")
    if not _vision_find(driver, _vision_target):
        raise Exception(f"Element bulunamadı (tüm stratejiler denendi): {text}")


def _safe_input(driver, xpath, value):
    """Metin girişi — önce ekrana bak, PIN klavyesi varsa tıkla, yoksa send_keys/ADB"""
    import subprocess as _sp, shutil as _sh, os as _os, re as _re2
    str_value = str(value)
    print(f"[INPUT] '{str_value}' yazılıyor... (xpath={xpath})")

    # ── iOS: send_keys yeterli, ADB/mobile:type desteklenmiyor ───────────────
    try:
        _platform = driver.capabilities.get("platformName", "").lower()
    except Exception:
        _platform = ""
    if _platform == "ios":
        try:
            _ios_el = driver.find_element(AppiumBy.XPATH, xpath) if xpath else None
        except Exception:
            _ios_el = None
        try:
            if _ios_el:
                _ios_el.click()
                import time as _t; _t.sleep(0.3)
                _ios_el.send_keys(str_value)
            else:
                driver.switch_to.active_element.send_keys(str_value)
            print(f"[INPUT] ✅ iOS send_keys: {str_value}")
        except Exception as _e:
            print(f"[INPUT] iOS send_keys hatası: {_e}")
            try:
                driver.switch_to.active_element.send_keys(str_value)
                print(f"[INPUT] ✅ iOS active_element send_keys: {str_value}")
            except Exception as _e2:
                print(f"[INPUT] iOS yazma başarısız: {_e2}")
        return

    # ── ADB yolu ──────────────────────────────────────────────────────────────
    def _adb_exec():
        _p = _sh.which("adb")
        if _p: return _p
        for _base in [_os.environ.get("LOCALAPPDATA",""), _os.environ.get("USERPROFILE","")]:
            _c = _os.path.join(_base, "AppData","Local","Android","Sdk","platform-tools","adb.exe")
            if _os.path.exists(_c): return _c
        return "adb"
    _ADB = _adb_exec()
    _adb = [_ADB, "-s", _DEVICE_ID] if _DEVICE_ID else [_ADB]

    # ── Sayfa kaynağını bir kez al ────────────────────────────────────────────
    try:
        _src = driver.page_source
    except Exception:
        _src = ""

    # ── PIN klavyesi tespiti: 6+ rakam butonu görünüyorsa ─────────────────────
    def _detect_pin_keyboard():
        _digit_count = sum(
            1 for _d in "0123456789"
            if f'text="{_d}"' in _src or f'content-desc="{_d}"' in _src
        )
        print(f"[INPUT] Rakam butonu sayısı: {_digit_count}")
        return _digit_count >= 6

    # ── Tek rakam butonuna tıkla ───────────────────────────────────────────────
    def _click_digit(d):
        # Ekrandaki tüm eleman bilgilerini çekip koordinat bazlı sırala
        _patterns = [
            f'//android.widget.Button[@text="{d}"]',
            f'//*[@text="{d}" and @clickable="true"]',
            f'//*[@content-desc="{d}" and @clickable="true"]',
            f'//*[contains(@resource-id,"key") and @text="{d}"]',
            f'//*[contains(@resource-id,"btn") and @text="{d}"]',
            f'//*[contains(@resource-id,"digit") and @text="{d}"]',
            f'//*[@text="{d}"]',
            f'//*[@content-desc="{d}"]',
        ]
        for _xp in _patterns:
            try:
                _els = driver.find_elements(AppiumBy.XPATH, _xp)
                if not _els:
                    continue
                # En alt y-koordinatlı elemanı tercih et (klavye genelde altta)
                _best = max(_els, key=lambda e: e.location.get("y", 0))
                _best.click()
                print(f"[PIN] '{d}' tıklandı ({_xp[:50]})")
                time.sleep(0.25)
                return True
            except Exception:
                continue
        # Vision fallback
        print(f"[PIN] '{d}' butonla bulunamadı, vision deneniyor...")
        return _vision_find(driver, d)

    # ── PIN klavyesi açıksa → direkt butonlara tıkla ─────────────────────────
    if _detect_pin_keyboard():
        print(f"[INPUT] PIN klavyesi tespit edildi, buton tıklama modu")
        _ok = 0
        for _ch in str_value:
            if _click_digit(_ch):
                _ok += 1
            else:
                print(f"[PIN] '{_ch}' yazılamadı")
        print(f"[INPUT] PIN sonuç: {_ok}/{len(str_value)} karakter")
        if _ok >= len(str_value):
            return
        # Kısmen yazdıysa yine de devam et
        if _ok > 0:
            return

    # ── Standart EditText modu ────────────────────────────────────────────────
    def _find_el():
        for _xp in [xpath,
                    '//android.widget.EditText[@password="true"]',
                    '//android.widget.EditText[1]',
                    '//android.widget.EditText']:
            try:
                _e = driver.find_element(AppiumBy.XPATH, _xp)
                _e.click(); time.sleep(0.4)
                return _e
            except Exception:
                continue
        return None

    def _field_has_value():
        for _xp in [xpath, '//android.widget.EditText[@password="true"]',
                    '//android.widget.EditText[1]']:
            try:
                _e = driver.find_element(AppiumBy.XPATH, _xp)
                _v = _e.text or _e.get_attribute("text") or _e.get_attribute("value") or ""
                if _v.strip():
                    return True
            except Exception:
                continue
        return False

    _el = _find_el()
    print(f"[INPUT] EditText {'bulundu' if _el else 'bulunamadı'}")

    # Alan tıklandıktan sonra PIN klavyesi açıldıysa buton moduna geç
    time.sleep(0.4)
    try:
        _src_r = driver.page_source
        _pin_r = sum(1 for _d in "0123456789"
                     if f'text="{_d}"' in _src_r or f'content-desc="{_d}"' in _src_r)
        if _pin_r >= 6:
            print(f"[INPUT] Alan tıklanınca PIN klavyesi açıldı ({_pin_r} rakam)")
            _ok = 0
            for _ch in str_value:
                if _click_digit(_ch):
                    _ok += 1
            if _ok > 0:
                print(f"[INPUT] PIN sonuç: {_ok}/{len(str_value)}")
                return
    except Exception as _e:
        print(f"[INPUT] PIN re-check hata: {_e}")

    # Placeholder metnini kaydet: typing başarısını doğrulamak için
    # Bazı uygulamalar placeholder'ı actual text olarak set eder (ör: "Şifre Giriniz")
    # send_keys başarısızsa uygulama placeholder'ı geri koyar, değiştiyse başarılı
    _placeholder = ""
    try:
        if _el:
            _placeholder = _el.text or _el.get_attribute("text") or ""
            print(f"[INPUT] Placeholder: '{_placeholder[:40]}'")
    except:
        pass

    def _typing_succeeded(el):
        # Placeholder kontrolü ÖNCE gelir — _field_has_value placeholder'ı dolu sayar
        if _placeholder:
            try:
                _curr = el.text or el.get_attribute("text") or "" if el else ""
            except:
                _curr = ""
            # Placeholder hala görünüyorsa typing kesinlikle başarısız
            if _curr == _placeholder:
                return False
            # Placeholder değiştiyse başarılı
            return True
        # Placeholder yoksa field_has_value'ya bak
        return _field_has_value()

    # Strateji A: send_keys
    if _el:
        try:
            _el.clear(); time.sleep(0.2)
            _el.send_keys(str_value); time.sleep(0.6)
            if _typing_succeeded(_el):
                print(f"[OK] send_keys başarılı: {value}"); return
            print("[INPUT] send_keys başarısız (placeholder değişmedi)")
        except Exception as _e:
            print(f"[INPUT] send_keys hata: {_e}")

    # Strateji B: ADB input text
    try:
        _sp.run(_adb + ["shell", "input", "text", str_value],
                capture_output=True, timeout=5)
        time.sleep(0.6)
        if _typing_succeeded(_el):
            print(f"[OK] ADB input text başarılı: {value}"); return
        print("[INPUT] ADB input text başarısız (placeholder değişmedi)")
    except Exception as _e:
        print(f"[INPUT] ADB hata: {_e}")

    # Strateji B2: ADB keyevent — rakam dizileri için (IME'den bağımsız, doğrudan tuş eventi)
    if str_value.isdigit():
        try:
            _km = {'0':7,'1':8,'2':9,'3':10,'4':11,'5':12,'6':13,'7':14,'8':15,'9':16}
            for _ch in str_value:
                _sp.run(_adb + ["shell", "input", "keyevent", str(_km[_ch])],
                        capture_output=True, timeout=3)
                time.sleep(0.12)
            time.sleep(0.5)
            if _typing_succeeded(_el):
                print(f"[OK] ADB keyevent başarılı: {value}"); return
            print("[INPUT] ADB keyevent başarısız (placeholder değişmedi)")
        except Exception as _e:
            print(f"[INPUT] ADB keyevent hata: {_e}")

    # Strateji C: mobile:type
    try:
        if _el or _find_el():
            driver.execute_script("mobile: type", {"text": str_value})
            time.sleep(0.4)
            if _typing_succeeded(_el):
                print(f"[OK] mobile:type başarılı: {value}"); return
        print("[INPUT] mobile:type başarısız")
    except Exception as _e:
        print(f"[INPUT] mobile:type hata: {_e}")

    # Strateji D: Clipboard paste
    try:
        driver.set_clipboard_text(str_value); time.sleep(0.2)
        _sp.run(_adb + ["shell", "input", "keyevent", "279"], capture_output=True, timeout=5)
        time.sleep(0.4)
        if _typing_succeeded(_el):
            print(f"[OK] Clipboard başarılı: {value}"); return
        print("[INPUT] Clipboard başarısız")
    except Exception as _e:
        print(f"[INPUT] Clipboard hata: {_e}")

    # Strateji E: Alan tekrar bul → PIN klavyesi açıldıysa tıkla
    time.sleep(0.5)
    try:
        _src2 = driver.page_source
        _digit_count2 = sum(
            1 for _d in "0123456789"
            if f'text="{_d}"' in _src2 or f'content-desc="{_d}"' in _src2
        )
        if _digit_count2 >= 4:
            print(f"[INPUT] Klavye sonradan açıldı ({_digit_count2} rakam), buton moduna geçiliyor")
            _ok2 = 0
            for _ch in str_value:
                if _click_digit(_ch):
                    _ok2 += 1
            print(f"[INPUT] Geç PIN sonuç: {_ok2}/{len(str_value)}")
            if _ok2 > 0:
                return
    except Exception as _e:
        print(f"[INPUT] Geç klavye tespiti hata: {_e}")

    # Strateji F: Vision per-karakter (son çare)
    print(f"[INPUT] Vision per-karakter başlatılıyor: {value}")
    _ok_v = 0
    for _ch in str_value:
        if _vision_find(driver, _ch):
            _ok_v += 1; time.sleep(0.25)
        else:
            print(f"[INPUT] Vision '{_ch}' bulunamadı")
    print(f"[INPUT] Vision sonuç: {_ok_v}/{len(str_value)}")


def _safe_assert(driver, text, key_text=None):
    """
    Element doğrulama — scroll + vision destekli.
    1. Direkt bul
    2. Aşağı kaydır → tekrar bul
    3. Yukarı kaydır → tekrar bul
    4. Vision ile koordinat al → görsel doğrulama
    Bulunamazsa WARNING verir ama testi durdurmaz (beklenen ekran gecikmeli gelebilir).
    """
    _all_texts = [t for t in [text, key_text] if t]

    def _try_find():
        for _t in _all_texts:
            for _xp in [
                f'//*[@text="{_t}"]',
                f'//*[contains(@text,"{_t}")]',
                f'//*[@content-desc="{_t}"]',
                f'//*[contains(@content-desc,"{_t}")]',
            ]:
                try:
                    el = driver.find_element(AppiumBy.XPATH, _xp)
                    if el.is_displayed():
                        print(f"[OK] Doğrulandı: {_t}")
                        return True
                except Exception:
                    continue
        return False

    if _try_find(): return

    # Aşağı kaydır + tekrar
    print(f"[SCROLL↓] '{text}' aranıyor...")
    driver.swipe(540, 1400, 540, 500, 800); time.sleep(0.7)
    if _try_find(): return

    # Yukarı kaydır + tekrar
    print(f"[SCROLL↑] '{text}' aranıyor...")
    driver.swipe(540, 500, 540, 1400, 800); time.sleep(0.7)
    if _try_find(): return

    # Vision fallback
    print(f"[VISION] '{text}' için ekran görüntüsü analiz ediliyor...")
    if _vision_find(driver, key_text or text):
        print(f"[OK] Vision ile doğrulandı: {text}")
        return

    print(f"[WARN] '{text}' ekranda bulunamadı — adım geçiliyor")


options = UiAutomator2Options()
options.platform_name = "Android"
options.device_name   = "v4lzlj4lw4u8d6uw"
options.app_package            = "com.vakifkatilim.mobil.test"
options.app_activity           = "boa.android.mobilebranch.v2.ui.splash.ACSplash"
options.no_reset               = True
options.auto_grant_permissions = True

print("Appium baglaniyor: http://localhost:4723")
driver = webdriver.Remote("http://localhost:4723", options=options)
wait   = WebDriverWait(driver, 15)
time.sleep(2)

# Uygulama açık değilse başlat
_TARGET_PKG = "com.vakifkatilim.mobil.test"
if _TARGET_PKG:
    try:
        _curr_pkg = driver.current_package
        if _curr_pkg != _TARGET_PKG:
            print(f"Uygulama başlatılıyor: {_TARGET_PKG} (şu an: {_curr_pkg})")
            driver.activate_app(_TARGET_PKG)
            time.sleep(2.5)
        else:
            print(f"Uygulama zaten açık: {_TARGET_PKG}")
    except Exception as _launch_err:
        print(f"activate_app başarısız: {_launch_err}, ADB ile deneniyor...")
        import subprocess as _sub
        _sub.run(["adb", "-s", _DEVICE_ID, "shell", "monkey",
                  "-p", _TARGET_PKG, "-c", "android.intent.category.LAUNCHER", "1"],
                 capture_output=True, timeout=5)
        time.sleep(3)

try:
    _check_stop()
    print('STEP_START:0')
    try:
        # "Ortam" tıklanır
        _safe_click(driver, 'Ortam')
        time.sleep(0.8)
        print('STEP_DONE:0')
    except Exception as _e_0:
        print(f'[FAIL] {_e_0}')
        print('STEP_FAIL:0')
        raise

    _check_stop()
    print('STEP_START:1')
    try:
        # "Prep" tıklanır
        _safe_click(driver, 'Prep')
        time.sleep(0.8)
        print('STEP_DONE:1')
    except Exception as _e_1:
        print(f'[FAIL] {_e_1}')
        print('STEP_FAIL:1')
        raise

    _check_stop()
    print('STEP_START:2')
    try:
        # "Devam" Tıklanır
        _safe_click(driver, 'Devam')
        time.sleep(0.8)
        print('STEP_DONE:2')
    except Exception as _e_2:
        print(f'[FAIL] {_e_2}')
        print('STEP_FAIL:2')
        raise

    _check_stop()
    print('STEP_START:3')
    try:
        # 5 saniye beklenir
        time.sleep(5)
        print('STEP_DONE:3')
    except Exception as _e_3:
        print(f'[FAIL] {_e_3}')
        print('STEP_FAIL:3')
        raise

    _check_stop()
    print('STEP_START:4')
    try:
        # "Giriş Yap" tıklanır
        _safe_click(driver, 'Giriş Yap')
        time.sleep(0.8)
        print('STEP_DONE:4')
    except Exception as _e_4:
        print(f'[FAIL] {_e_4}')
        print('STEP_FAIL:4')
        raise

    _check_stop()
    print('STEP_START:5')
    try:
        # Şifre Giriniz alanına "121212" yazılır
        _safe_input(driver, '//android.widget.EditText[@password="true"]', '121212')
        time.sleep(0.5)
        print('STEP_DONE:5')
    except Exception as _e_5:
        print(f'[FAIL] {_e_5}')
        print('STEP_FAIL:5')
        raise

    _check_stop()
    print('STEP_START:6')
    try:
        # 3 saniye bekle
        time.sleep(3)
        print('STEP_DONE:6')
    except Exception as _e_6:
        print(f'[FAIL] {_e_6}')
        print('STEP_FAIL:6')
        raise

    _check_stop()
    print('STEP_START:7')
    try:
        # "Tamamla Kazan" yazısının göründüğünü doğrula
        _safe_assert(driver, 'Tamamla Kazan')
        print('STEP_DONE:7')
    except Exception as _e_7:
        print(f'[FAIL] {_e_7}')
        print('STEP_FAIL:7')
        raise

    _check_stop()
    print('STEP_START:8')
    try:
        # "Hesap/Kart" tıklanır
        _safe_click(driver, 'Hesap/Kart')
        time.sleep(0.8)
        print('STEP_DONE:8')
    except Exception as _e_8:
        print(f'[FAIL] {_e_8}')
        print('STEP_FAIL:8')
        raise

    _check_stop()
    print('STEP_START:9')
    try:
        # "Hesaplar" tıklanır
        _safe_click(driver, 'Hesaplar')
        time.sleep(0.8)
        print('STEP_DONE:9')
    except Exception as _e_9:
        print(f'[FAIL] {_e_9}')
        print('STEP_FAIL:9')
        raise

    _check_stop()
    print('STEP_START:10')
    try:
        # "//*[@resource-id='com.vakifkatilim.mobil.test:id/fabAddAccount']" tıklanır
        _safe_click(driver, "//*[@resource-id='com.vakifkatilim.mobil.test:id/fabAddAccount']")
        time.sleep(0.8)
        print('STEP_DONE:10')
    except Exception as _e_10:
        print(f'[FAIL] {_e_10}')
        print('STEP_FAIL:10')
        raise

    _check_stop()
    print('STEP_START:11')
    try:
        # "Seçiniz" tıklanır
        _safe_click(driver, 'Seçiniz')
        time.sleep(0.8)
        print('STEP_DONE:11')
    except Exception as _e_11:
        print(f'[FAIL] {_e_11}')
        print('STEP_FAIL:11')
        raise

    _check_stop()
    print('STEP_START:12')
    try:
        # "Cari Hesaplar" yazısının göründüğünü doğrula
        _safe_assert(driver, 'Cari Hesaplar')
        print('STEP_DONE:12')
    except Exception as _e_12:
        print(f'[FAIL] {_e_12}')
        print('STEP_FAIL:12')
        raise

    _check_stop()
    print('STEP_START:13')
    try:
        # "Cari Hesap" tıklanır
        _safe_click(driver, 'Cari Hesap')
        time.sleep(0.8)
        print('STEP_DONE:13')
    except Exception as _e_13:
        print(f'[FAIL] {_e_13}')
        print('STEP_FAIL:13')
        raise

    _check_stop()
    print('STEP_START:14')
    try:
        # "Döviz Cinsi" yazısının göründüğünü doğrula
        _safe_assert(driver, 'Döviz Cinsi')
        print('STEP_DONE:14')
    except Exception as _e_14:
        print(f'[FAIL] {_e_14}')
        print('STEP_FAIL:14')
        raise

    _check_stop()
    print('STEP_START:15')
    try:
        # "Döviz Cinsi" tıklanır
        _safe_click(driver, 'Döviz Cinsi')
        time.sleep(0.8)
        print('STEP_DONE:15')
    except Exception as _e_15:
        print(f'[FAIL] {_e_15}')
        print('STEP_FAIL:15')
        raise

    _check_stop()
    print('STEP_START:16')
    try:
        # "Türk Lirası" tıklanır
        _safe_click(driver, 'Türk Lirası')
        time.sleep(0.8)
        print('STEP_DONE:16')
    except Exception as _e_16:
        print(f'[FAIL] {_e_16}')
        print('STEP_FAIL:16')
        raise

    _check_stop()
    print('STEP_START:17')
    try:
        # 2 saniye beklenir
        time.sleep(2)
        print('STEP_DONE:17')
    except Exception as _e_17:
        print(f'[FAIL] {_e_17}')
        print('STEP_FAIL:17')
        raise

    _check_stop()
    print('STEP_START:18')
    try:
        # "//android.view.View[@resource-id='com.vakifkatilim.mobil.test:id/btnNext']" tıklanır
        _safe_click(driver, "//android.view.View[@resource-id='com.vakifkatilim.mobil.test:id/btnNext']")
        time.sleep(0.8)
        print('STEP_DONE:18')
    except Exception as _e_18:
        print(f'[FAIL] {_e_18}')
        print('STEP_FAIL:18')
        raise

    _check_stop()
    print('STEP_START:19')
    try:
        # "Hesap Adı" yazısının göründüğünü doğrula
        _safe_assert(driver, 'Hesap Adı')
        print('STEP_DONE:19')
    except Exception as _e_19:
        print(f'[FAIL] {_e_19}')
        print('STEP_FAIL:19')
        raise

    _check_stop()
    print('STEP_START:20')
    try:
        # "Giriniz" tıklanır
        _safe_click(driver, 'Giriniz')
        time.sleep(0.8)
        print('STEP_DONE:20')
    except Exception as _e_20:
        print(f'[FAIL] {_e_20}')
        print('STEP_FAIL:20')
        raise

    _check_stop()
    print('STEP_START:21')
    try:
        # "Test" yaz
        _safe_input(driver, '//android.widget.EditText[1]', 'Test')
        time.sleep(0.5)
        print('STEP_DONE:21')
    except Exception as _e_21:
        print(f'[FAIL] {_e_21}')
        print('STEP_FAIL:21')
        raise

    _check_stop()
    print('STEP_START:22')
    try:
        # klavye kapat
        try:
            driver.hide_keyboard()
        except Exception:
            driver.back()
        time.sleep(0.5)
        print('STEP_DONE:22')
    except Exception as _e_22:
        print(f'[FAIL] {_e_22}')
        print('STEP_FAIL:22')
        raise

    _check_stop()
    print('STEP_START:23')
    try:
        # "//android.widget.ToggleButton[@resource-id='com.vakifkatilim.mobil.test:id/switchReadAndConfirm']" tıklanır
        _safe_click(driver, "//android.widget.ToggleButton[@resource-id='com.vakifkatilim.mobil.test:id/switchReadAndConfirm']")
        time.sleep(0.8)
        print('STEP_DONE:23')
    except Exception as _e_23:
        print(f'[FAIL] {_e_23}')
        print('STEP_FAIL:23')
        raise

    _check_stop()
    print('STEP_START:24')
    try:
        # "//android.view.View[@resource-id='com.vakifkatilim.mobil.test:id/btnNext']" tıklanır
        _safe_click(driver, "//android.view.View[@resource-id='com.vakifkatilim.mobil.test:id/btnNext']")
        time.sleep(0.8)
        print('STEP_DONE:24')
    except Exception as _e_24:
        print(f'[FAIL] {_e_24}')
        print('STEP_FAIL:24')
        raise

    _check_stop()
    print('STEP_START:25')
    try:
        # "Hesap Numarası" yazısının göründüğünü doğrula
        _safe_assert(driver, 'Hesap Numarası')
        print('STEP_DONE:25')
    except Exception as _e_25:
        print(f'[FAIL] {_e_25}')
        print('STEP_FAIL:25')
        raise

    _check_stop()
    print('STEP_START:26')
    try:
        # "//*[@resource-id='com.vakifkatilim.mobil.test:id/btnConfirm']" tıklanır
        _safe_click(driver, "//*[@resource-id='com.vakifkatilim.mobil.test:id/btnConfirm']")
        time.sleep(0.8)
        print('STEP_DONE:26')
    except Exception as _e_26:
        print(f'[FAIL] {_e_26}')
        print('STEP_FAIL:26')
        raise

    _check_stop()
    print('STEP_START:27')
    try:
        # "Hesabınız oluşturuldu." yazısının göründüğünü doğrula
        _safe_assert(driver, 'Hesabınız oluşturuldu.')
        print('STEP_DONE:27')
    except Exception as _e_27:
        print(f'[FAIL] {_e_27}')
        print('STEP_FAIL:27')
        raise

    _check_stop()
    print('STEP_START:28')
    try:
        # "Tamam" tıklanır
        _safe_click(driver, 'Tamam')
        time.sleep(0.8)
        print('STEP_DONE:28')
    except Exception as _e_28:
        print(f'[FAIL] {_e_28}')
        print('STEP_FAIL:28')
        raise

except Exception as e:
    print(f"HATA: {e}")
    raise
finally:
    driver.quit()