# -*- coding: utf-8 -*-
import sys
import os

BASE_DIR = 'C:/Users/ertug/.gemini/antigravity/scratch/04-Finans-Borsa-ve-Ticaret/ertugrul-yz-alsat-botu'
sys.path.append(BASE_DIR)

from core.analyzer import analyze_stock

symbols = ['THYAO', 'GARAN', 'BIMAS', 'ASELS', 'KCHOL', 'TUPRS', 'ISCTR', 'AKBNK', 'EREGL', 'SISE', 'SAHOL', 'YKBNK']
results = []

for s in symbols:
    d = analyze_stock(s)
    p = float(d.get('current_price') or 0)
    chg = float(d.get('change_pct') or 0)
    rsi = float(d.get('rsi') or 50)
    vol = d.get('volume_surge', 'Normal')
    bofa = d.get('bofa_action', 'Nötr')
    act = d.get('action', 'BEKLE')
    
    score = 0
    if chg > 0: score += 40
    if act == 'AL': score += 20
    if 50 <= rsi <= 72: score += 20
    if 'ALIM' in bofa.upper() or 'SMART' in bofa.upper(): score += 20
    
    results.append({
        'symbol': s,
        'price': p,
        'change': chg,
        'rsi': rsi,
        'action': act,
        'bofa': bofa[:20],
        'score': score
    })

results.sort(key=lambda x: x['score'], reverse=True)
print("=== YENI TEST: SAAT 12:20 ANLIK BIST MOMENTUM TARAMASI ===")
for r in results:
    print(f"{r['symbol']:<6} | Fiyat: {r['price']:>6.2f} TL | Degisim: %{r['change']:>5.2f} | RSI: {r['rsi']:>4.1f} | Karar: {r['action']:<4} | Skor: {r['score']}")
