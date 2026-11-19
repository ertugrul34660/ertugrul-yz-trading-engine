# -*- coding: utf-8 -*-
import sys
import os
import json
import datetime

BASE_DIR = 'C:/Users/ertug/.gemini/antigravity/scratch/04-Finans-Borsa-ve-Ticaret/ertugrul-yz-alsat-botu'
sys.path.append(BASE_DIR)

DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
SCALP_FILE = os.path.join(DATA_DIR, 'live_scalp_10000tl.json')

def create_scalp_portfolio():
    # 10.000 TL Dağılımı:
    # 1. BIMAS: 12 Lot @ 400.50 TL = 4.806,00 TL (Günün en güçlüsü, +%1.26 primli, RSI 59)
    # 2. THYAO: 15 Lot @ 321.50 TL = 4.822,50 TL (Günün pozitif direnci, +%0.39 primli, RSI 71.8)
    # Nakit Kalan: 10.000 - (4.806,00 + 4.822,50) = 371,50 TL
    
    positions = [
        {
            "symbol": "BIMAS",
            "name": "BİM Birleşik Mağazalar",
            "entry_price": 400.50,
            "lots": 12,
            "invested_tl": 4806.00,
            "target_scalp": 403.50, # +%0.75 hızlı kâr al
            "stop_scalp": 398.00,   # -%0.62 hızlı stop
            "weight_pct": 48.06,
            "rationale": "Günün en yüksek pozitif momentumuna sahip hissesi (+%1.26), RSI 59 sağlıklı yükselişte."
        },
        {
            "symbol": "THYAO",
            "name": "Türk Hava Yolları",
            "entry_price": 321.50,
            "lots": 15,
            "invested_tl": 4822.50,
            "target_scalp": 323.50, # +%0.62 hızlı kâr al
            "stop_scalp": 319.50,   # -%0.62 hızlı stop
            "weight_pct": 48.23,
            "rationale": "Ulaştırma lideri, endekse karşı pozitif ayrışma (+%0.39), güçlü alıcı kademesi."
        }
    ]
    
    port = {
        "strategy": "10-DAKİKALIK HIZLI MOMENTUM SCALPING",
        "start_time_iso": datetime.datetime.now().isoformat(),
        "start_time_str": datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        "duration_minutes": 10,
        "initial_capital_tl": 10000.0,
        "invested_capital_tl": 9628.50,
        "cash_tl": 371.50,
        "current_total_value_tl": 10000.0,
        "pnl_tl": 0.0,
        "pnl_pct": 0.0,
        "positions": positions,
        "status": "RUNNING"
    }
    
    with open(SCALP_FILE, 'w', encoding='utf-8') as f:
        json.dump(port, f, ensure_ascii=False, indent=2)
        
    return port

if __name__ == '__main__':
    p = create_scalp_portfolio()
    print("10.000 TL Scalp Portföyü Başlatıldı:")
    print("Yatırım:", p['invested_capital_tl'], "TL | Nakit:", p['cash_tl'], "TL")
