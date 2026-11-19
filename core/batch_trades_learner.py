# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • 10 Farklı Strateji & 10 Bağımsız İşlem Simülasyon Laboratuvarı
Toplam Sermaye: 100.000 TL (10 İşlem x 10.000 TL)
Amaç: Her bir stratejinin (Momentum, Dip Dönüşü, BofA Takası, Bilanço, Breakout vb.)
başarı oranını ölçmek, en karlı modelleri tespit edip sisteme öğretmek.
"""

import sys
import os
import json
import datetime
import time

BASE_DIR = 'C:/Users/ertug/.gemini/antigravity/scratch/04-Finans-Borsa-ve-Ticaret/ertugrul-yz-alsat-botu'
sys.path.append(BASE_DIR)

from core.analyzer import analyze_stock

DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
BATCH_FILE = os.path.join(DATA_DIR, 'batch_10_trades_learning.json')

def setup_10_trades():
    # 10 Farklı Hissede 10 Farklı Hipotez / Strateji
    trade_definitions = [
        {"id": 1, "symbol": "BIMAS", "strategy": "Pozitif Momentum & Güçlü Trend", "rationale": "Günün en yüksek pozitif ayrışması, RSI 59 sağlıklı boğa bandı."},
        {"id": 2, "symbol": "THYAO", "strategy": "BofA Kurumsal Akıllı Para + Döviz Kalkanı", "rationale": "BofA net alıcı, 118 Milyar TL net kâr, endeks üstü getiri."},
        {"id": 3, "symbol": "GARAN", "strategy": "Dip Tepki & Bankacılık Toparlanması", "rationale": "Sabahki kâr satışından sonra destek seviyesinden seans içi dönüş."},
        {"id": 4, "symbol": "ASELS", "strategy": "Savunma Sanayii & Güçlü Sipariş Katalizörü", "rationale": "KAP duyarlılığı yüksek, RSI 49 nötr bölgeden yukarı kıvrılma."},
        {"id": 5, "symbol": "TUPRS", "strategy": "Yüksek Temettü & Rafineri Marjı Desteği", "rationale": "Düşük F/K, güçlü nakit yaratımı, pivot PP üzerinde tutunma."},
        {"id": 6, "symbol": "KCHOL", "strategy": "Holding İskontosu & Net Aktif Değer", "rationale": "Net aktif değerine göre %35 iskontolu, BofA takas girişi."},
        {"id": 7, "symbol": "ISCTR", "strategy": "Hacim Patlaması & Likidite Lideri", "rationale": "BIST'in en yüksek hacimli hisselerinden biri, ucuz çarpanlar."},
        {"id": 8, "symbol": "AKBNK", "strategy": "Özsermaye Kârlılığı & Yabancı İlgisi", "rationale": "Bankacılık ralli adayı, yüksek sermaye yeterlilik rasyosu."},
        {"id": 9, "symbol": "EREGL", "strategy": "Emtia / Çelik Döngüsel Dip Dönüşü", "rationale": "Aşırı satım bölgesinden tepki, uzun vadeli ucuzluk bölgesi."},
        {"id": 10, "symbol": "SISE", "strategy": "İhracat & Global Cam Şişe Lideri", "rationale": "Döviz fazlası pozisyonu, 200 günlük hareketli ortalama desteği."}
    ]
    
    trades = []
    print("=== 10 İŞLEM x 10.000 TL = 100.000 TL ÖĞRENME LABORATUVARI KURULUYOR ===")
    
    total_invested = 0.0
    total_cash = 0.0
    
    for td in trade_definitions:
        sym = td['symbol']
        d = analyze_stock(sym)
        price = float(d.get('current_price') or 100.0)
        
        # 10.000 TL'lik alım hesaplama
        lots = int(10000.0 // price)
        if lots == 0: lots = 1
        invested = round(lots * price, 2)
        cash_left = round(10000.0 - invested, 2)
        
        total_invested += invested
        total_cash += cash_left
        
        trade_item = {
            "trade_id": td['id'],
            "symbol": sym,
            "strategy_name": td['strategy'],
            "rationale": td['rationale'],
            "entry_price": price,
            "lots": lots,
            "invested_tl": invested,
            "cash_tl": cash_left,
            "target_price": round(price * 1.015, 2), # %1.5 Hedef
            "stop_price": round(price * 0.985, 2),   # %1.5 Stop
            "current_price": price,
            "current_val_tl": invested,
            "pnl_tl": 0.0,
            "pnl_pct": 0.0,
            "status": "OPEN",
            "entry_time": datetime.datetime.now().strftime("%H:%M:%S")
        }
        trades.append(trade_item)
        print(f"İşlem #{td['id']:02d}: {sym:<6} | {lots:>4} Lot @ {price:>6.2f} TL | Tutar: {invested:>8.2f} TL | Strateji: {td['strategy']}")

    batch_data = {
        "title": "Ertuğrul YZ 10'lu Öğrenme ve Model Benchmark Laboratuvarı",
        "created_at": datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        "total_budget_tl": 100000.0,
        "total_invested_tl": round(total_invested, 2),
        "total_cash_reserve_tl": round(total_cash, 2),
        "total_portfolio_val_tl": 100000.0,
        "total_pnl_tl": 0.0,
        "total_pnl_pct": 0.0,
        "trades": trades
    }
    
    with open(BATCH_FILE, 'w', encoding='utf-8') as f:
        json.dump(batch_data, f, ensure_ascii=False, indent=2)
        
    return batch_data

def update_10_trades():
    if not os.path.exists(BATCH_FILE):
        return setup_10_trades()
        
    with open(BATCH_FILE, 'r', encoding='utf-8') as f:
        batch = json.load(f)
        
    total_val = batch['total_cash_reserve_tl']
    winning_trades = 0
    losing_trades = 0
    
    for t in batch['trades']:
        sym = t['symbol']
        d = analyze_stock(sym)
        cur_p = float(d.get('current_price') or t['entry_price'])
        t['current_price'] = cur_p
        t['current_val_tl'] = round(cur_p * t['lots'], 2)
        t['pnl_tl'] = round(t['current_val_tl'] - t['invested_tl'], 2)
        t['pnl_pct'] = round((t['pnl_tl'] / t['invested_tl']) * 100, 2)
        total_val += t['current_val_tl']
        
        if t['pnl_tl'] > 0: winning_trades += 1
        elif t['pnl_tl'] < 0: losing_trades += 1
        
    batch['total_portfolio_val_tl'] = round(total_val, 2)
    batch['total_pnl_tl'] = round(total_val - batch['total_budget_tl'], 2)
    batch['total_pnl_pct'] = round((batch['total_pnl_tl'] / batch['total_budget_tl']) * 100, 2)
    batch['winning_trades_count'] = winning_trades
    batch['losing_trades_count'] = losing_trades
    batch['last_update'] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    
    with open(BATCH_FILE, 'w', encoding='utf-8') as f:
        json.dump(batch, f, ensure_ascii=False, indent=2)
        
    return batch

if __name__ == '__main__':
    b = setup_10_trades()
    print(f"\nToplam Bütçe: {b['total_budget_tl']} TL | Yatırılan: {b['total_invested_tl']} TL | Rezerv Nakit: {b['total_cash_reserve_tl']} TL")
