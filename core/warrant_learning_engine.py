"""
Ertuğrul YZ — Varant, Kaldıraç & Türev Araçlar Quant Öğrenme Motoru
(Borsa İstanbul & Midas Atlas Varant Strateji Modülü)
"""

import sys
import math
import random
import datetime

print("="*75)
print("🦅 ERTUĞRUL YZ • VARANT & TÜREV ARAÇLAR UZMANLIK MODÜLÜ BAŞLATILDI")
print("Saat:", datetime.datetime.now().strftime("%H:%M:%S"))
print("="*75)

# Varantın Temel Bileşenleri ve Parametreleri:
# 1. Alım Varantı (Call): Dayanak varlık (Örn. THYAO) yükselirse varant katlanarak yükselir.
# 2. Satım Varantı (Put): Dayanak varlık düşerse varant katlanarak yükselir (Düşüşten para kazanma).
# 3. Kaldıraç (Gearing): Küçük parayla (1 TL - 5 TL) büyük hisse hareketi yakalama (Örn. 5x - 10x).
# 4. Teta (Theta - Zaman Aşımı): Varantın vadesi yaklaştıkça her gün değer kaybeder (Zaman erimesi).
# 5. Delta: Dayanak varlık 1 TL değiştiğinde varantın kaç kuruş değişeceği.

SAMPLE_WARRANTS = [
    {"code": "THDAA", "underlying": "THYAO", "type": "ALIM (CALL)", "strike": 330.0, "price": 1.45, "gearing": 7.5, "delta": 0.55, "days_to_expiry": 45},
    {"code": "THDRR", "underlying": "THYAO", "type": "SATIM (PUT)", "strike": 315.0, "price": 0.85, "gearing": 8.2, "delta": -0.45, "days_to_expiry": 45},
    {"code": "ASDAA", "underlying": "ASELS", "type": "ALIM (CALL)", "strike": 355.0, "price": 1.80, "gearing": 6.8, "delta": 0.60, "days_to_expiry": 60},
    {"code": "AKDAA", "underlying": "AKBNK", "type": "ALIM (CALL)", "strike": 72.0,  "price": 0.65, "gearing": 9.1, "delta": 0.50, "days_to_expiry": 30},
    {"code": "IBDAA", "underlying": "XU030", "type": "ENDEKS ALIM", "strike": 11000, "price": 2.10, "gearing": 12.0, "delta": 0.65, "days_to_expiry": 40}
]

print("\n[BIST 30 SEÇKİN VARANT HAVUZU (MİDAS ATLAS UYUMLU)]:")
for w in SAMPLE_WARRANTS:
    print(f"• {w['code']:<6} | Dayanak: {w['underlying']:<6} | Tip: {w['type']:<12} | Fiyat: {w['price']:>5.2f} TL | Kaldıraç: {w['gearing']:>4.1f}x | Vade: {w['days_to_expiry']} Gün")

print("\n" + "="*75)
print("📊 1.000 İŞLEMLİK AKILLI VARANT SİMÜLASYONU VE ÖĞRENME TESTİ:")

initial_kasa = 120.0  # Kullanıcının mevcut 120 TL'lik bakiyesi
kasa = initial_kasa
wins = 0
losses = 0

for i in range(1, 1001):
    w = random.choice(SAMPLE_WARRANTS)
    
    # Kasanın %25'i ile varant işlemi (30 TL ile örneğin 20-30 adet varant)
    pos_size = kasa * 0.25
    
    # Dayanak varlık hareketi (Örn. hissede %1.5 hareket)
    stock_move = random.gauss(0.002, 0.012)
    
    # Varant kaldıraçlı hareketi: stock_move * gearing - günlük teta erimesi (-%0.3)
    teta_decay = 0.003
    warrant_move = (stock_move * w["gearing"]) - teta_decay
    
    pnl = pos_size * warrant_move
    kasa += pnl
    
    if pnl > 0:
        wins += 1
    else:
        losses += 1

print(f"• Başlangıç Sermayesi : {initial_kasa:.2f} TL")
print(f"• Bitiş Sermayesi     : {kasa:.2f} TL (Net Büyüme: %{((kasa-initial_kasa)/initial_kasa)*100:+.2f})")
print(f"• Başarılı / Başarısız : {wins} Kâr / {losses} Zarar (Kazanma Oranı: %{(wins/1000)*100:.1f})")
print("="*75)

print("\n🧠 VARANTLARDAN ÖĞRENİLEN 4 BÜYÜK YASA:")
print("1. ÇİFT TARAFLI KAZANÇ: Borsa çökerken dahi 'Satım (PUT)' varantı alarak endeks düştükçe para kazanılabilir!")
print("2. KALDIRAÇ GÜCÜ: Hissede %2'lik bir yükseliş, 8x kaldıraçlı varantta %16 kâr üretir!")
print("3. TETA (ZAMAN AŞIMI) TEHLİKESİ: Varant uzun süre elde tutulmaz; zaman erimesi parayı yer. Gün içi veya 2-3 günlük trendlerde vur-kaç yapılır.")
print("4. MİDAS ATLAS AVANTAJI: Midas'ta 'Varant zinciri' ve 'Varant trendleri' modülleri doğrudan mevcuttur.")
print("="*75)
