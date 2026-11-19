# -*- coding: utf-8 -*-
import sys
import os
import json

BASE_DIR = 'C:/Users/ertug/.gemini/antigravity/scratch/04-Finans-Borsa-ve-Ticaret/ertugrul-yz-alsat-botu'
sys.path.append(BASE_DIR)

from core.portfolio_manager import update_portfolio, PORTFOLIO_FILE

p = update_portfolio()
p['status'] = 'COMPLETED'
p['completed_at'] = '16.11.2026 11:20:00'

with open(PORTFOLIO_FILE, 'w', encoding='utf-8') as f:
    json.dump(p, f, ensure_ascii=False, indent=2)

print("=== 1 SAATLIK PORTFOY FINAL RAPORU ===")
print("Baslangic Sermayesi:", p['initial_capital_tl'], "TL")
print("Yatirim Tutari:", p['invested_capital_tl'], "TL")
print("Nakit Kalan:", p['cash_tl'], "TL")
print("Son Portfoy Degeri:", p['current_total_value_tl'], "TL")
print("Net Kar / Zarar:", p['pnl_tl'], "TL", f"(%{p['pnl_pct']})")
print("\nPozisyonlar:")
for pos in p['positions']:
    print(f"  {pos['symbol']}: {pos['lots']} Lot @ {pos['entry_price']} TL -> Son: {pos['current_price']} TL | Deger: {pos['current_val_tl']} TL | Net: {pos['pos_pnl_tl']} TL (%{pos['pos_pnl_pct']})")
