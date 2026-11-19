import os
import sys
import time
import subprocess
from datetime import datetime

PYTHON_EXE = sys.executable
BASE_DIR = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu"
CLOUD_SYNC_SCRIPT = os.path.join(BASE_DIR, "core", "cloud_sync_daemon.py")
RL_DAEMON_SCRIPT = os.path.join(BASE_DIR, "core", "rl_continuous_daemon.py")

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def run_loop():
    log("🦅 ERTUĞRUL YZ • 7/24 KESİNTİSİZ BULUT & BORSA NÖBETÇİSİ BAŞLATILDI")
    iteration = 0
    while True:
        iteration += 1
        log(f"--- DÖNGÜ #{iteration} BAŞLADI ---")
        try:
            # 1. Pekiştirmeli Öğrenme Motorunu Çalıştır
            subprocess.run([PYTHON_EXE, RL_DAEMON_SCRIPT], capture_output=True, text=True, timeout=30)
            # 2. Google Drive Bulut Senkronizasyonunu Çalıştır
            subprocess.run([PYTHON_EXE, CLOUD_SYNC_SCRIPT], capture_output=True, text=True, timeout=45)
            log("✅ Bulut ve Öğrenme senkronizasyonu tamamlandı.")
        except Exception as e:
            log(f"⚠️ Hata: {e}")
        
        # 60 saniye bekle ve tekrar et (Kesintisiz 7/24 döngü)
        time.sleep(60)

if __name__ == "__main__":
    run_loop()
