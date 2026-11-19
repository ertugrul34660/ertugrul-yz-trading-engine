# -*- coding: utf-8 -*-
import sys
import os
import json

BASE_DIR = 'C:/Users/ertug/.gemini/antigravity/scratch/04-Finans-Borsa-ve-Ticaret/ertugrul-yz-alsat-botu'
sys.path.append(BASE_DIR)

from core.scalp_manager import SCALP_FILE

with open(SCALP_FILE, 'r', encoding='utf-8') as f:
    p = json.load(f)

p['status'] = 'COMPLETED'
p['completed_at'] = '16.11.2026 11:34:25'

with open(SCALP_FILE, 'w', encoding='utf-8') as f:
    json.dump(p, f, ensure_ascii=False, indent=2)

print("=== 10 DAKIKALIK SCALPING FINAL RAPORU ===")
print("Baslangic Sermayesi:", p['initial_capital_tl'], "TL")
print("Yatirim Tutari:", p['invested_capital_tl'], "TL")
print("Nakit Kalan:", p['cash_tl'], "TL")
print("Nihai Portfoy Degeri:", p['current_total_value_tl'], "TL")
print("Net Kar / Kazanc:", f"+{p['pnl_tl']}", "TL", f"(+%{p['pnl_pct']})")
print("\nPozisyonlar:")
for pos in p['positions']:
    print(f"  {pos['symbol']}: {pos['lots']} Lot @ {pos['entry_price']} TL -> Son: {pos['current_price']} TL | Deger: {pos['current_val_tl']} TL | Net: +{pos['pos_pnl_tl']} TL (+%{pos['pos_pnl_pct']})")
