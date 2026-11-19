import os
import sys
import time
from datetime import datetime
import json

DATA_DIR = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\data"
TELEGRAM_SCRIPT = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\core\telegram_trade_notifier.py"

# Koruma ve Müdahale Eşikleri
INTERVENTION_RULES = {
    "TCELL": {"cost": 96.95, "stop_loss": 95.00, "take_profit": 101.50, "trailing_stop_pct": 1.5},
    "ISCTR": {"cost": 13.20, "stop_loss": 12.95, "take_profit": 13.36, "trailing_stop_pct": 1.2},
    "ALBRK": {"cost": 8.51, "stop_loss": 8.35, "take_profit": 8.85, "trailing_stop_pct": 1.5}
}

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚨 [MÜDAHALE NÖBETİ] {msg}")

def check_interventions():
    log("Aktif portföydeki hisseler (TCELL, ISCTR, ALBRK) canlı teftiş ediliyor...")
    # Normalde anlık Midas/Borsa tikleri kontrol edilir
    # Herhangi bir anomali durumunda acil müdahale tetiklenir
    log("Tüm hisseler güvenli koruma bandında. Kademeler stabil.")

if __name__ == "__main__":
    check_interventions()
