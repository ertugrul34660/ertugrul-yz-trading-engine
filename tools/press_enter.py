import time
import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32

def press_enter_on_midas():
    # Chrome pencerelerini tara
    def enum_windows_callback(hwnd, extra):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                title = buff.value
                if "Midas" in title or "Chrome" in title:
                    extra.append((hwnd, title))
        return True

    windows = []
    cb = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, ctypes.c_void_p)(enum_windows_callback)
    user32.EnumWindows(cb, ctypes.byref(ctypes.py_object(windows)))
    
    print("Bulunan Uygun Pencereler:", windows)
    if not windows:
        print("Midas veya Chrome penceresi bulunamadi.")
        return False

    target_hwnd, target_title = windows[0]
    print(f"Hedef Pencere: {target_title} (HWND: {target_hwnd})")
    
    # Pencereyi one getir
    user32.ShowWindow(target_hwnd, 9) # SW_RESTORE
    user32.SetForegroundWindow(target_hwnd)
    time.sleep(0.5)
    
    # VK_RETURN = 0x0D (Enter tusu)
    VK_RETURN = 0x0D
    KEYEVENTF_KEYUP = 0x0002
    
    user32.keybd_event(VK_RETURN, 0, 0, 0)
    time.sleep(0.1)
    user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0)
    print("ENTER tusu basariyla gonderildi!")
    return True

if __name__ == "__main__":
    press_enter_on_midas()
