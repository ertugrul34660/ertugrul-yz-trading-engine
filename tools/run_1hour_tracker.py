# -*- coding: utf-8 -*-
import time
import os
import sys
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core.portfolio_manager import update_portfolio

def run_tracker():
    print("=== ERTUĞRUL YZ • 1 SAATLİK YATIRIM İZLEME BOTU BAŞLATILDI ===")
    start_time = time.time()
    duration_seconds = 3600 # 1 Saat (60 dakika)
    check_interval = 60 # Her 60 saniyede bir fiyatları güncelle
    
    while True:
        elapsed = time.time() - start_time
        remaining = duration_seconds - elapsed
        
        try:
            port = update_portfolio()
            mins_elapsed = int(elapsed // 60)
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Geçen Süre: {mins_elapsed}/60 dk | Portföy: {port['current_total_value_tl']} TL | PnL: {port['pnl_tl']} TL (%{port['pnl_pct']})")
        except Exception as e:
            print("İzleme hatası:", e)
            
        if elapsed >= duration_seconds:
            print("\n*** 1 SAAT TAMAMLANDI! NİHAİ RAPOR OLUŞTURULUYOR ***")
            port = update_portfolio()
            port['status'] = 'COMPLETED'
            port['end_time_str'] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            from core.portfolio_manager import PORTFOLIO_FILE
            import json
            with open(PORTFOLIO_FILE, 'w', encoding='utf-8') as f:
                json.dump(port, f, ensure_ascii=False, indent=2)
            print(f"Nihai Sonuç: Sermaye: 1000 TL -> Son Değer: {port['current_total_value_tl']} TL | Net Kâr/Zarar: {port['pnl_tl']} TL (%{port['pnl_pct']})")
            break
            
        time.sleep(check_interval)

if __name__ == '__main__':
    run_tracker()
