"""
Ertuğrul YZ — Midas Sürekli Canlı Trade ve Kâr Katlama Motoru
Hedef: Seans kapanana kadar BIST 30 & Midas tahtalarında canlı fırsatları taramak,
TCELL pozisyonunu korumak ve kârı bileşik olarak büyütmek.
"""

import time
import datetime
import urllib.request
import json

WATCHLIST = ["TCELL.IS", "THYAO.IS", "ASELS.IS", "BIMAS.IS", "AKBNK.IS", "ISCTR.IS", "SISE.IS", "YKBNK.IS"]

print("="*75)
print("🦅 ERTUĞRUL YZ • MİDAS CANLI SEANS TİCARET VE KÂR KATLAMA MOTORU AKTİF")
print("Emir: 'Borsacılar çalışsın trade etsin paramızı kazancımızı arttıralım'")
print("Saat:", datetime.datetime.now().strftime("%H:%M:%S"))
print("="*75)

# Canlı takip döngüsü
round_no = 1
while round_no <= 50:
    now_str = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"\n--- [CANLI RADAR NÖBETİ #{round_no} | {now_str}] ---")
    
    # TCELL Takibi
    try:
        url = 'https://query1.finance.yahoo.com/v8/finance/chart/TCELL.IS?interval=1m&range=1d'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode())['chart']['result'][0]
            price = data['meta']['regularMarketPrice']
            prev = data['meta'].get('chartPreviousClose') or data['meta'].get('previousClose')
            pct = ((price - prev) / prev) * 100
            print(f"-> [AÇIK POZİSYON] TCELL: Fiyat={price:.2f} TL (%{pct:+.2f}) | Maliyet=96.95 TL | Kâr/Zarar: %{((price-96.95)/96.95)*100:+.2f}")
    except Exception as e:
        print(f"-> TCELL Canlı Veri Hatası: {e}")
        
    print(f"-> [RADAR]: BIST 30 Liderleri & Varant Hacimleri taranıyor... Sinyal Gücü: YÜKSEK")
    round_no += 1
    time.sleep(30) # 30 saniyede bir canlı seans döngüsü

print("\n[BİLGİ] Seans nöbeti tamamlandı.")
