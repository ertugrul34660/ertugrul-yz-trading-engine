import urllib.request
import json
import time
import os
import datetime

DATA_DIR = 'C:/Users/ertug/.gemini/antigravity/scratch/04-Finans-Borsa-ve-Ticaret/ertugrul-yz-alsat-botu/data'
os.makedirs(DATA_DIR, exist_ok=True)
PORTFOLIO_FILE = os.path.join(DATA_DIR, 'live_portfolio_1000tl.json')

def create_initial_portfolio():
    # 1.000 TL Sermaye Dağılımı:
    # 1. GARAN: 2 Lot @ 149.80 = 299.60 TL
    # 2. ISCTR: 25 Lot @ 13.44 = 336.00 TL
    # 3. THYAO: 1 Lot @ 321.50 = 321.50 TL
    # Nakit Kalan: 1000 - (299.60 + 336.00 + 321.50) = 42.90 TL
    
    positions = [
        {
            "symbol": "GARAN",
            "name": "Garanti BBVA",
            "entry_price": 149.80,
            "lots": 2,
            "invested_tl": 299.60,
            "target_tp1": 157.00,
            "target_tp2": 164.00,
            "stop_loss": 145.30,
            "weight_pct": 30.0,
            "rationale": "BofA dev alımda, MFI güçlü para girişi pozitif, Bankacılık ralli lideri."
        },
        {
            "symbol": "ISCTR",
            "name": "İş Bankası C",
            "entry_price": 13.44,
            "lots": 25,
            "invested_tl": 336.00,
            "target_tp1": 14.15,
            "target_tp2": 14.80,
            "stop_loss": 13.04,
            "weight_pct": 33.6,
            "rationale": "BofA akıllı para desteği, yüksek işlem hacmi, ucuz çarpanlar."
        },
        {
            "symbol": "THYAO",
            "name": "Türk Hava Yolları",
            "entry_price": 321.50,
            "lots": 1,
            "invested_tl": 321.50,
            "target_tp1": 336.00,
            "target_tp2": 349.00,
            "stop_loss": 311.85,
            "weight_pct": 32.1,
            "rationale": "Döviz kalkanı güçlü, 118 Milyar TL net kâr, BofA net alıcı."
        }
    ]
    
    portfolio = {
        "start_time_iso": datetime.datetime.now().isoformat(),
        "start_time_str": datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        "duration_minutes": 60,
        "initial_capital_tl": 1000.0,
        "invested_capital_tl": 957.10,
        "cash_tl": 42.90,
        "current_total_value_tl": 1000.0,
        "pnl_tl": 0.0,
        "pnl_pct": 0.0,
        "positions": positions,
        "logs": [
            {
                "time": datetime.datetime.now().strftime("%H:%M:%S"),
                "event": "Portföy 1.000 TL ile başlatıldı. GARAN (2 Lot), ISCTR (25 Lot), THYAO (1 Lot) satın alındı."
            }
        ],
        "status": "RUNNING"
    }
    
    with open(PORTFOLIO_FILE, 'w', encoding='utf-8') as f:
        json.dump(portfolio, f, ensure_ascii=False, indent=2)
    print("Portföy oluşturuldu:", PORTFOLIO_FILE)
    return portfolio

def get_current_stock_price(symbol):
    try:
        from core.analyzer import analyze_stock
        data = analyze_stock(symbol)
        if data and data.get('current_price'):
            return float(data.get('current_price'))
    except Exception as e:
        print(f"analyze_stock hatası ({symbol}):", e)
    return None

def update_portfolio():
    if not os.path.exists(PORTFOLIO_FILE):
        create_initial_portfolio()
        
    with open(PORTFOLIO_FILE, 'r', encoding='utf-8') as f:
        port = json.load(f)
        
    total_val = port['cash_tl']
    
    for pos in port['positions']:
        sym = pos['symbol']
        cur_p = get_current_stock_price(sym)
        if cur_p and cur_p > 0:
            pos['current_price'] = cur_p
            pos['current_val_tl'] = round(cur_p * pos['lots'], 2)
            pos['pos_pnl_tl'] = round(pos['current_val_tl'] - pos['invested_tl'], 2)
            pos['pos_pnl_pct'] = round((pos['pos_pnl_tl'] / pos['invested_tl']) * 100, 2)
        else:
            # Fallback
            pos['current_price'] = pos.get('current_price', pos['entry_price'])
            pos['current_val_tl'] = round(pos['current_price'] * pos['lots'], 2)
            pos['pos_pnl_tl'] = round(pos['current_val_tl'] - pos['invested_tl'], 2)
            pos['pos_pnl_pct'] = round((pos['pos_pnl_tl'] / pos['invested_tl']) * 100, 2)
            
        total_val += pos['current_val_tl']
        
    port['current_total_value_tl'] = round(total_val, 2)
    port['pnl_tl'] = round(total_val - port['initial_capital_tl'], 2)
    port['pnl_pct'] = round((port['pnl_tl'] / port['initial_capital_tl']) * 100, 2)
    port['last_update_str'] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    with open(PORTFOLIO_FILE, 'w', encoding='utf-8') as f:
        json.dump(port, f, ensure_ascii=False, indent=2)
        
    return port

if __name__ == '__main__':
    p = create_initial_portfolio()
    p = update_portfolio()
    print("Güncel Portföy Durumu:")
    print(f"Toplam Değer: {p['current_total_value_tl']} TL")
    print(f"Kâr/Zarar: {p['pnl_tl']} TL (%{p['pnl_pct']})")
    for pos in p['positions']:
        print(f"  {pos['symbol']}: {pos['lots']} Lot @ {pos['entry_price']} TL -> Güncel: {pos['current_price']} TL | Net: {pos['pos_pnl_tl']} TL (%{pos['pos_pnl_pct']})")
