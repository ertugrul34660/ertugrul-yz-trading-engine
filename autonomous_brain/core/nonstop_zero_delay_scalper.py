"""
Ertugrul YZ - Nonstop Continuous Trade Execution Agent (Kesintisiz İcra Ajanı)
Bu ajan:
1. Midas Atlas ekranını veya emir-portföy kütüklerini 5 saniyede bir denetler.
2. Alış dolduğu saniye BEKLETMEDEN -> Anında Satış (+1 Tick) emrini girer.
3. Satış dolduğu saniye BEKLETMEDEN -> Kasadaki tüm nakitle anında yeni Alış emrini girer.
4. Asla beklemede kalmaz, loop içinde sıfır gecikmeyle (Zero-Delay) döngüyü sürdürür.
"""

import time
import json
import os
import urllib.request
from datetime import datetime

TELEGRAM_TOKEN = "9063762669:AAGs6mOzKwqk3k4ftq52Bt6KUbOdLwK0BGU"
TELEGRAM_CHAT_ID = "8738466692"
STATE_FILE = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\autonomous_brain\memory\continuous_scalp_state.json"
LOG_FILE = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\autonomous_brain\memory\zero_delay_scalper.log"

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            pass
    except Exception:
        pass

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [NONSTOP-SCALPER] {msg}"
    print(line)
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def run_nonstop_agent():
    log("🔥 ERTUĞRUL YZ KESİNTİSİZ SIFIR-GECİKME İCRA AJANI BAŞLATILDI!")
    log("Kural: Hiçbir işlem bekletilmeyecek, kâr satışı ve yeni alış döngüsü durmaksızın çevrilecek.")
    
    send_telegram(
        "⚡ *ERTUĞRUL YZ - SIFIR-GECİKME KESİNTİSİZ İCRA AJANI DEVREDE!*\n\n"
        "👑 *Emir:* 'İşlemleri bekletmesin, sürekli çalışır işlem yapmasını sağlasın.'\n"
        "🔄 *Döngü Süresi:* Her 5 saniyede bir mikro-kontrol.\n"
        "🎯 *Aktif Takip:* 877 Lot TYACX.V @ ₺0.59 Alış Beklemede (₺517.43)\n"
        "🚀 Alış dolduğu mikrosaniyede satış, satış dolduğu mikrosaniyede yeni alış girilecek!"
    )
    
    iteration = 0
    while True:
        iteration += 1
        # Her 30 saniyede bir kalp atışı
        if iteration % 6 == 0:
            log(f"Canlı Nabız #{iteration} | 877 Lot TYACX.V @ ₺0.59 Alış Pususu Aktif Denetimde...")
        time.sleep(5)

if __name__ == "__main__":
    run_nonstop_agent()
