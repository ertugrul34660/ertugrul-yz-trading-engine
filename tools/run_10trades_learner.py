# -*- coding: utf-8 -*-
import time
import os
import sys
import datetime
import json

BASE_DIR = 'C:/Users/ertug/.gemini/antigravity/scratch/04-Finans-Borsa-ve-Ticaret/ertugrul-yz-alsat-botu'
sys.path.append(BASE_DIR)

from core.batch_trades_learner import update_10_trades, BATCH_FILE

def monitor_10_trades_loop():
    print("=== 10'LU STRATEJİ BENCHMARK VE ÖĞRENME MOTORU İZLEME BAŞLADI ===")
    
    # 30 Dakikalık Karşılaştırmalı Öğrenme Seansı
    duration_seconds = 1800 # 30 Dakika
    start_time = time.time()
    
    while True:
        elapsed = time.time() - start_time
        try:
            batch = update_10_trades()
            mins = int(elapsed // 60)
            secs = int(elapsed % 60)
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Süre: {mins:02d}:{secs:02d}/30:00 | Portföy: {batch['total_portfolio_val_tl']} TL | PnL: {batch['total_pnl_tl']} TL (%{batch['total_pnl_pct']}) | Kazanan: {batch.get('winning_trades_count', 0)} / Kaybeden: {batch.get('losing_trades_count', 0)}")
        except Exception as e:
            print("İzleme hatası:", e)
            
        if elapsed >= duration_seconds:
            print("\n*** 30 DAKİKALIK ÖĞRENME SEANSI TAMAMLANDI! STRATEJİ KARNESİ ÇIKARILIYOR ***")
            batch = update_10_trades()
            batch['status'] = 'COMPLETED'
            with open(BATCH_FILE, 'w', encoding='utf-8') as f:
                json.dump(batch, f, ensure_ascii=False, indent=2)
            break
            
        time.sleep(30) # Her 30 saniyede bir 10 hisseyi anlık güncelle

if __name__ == '__main__':
    monitor_10_trades_loop()
