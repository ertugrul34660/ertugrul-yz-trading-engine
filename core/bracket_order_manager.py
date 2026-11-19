import os
import sys
import json
from datetime import datetime

DATA_DIR = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\data"

class BracketOrderManager:
    """
    Her alım işleminde eşzamanlı olarak:
    1. Giriş Fiyatı (ENTRY)
    2. Kâr Al Emri (TAKE PROFIT - TP)
    3. Zarar Durdur / Stop Emri (STOP LOSS - SL)
    oranlarını ve fiyatlarını hesaplayıp piyasaya paket olarak bağlar.
    """
    DEFAULT_TP_PCT = 2.0  # +%2.0 Kâr Al
    DEFAULT_SL_PCT = 1.5  # -%1.5 Zarar Durdur

    @classmethod
    def calculate_bracket(cls, symbol, buy_price, tp_pct=None, sl_pct=None):
        tp_ratio = (tp_pct or cls.DEFAULT_TP_PCT) / 100.0
        sl_ratio = (sl_pct or cls.DEFAULT_SL_PCT) / 100.0
        
        tp_price = round(buy_price * (1.0 + tp_ratio), 2)
        sl_price = round(buy_price * (1.0 - sl_ratio), 2)
        
        bracket = {
            "symbol": symbol,
            "buy_price": buy_price,
            "take_profit_price": tp_price,
            "take_profit_pct": f"+{tp_pct or cls.DEFAULT_TP_PCT}%",
            "stop_loss_price": sl_price,
            "stop_loss_pct": f"-{sl_pct or cls.DEFAULT_SL_PCT}%",
            "status": "ARMED_AND_WATCHED",
            "timestamp": datetime.now().isoformat()
        }
        return bracket

    @classmethod
    def arm_active_positions(cls):
        # Mevcut aktif pozisyonlarımızın Bracket paketleri:
        positions = [
            ("TCELL", 96.95, 4.5, 2.0),   # 101.30 TP, 95.00 SL
            ("ISCTR", 13.20, 1.2, 1.5),   # 13.36 TP (Emir Borsada), 13.00 SL
            ("ALBRK", 8.51, 4.0, 1.8)     # 8.85 TP, 8.35 SL
        ]
        brackets = {}
        for sym, price, tp, sl in positions:
            brackets[sym] = cls.calculate_bracket(sym, price, tp, sl)
        
        file_path = os.path.join(DATA_DIR, "bracket_orders_active.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(brackets, f, indent=2, ensure_ascii=False)
        print("✅ Tüm aktif hisseler için eşzamanlı TP ve SL koruma zırhı bağlandı.")
        return brackets

if __name__ == "__main__":
    b = BracketOrderManager.arm_active_positions()
    for k, v in b.items():
        print(f"🎯 {k} -> Alış: {v['buy_price']} ₺ | TP (Kâr Al): {v['take_profit_price']} ₺ ({v['take_profit_pct']}) | SL (Stop): {v['stop_loss_price']} ₺ ({v['stop_loss_pct']})")
