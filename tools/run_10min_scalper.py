# -*- coding: utf-8 -*-
import time
import os
import sys
import datetime
import json
import urllib.request

BASE_DIR = 'C:/Users/ertug/.gemini/antigravity/scratch/04-Finans-Borsa-ve-Ticaret/ertugrul-yz-alsat-botu'
sys.path.append(BASE_DIR)

from core.scalp_manager import SCALP_FILE
from core.analyzer import analyze_stock

def run_scalp_tracker():
    print("=== 10 DAKİKALIK HIZLI SCALPING BOTU AKTİF EDİLDİ ===")
    start_time = time.time()
    duration_seconds = 600 # 10 Dakika
    check_interval = 20 # Her 20 saniyede bir kontrol et
    
    while True:
        elapsed = time.time() - start_time
        
        try:
            with open(SCALP_FILE, 'r', encoding='utf-8') as f:
                port = json.load(f)
                
            total_val = port['cash_tl']
            for pos in port['positions']:
                sym = pos['symbol']
                d = analyze_stock(sym)
                cur_p = float(d.get('current_price') or pos['entry_price'])
                pos['current_price'] = cur_p
                pos['current_val_tl'] = round(cur_p * pos['lots'], 2)
                pos['pos_pnl_tl'] = round(pos['current_val_tl'] - pos['invested_tl'], 2)
                pos['pos_pnl_pct'] = round((pos['pos_pnl_tl'] / pos['invested_tl']) * 100, 2)
                total_val += pos['current_val_tl']
                
            port['current_total_value_tl'] = round(total_val, 2)
            port['pnl_tl'] = round(total_val - port['initial_capital_tl'], 2)
            port['pnl_pct'] = round((port['pnl_tl'] / port['initial_capital_tl']) * 100, 2)
            port['last_update_str'] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            
            with open(SCALP_FILE, 'w', encoding='utf-8') as f:
                json.dump(port, f, ensure_ascii=False, indent=2)
                
            mins = int(elapsed // 60)
            secs = int(elapsed % 60)
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Süre: {mins:02d}:{secs:02d}/10:00 | Portföy: {port['current_total_value_tl']} TL | PnL: {port['pnl_tl']} TL (%{port['pnl_pct']})")
        except Exception as e:
            print("Scalp hata:", e)
            
        if elapsed >= duration_seconds:
            print("\n*** 10 DAKİKA DOLDU! SCALPING POZİSYONLARI KAPATILIYOR ***")
            with open(SCALP_FILE, 'r', encoding='utf-8') as f:
                port = json.load(f)
            port['status'] = 'COMPLETED'
            port['completed_at'] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            with open(SCALP_FILE, 'w', encoding='utf-8') as f:
                json.dump(port, f, ensure_ascii=False, indent=2)
            print(f"Nihai Scalping Sonucu: 10.000 TL -> {port['current_total_value_tl']} TL | Net Kâr/Zarar: {port['pnl_tl']} TL (%{port['pnl_pct']})")
            break
            
        time.sleep(check_interval)

if __name__ == '__main__':
    run_scalp_tracker()
