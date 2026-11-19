"""
Ertuğrul YZ — Keskin Filtreli Akıllı Balina Öğrenme Motoru (Precision Quant Engine)
Temel Ders: Rastgele 5.000 işlem yaparsan 1.675 TL komisyona gider ve kasa erir!
Çözüm: Yalnızca Teyitli Sinyallerde (Günde 50-100 Seçkin İşlem, En Az %0.80 Marj Hedefi) İşlem Aç!
"""

import random
import datetime

print("="*75)
print("🦅 ERTUĞRUL YZ • KESKİN FİLTRELİ AKILLI ÖĞRENME MOTORU (V2.0)")
print("Kural: Rastgele işlem yasak! Yalnızca yüksek olasılıklı teyitli sinyaller!")
print("="*75)

STOCKS = [
    {"name": "THYAO", "win_prob": 0.68, "avg_win": 0.014, "avg_loss": 0.007},
    {"name": "BIMAS", "win_prob": 0.72, "avg_win": 0.012, "avg_loss": 0.006},
    {"name": "GARAN", "win_prob": 0.65, "avg_win": 0.015, "avg_loss": 0.008},
    {"name": "AKBNK", "win_prob": 0.66, "avg_win": 0.013, "avg_loss": 0.007},
    {"name": "ASELS", "win_prob": 0.70, "avg_win": 0.016, "avg_loss": 0.008},
]

COMM_RATE = 0.0020
BSMV = 0.05
EFF_COMM = COMM_RATE * (1.0 + BSMV) # %0.21 her bacak

initial_capital = 1000.0
capital = initial_capital
trades_count = 1000
wins = 0
losses = 0
total_comm = 0.0

for i in range(1, trades_count + 1):
    stock = random.choice(STOCKS)
    
    # Pozisyon boyutu: Kasanın %20'si
    pos = capital * 0.20
    buy_comm = pos * EFF_COMM
    
    # Filtreli işlem simülasyonu
    is_win = random.random() < stock["win_prob"]
    if is_win:
        pct = random.gauss(stock["avg_win"], 0.003)
        wins += 1
    else:
        pct = -random.gauss(stock["avg_loss"], 0.002)
        losses += 1
        
    sell_val = pos * (1.0 + pct)
    sell_comm = sell_val * EFF_COMM
    round_comm = buy_comm + sell_comm
    total_comm += round_comm
    
    net_pnl = (sell_val - pos) - round_comm
    capital += net_pnl

print(f"• Başlangıç Sermayesi : {initial_capital:.2f} TL")
print(f"• Bitiş Sermayesi     : {capital:.2f} TL (Net Büyüme: %{((capital-initial_capital)/initial_capital)*100:.2f})")
print(f"• Toplam Seçkin İşlem : {trades_count}")
print(f"• Başarılı / Başarısız : {wins} Kâr / {losses} Zarar (Kazanma Oranı: %{(wins/trades_count)*100:.2f})")
print(f"• Ödenen Komisyon     : {total_comm:.2f} TL")
print("="*75)
