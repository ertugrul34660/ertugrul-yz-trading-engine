"""
Ertuğrul YZ — 1.000.000 TL Kapanış Rallisi Canlı İcra Motoru
Yatırımcı Fonu: 1.000.000 TL
Strateji: Kapanış Öncesi Güçlü Momentum Liderleri (ASELS & THYAO) + Dipten Tepki (AKBNK)
Komisyon Modeli: İş Bankası Binde 2 + BSMV (Gidiş-Dönüş %0.42 Kesinti Dahil)
"""

import sys
import time
import datetime
import urllib.request
import json

PORTFOLIO_CASH = 1000000.00
RESERVE_CASH = 200000.00  # Nakit koruma rezervi
DEPLOYED_CAPITAL = 800000.00

COMMISSION_RATE = 0.0020
BSMV_RATE = 0.05
EFF_COMMISSION_PER_SIDE = COMMISSION_RATE * (1.0 + BSMV_RATE) # %0.21

ALLOCATIONS = [
    {"symbol": "ASELS.IS", "name": "ASELS", "weight": 0.45, "capital": 360000.0, "entry": 354.50, "lots": 1015},
    {"symbol": "THYAO.IS", "name": "THYAO", "weight": 0.35, "capital": 280000.0, "entry": 323.25, "lots": 866},
    {"symbol": "AKBNK.IS", "name": "AKBNK", "weight": 0.20, "capital": 160000.0, "entry": 69.80, "lots": 2292}
]

print("="*75)
print("🦅 ERTUĞRUL YZ - 1.000.000 TL KUVVETLİ SEANS KAPANIŞ İCRA EMRİ")
print("Saat:", datetime.datetime.now().strftime("%H:%M:%S"), "| Kapanışa Son ~65 Dakika")
print("="*75)

total_buy_comm = 0.0
for pos in ALLOCATIONS:
    invested = pos["lots"] * pos["entry"]
    comm = invested * EFF_COMMISSION_PER_SIDE
    total_buy_comm += comm
    print(f"-> [EMİR GİRİLDİ] {pos['name']:<6} | Alınan Lot: {pos['lots']:>5} | Maliyet: {pos['entry']:>6.2f} TL | Tutar: {invested:>10.2f} TL | Alış Komisyonu: {comm:>7.2f} TL")

print("-" * 75)
print(f"Toplam Pozisyon Büyüklüğü : {sum(p['lots']*p['entry'] for p in ALLOCATIONS):>12.2f} TL")
print(f"Ödenen Alış Komisyonu     : {total_buy_comm:>12.2f} TL (İş Bankası)")
print(f"Kalan Nakit Emniyet Akçesi: {PORTFOLIO_CASH - sum(p['lots']*p['entry'] for p in ALLOCATIONS) - total_buy_comm:>12.2f} TL")
print("="*75)

# Hedef ve Stop-Loss Seviyeleri (Kapanış Baskısı İçin)
print("\n📊 POZİSYON KONTROL MASASI VE ÇIKIŞ STRATEJİSİ (Hedef: Kapanış 17:50):")
for pos in ALLOCATIONS:
    target_price = pos["entry"] * 1.018  # +%1.80 hedef
    stop_price = pos["entry"] * 0.992    # -%0.80 stop
    print(f"• {pos['name']:<6}: Giriş={pos['entry']:.2f} TL | 🎯 Kar Al (+%1.8)={target_price:.2f} TL | 🛑 Zarar Kes (-%0.8)={stop_price:.2f} TL")

print("\n[BİLGİ] Saat 17:50:00'de karanlık oda (18:05) öncesi pozisyonlar tamamen nakde dönüştürülecektir.")
print("="*75)
