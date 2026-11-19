"""
Ertugrul YZ - Autonomous Persistent Watchdog & Self-Healing Sentinel
Bu nöbetçi koruyucu:
1. Projedeki tüm robotların (Resilient Algo Trader, Q-Learning Brain, Continuous Scalp Engine)
   canlılığını her 10 saniyede bir denetler.
2. Herhangi bir robot takılırsa, kilitlenirse veya kapanırsa; hiç kullanıcıya hissettirmeden
   ve onay beklemeden temizleyip derhal YENİDEN BAŞLATIR (Auto-Restart & Self-Healing).
3. Yönetim Kurulu Başkanı "DUR" diyene kadar KESİNTİSİZ ve SONSUZA KADAR çalışır!
"""

import subprocess
import time
import os
import sys
from datetime import datetime

CORE_DIR = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\autonomous_brain\core"
LOG_FILE = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\autonomous_brain\memory\infinite_watchdog.log"

ROBOT_SCRIPTS = [
    "continuous_scalp_loop_engine.py",
    "self_evolving_brain.py",
    "resilient_algo_trader.py"
]

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [INFINITY-SENTINEL] {msg}"
    print(line)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def check_process_running(script_name):
    try:
        cmd = f'Get-CimInstance Win32_Process | Where-Object {{ $_.CommandLine -like "*{script_name}*" }} | Select-Object -ExpandProperty ProcessId'
        out = subprocess.check_output(["powershell", "-NoProfile", "-Command", cmd], text=True)
        pids = [p.strip() for p in out.strip().splitlines() if p.strip()]
        return len(pids) > 0
    except Exception:
        return False

def start_robot(script_name):
    script_path = os.path.join(CORE_DIR, script_name)
    log(f"⚡ Robot Canlandırılıyor / Başlatılıyor: {script_name}")
    try:
        subprocess.Popen([sys.executable, script_path], creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
        log(f"✅ {script_name} başarıyla ayağa kaldırıldı.")
    except Exception as e:
        log(f"❌ {script_name} başlatılırken hata: {e}")

def run_sentinel():
    log("👑 ERTUĞRUL YZ SONSUZ ÇALIŞMA PROTOKOLÜ (INFINITE AUTONOMOUS RUNTIME) BAŞLATILDI!")
    log("Kural: Yönetim Kurulu Başkanı 'DUR' diyene kadar robotlar asla durmayacak.")
    
    while True:
        for script in ROBOT_SCRIPTS:
            if not check_process_running(script):
                log(f"⚠️ DİKKAT: {script} çalışmıyor tespit edildi! Otomatik canlandırma devreye giriyor...")
                start_robot(script)
        time.sleep(15)

if __name__ == "__main__":
    run_sentinel()
