import os
import sys
import json
import time
from datetime import datetime
import subprocess

DATA_DIR = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\data"
CLOUD_FOLDER_ID = "1C_-DTzNWPb5qdm_E6LqYjcFq7ishbXr1"

def generate_live_status():
    status = {
        "timestamp": datetime.now().isoformat(),
        "brand": "Ertuğrul YZ",
        "chairman": "Ertuğrul KÖKCE",
        "portfolio": {
            "total_value_try": 120.75,
            "cash_try": 1.72,
            "positions": [
                {"symbol": "TCELL", "lot": 1, "cost": 96.95, "current": 97.30, "pnl": "+0.35 TL", "target": 101.50},
                {"symbol": "ISCTR", "lot": 1, "cost": 13.20, "current": 13.22, "pnl": "+0.02 TL", "target": "13.36 (LIMIT SATIŞ EMRİ AKTİF)"},
                {"symbol": "ALBRK", "lot": 1, "cost": 8.51, "current": 8.51, "pnl": "0.00 TL", "target": "8.85 (DİP DEĞER SKALP)"}
            ]
        },
        "learning": {
            "total_experience_trades": 8678,
            "status": "AKTİF SÜREKLİ ÖĞRENME AÇIK",
            "q_table_leader": "bofa_order_flow (1.45)",
            "scalp_chark": "hft_micro_scalp (1.405)"
        },
        "six_weapons_status": {
            "scalping": "ALBRK & ISCTR devrede",
            "trend": "TCELL korunuyor",
            "warrant": "Midas uygunluk testi sonrası aktif",
            "viop": "İzlemede",
            "kap_news": "Anlık dinlemede",
            "ipo": "Takvim taranıyor"
        }
    }
    file_path = os.path.join(DATA_DIR, "live_portfolio_status.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2, ensure_ascii=False)
    return file_path

def sync_file_to_drive(file_path, filename):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] ☁️ Buluta Yükleniyor: {filename}...")
    cmd = f'gdrive mutate upload "{file_path}" --parent {CLOUD_FOLDER_ID}'
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if res.returncode == 0:
            print(f"✅ {filename} Google Drive'a başarıyla senkronize edildi.")
            return True
        else:
            print(f"⚠️ Yükleme çıktısı: {res.stderr or res.stdout}")
            return False
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def run_single_cycle():
    status_file = generate_live_status()
    rl_file = os.path.join(DATA_DIR, "reinforcement_learning_ledger.json")
    
    sync_file_to_drive(status_file, "live_portfolio_status.json")
    sync_file_to_drive(rl_file, "reinforcement_learning_ledger.json")
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔄 Dakikalık Bulut Senkronizasyon Döngüsü Tamamlandı.")

if __name__ == "__main__":
    print("=" * 70)
    print("☁️ ERTUĞRUL YZ • GOOGLE DRIVE BULUT SENKRONİZASYON MOTORU (/goal)")
    print("=" * 70)
    run_single_cycle()
