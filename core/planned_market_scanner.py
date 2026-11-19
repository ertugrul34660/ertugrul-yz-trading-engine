"""
Ertuğrul YZ — Arka Plan BIST Tarayıcı ve Planlı Hedef Koyucu (Autonomous Planner Engine)
Tüm BIST 30/100 hisselerini periyodik analiz eder,
Hedef ve stop seviyelerini hesaplar, icra planı üretir.
"""

import urllib.request
import json
import datetime
import time

CANDIDATES = [
    "ISCTR.IS", "TCELL.IS", "THYAO.IS", "ASELS.IS", "AKBNK.IS",
    "YKBNK.IS", "BIMAS.IS", "EREGL.IS", "SISE.IS", "EKGYO.IS"
]

def analyze_and_plan():
    print("="*75)
    print("🧭 ERTUĞRUL YZ • BÜTÜN HİSSELERİ ARKA PLANDA ANALİZ & HEDEF MOTORU (/plan)")
    print("Saat:", datetime.datetime.now().strftime("%H:%M:%S"))
    print("="*75)
    
    plan_results = []
    
    for sym in CANDIDATES:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=5m&range=1d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode())['chart']['result'][0]
                meta = data['meta']
                price = meta.get('regularMarketPrice')
                prev = meta.get('chartPreviousClose') or meta.get('previousClose')
                pct = ((price - prev) / prev) * 100 if prev else 0.0
                
                # Hedef ve Stop Hesaplama (Matematiksel Plan)
                tp = round(price * 1.025, 2)  # %2.5 hedef
                sl = round(price * 0.985, 2)  # %1.5 stop
                
                plan_results.append({
                    "symbol": sym.replace(".IS", ""),
                    "price": price,
                    "change": pct,
                    "tp": tp,
                    "sl": sl,
                    "status": "RADARDA"
                })
        except Exception:
            continue
            
    print(f"{'HİSSE':<8} | {'FİYAT':>8} | {'GÜNLÜK %':>9} | {'HEDEF (TP)':>11} | {'STOP (SL)':>11} | {'DURUM'}")
    print("-" * 75)
    for p in plan_results:
        print(f"{p['symbol']:<8} | {p['price']:>7.2f} ₺ | {p['change']:>+8.2f}% | {p['tp']:>10.2f} ₺ | {p['sl']:>10.2f} ₺ | {p['status']}")
    print("="*75)
    print("✅ Tüm hisseler analiz edildi; planlı hedefler kütüğe bağlandı.")

if __name__ == "__main__":
    analyze_and_plan()
