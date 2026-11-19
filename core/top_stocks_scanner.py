# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • En Yüksek Kâr Potansiyelli 5 Hisse Radarı (Top 5 Profit Scanner)
Borsa İstanbul'daki güçlü hisseleri tarar, BofA takası ve kâr marjına göre
en karlı 5 hisseyi seçerek önbelleğe alır.
"""

import json
import os
import sys
import time
import concurrent.futures

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core.analyzer import analyze_stock

CACHE_FILE = os.path.join(BASE_DIR, "learning", "top5_stocks.json")

# Taranacak Gözde ve Hacimli BIST Havuzu
SCAN_POOL = [
    "TUPRS", "THYAO", "KCHOL", "SAHOL", "FROTO", 
    "ASELS", "BIMAS", "AKBNK", "GARAN", "SISE", 
    "TOASO", "ENKAI", "ASTOR", "MIATK", "PGSUS"
]

def _analyze_single(sym):
    try:
        res = analyze_stock(sym)
        if res.get("success"):
            action = res.get("action")
            score_val = float(res.get("score", "0"))
            profit_str = res.get("profit_badge", "%0")
            profit_num = 0.0
            try:
                clean_pct = profit_str.replace("+%", "").replace("-%", "").replace("%", "").split()[0]
                profit_num = float(clean_pct)
            except Exception:
                profit_num = 0.0
                
            return {
                "symbol": res.get("symbol"),
                "action": action,
                "action_class": res.get("action_class"),
                "badge_text": res.get("badge_text"),
                "current_price": f"{res.get('current_price')} {res.get('currency')}",
                "suggested_entry": res.get("suggested_entry"),
                "target_price": res.get("target_price"),
                "profit_badge": res.get("profit_badge"),
                "profit_num": profit_num,
                "stop_loss": res.get("stop_loss"),
                "bofa_action": res.get("bofa_action"),
                "confidence": res.get("confidence"),
                "score_val": score_val
            }
    except Exception:
        pass
    return None

def get_top5_profitable_stocks(force_refresh=False):
    # Önbellek kontrolü (1 saatlik geçerlilik)
    if not force_refresh and os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if time.time() - data.get("timestamp", 0) < 3600:
                    return data.get("stocks", [])
        except Exception:
            pass

    scored = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(_analyze_single, SCAN_POOL)
        for r in results:
            if r:
                scored.append(r)

    # Sıralama: Önce AL olanlar, sonra en yüksek puan ve en yüksek % kâr
    scored.sort(key=lambda x: (
        2 if x["action"] == "AL" else (1 if x["action"] == "KARIŞMA" else 0),
        x["score_val"],
        x["profit_num"]
    ), reverse=True)

    top5 = scored[:5]

    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": time.time(),
                "stocks": top5
            }, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

    return top5

if __name__ == "__main__":
    top = get_top5_profitable_stocks(force_refresh=True)
    for idx, s in enumerate(top, 1):
        print(f"{idx}. {s['symbol']} | {s['action']} | Giriş: {s['suggested_entry']} | Hedef: {s['target_price']} | Kâr: {s['profit_badge']}")
