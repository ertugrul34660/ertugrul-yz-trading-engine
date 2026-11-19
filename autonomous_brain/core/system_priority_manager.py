"""
Ertugrul YZ - System Hardware & OS High Priority Manager
Bu arac:
1. Tum borsa robotlarinin (autonomous_brain) ve Chrome tarayicisinin islem onceligini (Process Priority)
   isletim sistemi seviyesinde en yuksege (High / AboveNormal) ceker.
2. Islemci (CPU), Bellek (RAM) ve Ag (Network) kaynaklarinda bu projeye MUTLAK ONCELIK tanir.
3. Arka planda donma, gecikme veya diger uygulamalarin sistemi yavaslatmasini engeller.
"""

import psutil
import os
import sys
from datetime import datetime

LOG_FILE = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\autonomous_brain\memory\priority_optimizer.log"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [PRIORITY-OPTIMIZER] {msg}"
    print(line)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def elevate_priorities():
    elevated_count = 0
    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmd = " ".join(p.info['cmdline'] or [])
            name = (p.info['name'] or "").lower()
            
            # Robotlarimiz
            if "autonomous_brain" in cmd:
                p.nice(psutil.HIGH_PRIORITY_CLASS)
                log(f"⚡ Robot PID {p.pid} önceliği YÜKSEK (HIGH) yapıldı.")
                elevated_count += 1
            # Midas Atlas Chrome islemleri
            elif "chrome" in name and any("midas" in arg.lower() or "atlas" in arg.lower() for arg in (p.info['cmdline'] or [])):
                p.nice(psutil.ABOVE_NORMAL_PRIORITY_CLASS)
                log(f"🌐 Midas Atlas Chrome PID {p.pid} önceliği NORMAL ÜSTÜ yapıldı.")
                elevated_count += 1
        except Exception:
            continue
            
    log(f"✅ Toplam {elevated_count} kritik ticaret süreci Windows işletim sisteminde en yüksek önceliğe alındı.")

if __name__ == "__main__":
    elevate_priorities()
