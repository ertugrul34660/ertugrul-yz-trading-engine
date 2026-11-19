import time
import win32com.client

try:
    shell = win32com.client.Dispatch("WScript.Shell")
    res = shell.AppActivate("Midas Atlas")
    print("Midas Atlas Activate:", res)
    if not res:
        res = shell.AppActivate("Chrome")
        print("Chrome Activate:", res)
    if res:
        time.sleep(0.4)
        shell.SendKeys("{ENTER}")
        print("ENTER BASILDI!")
    else:
        print("Pencere bulunamadi.")
except Exception as e:
    print("Hata:", e)
