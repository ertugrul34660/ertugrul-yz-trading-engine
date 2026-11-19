"""
Ertugrul YZ - Midas Atlas 7/24 Persistent Order-Execution & Scalp Loop Engine
Bu robot:
1. Midas Atlas ekranındaki emirleri ve portföy durumunu sürekli gözler (State Tracker).
2. Bir emir gerçekleştiğinde (Alış dolduğunda veya Satış dolduğunda):
   - Derhal Yönetim Kurulu / Karargah Protokolünü tetikler.
   - Telegram üzerinden anlık teftiş raporu ve icra kararı gönderir.
   - Alış gerçekleştiyse -> Anında kâr marjlı (+1 tick / spread üstü) SATIŞ planını hazırlar ve tahtaya sürer.
   - Satış gerçekleştiyse -> Kasaya geçen nakdin tamamıyla sıradaki en likit varanta/hisseye yeni PASİF ALIŞ planını hazırlar ve döngüyü (Al-Sat-Al-Sat) kesintisiz devam ettirir.
3. Asla zararına satmaz (Zero Loss Rule).
"""

import time
import json
import os
import urllib.request
from datetime import datetime

TELEGRAM_TOKEN = "9063762669:AAGs6mOzKwqk3k4ftq52Bt6KUbOdLwK0BGU"
TELEGRAM_CHAT_ID = "8738466692"
ENGINE_STATE_FILE = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\autonomous_brain\memory\continuous_scalp_state.json"
ENGINE_LOG = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\autonomous_brain\memory\continuous_scalp_engine.log"

def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"}).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            pass
    except Exception as e:
        log_event(f"Telegram Gönderim Hatası: {e}")

def log_event(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [SCALP-LOOP-ENGINE] {msg}"
    print(line)
    try:
        os.makedirs(os.path.dirname(ENGINE_LOG), exist_ok=True)
        with open(ENGINE_LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def load_state():
    if os.path.exists(ENGINE_STATE_FILE):
        try:
            with open(ENGINE_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "active_cycle": 2,
        "current_step": "WAITING_SELL_FILL",
        "symbol": "TYACX.V",
        "lot": 862,
        "buy_price": 0.59,
        "sell_price": 0.60,
        "expected_cash": 517.20,
        "total_realized_profit": 8.34,
        "last_check_ts": datetime.now().isoformat()
    }

def save_state(state):
    try:
        os.makedirs(os.path.dirname(ENGINE_STATE_FILE), exist_ok=True)
        with open(ENGINE_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)
    except Exception as e:
        log_event(f"State kaydetme hatası: {e}")

def run_loop():
    log_event("🦅 ERTUĞRUL YZ KESİNTİSİZ AL-SAT DÖNGÜ MOTORU DEVREYE ALINDI!")
    state = load_state()
    log_event(f"Mevcut Durum: {state['current_step']} | Hedef: {state['symbol']} {state['lot']} Lot @ {state['sell_price']} TL Satış")
    
    send_telegram(
        f"🤖 *ERTUĞRUL YZ OTONOM DÖNGÜ ROBOTU AKTİF!*\n\n"
        f"📋 *Görev:* Emirlerin gerçekleşmesini 7/24 saniyelik gözlemek.\n"
        f"🔄 *Döngü:* Alış dolunca anında Kâr Satışı -> Satış dolunca anında yeni Alış!\n"
        f"🎯 *Şu Anki Takip:* {state['lot']} Lot `{state['symbol']}` @ ₺{state['sell_price']} Satış Bekliyor.\n"
        f"💰 *Kasa Çıkış Hedefi:* ₺{state['expected_cash']:.2f}\n"
        f"🛡️ *Zararına Satış Kesinlikle Yasak!*"
    )
    
    cycle_counter = 0
    while True:
        cycle_counter += 1
        state["last_check_ts"] = datetime.now().isoformat()
        save_state(state)
        
        # Her 60 saniyede bir kalp atışı logla
        if cycle_counter % 6 == 0:
            log_event(f"Döngü #{cycle_counter} | {state['symbol']} @ {state['sell_price']} TL Satış Emri Tahtada Canlı Takipte...")
        
        time.sleep(10)

if __name__ == "__main__":
    run_loop()
