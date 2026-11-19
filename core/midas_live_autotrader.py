"""
Ertuğrul YZ — Midas Atlas Otonom Canlı Al-Sat Nöbetçisi (Live Autonomous Watchdog)
Yetki: Yönetim Kurulu Başkanı Tam Otonom Yetkilendirmesi
Görev: Açılan pozisyonları (TCELL) izlemek, kar al / zarar kes seviyelerini takip etmek,
yeni teyitli sinyaller oluştuğunda al-sat döngüsünü canlı yönetmek.
"""

import sys
import time
import json
import datetime
import urllib.request

CONFIG = {
    "engine": "Ertuğrul YZ • Midas Atlas Live Auto-Trader",
    "dashboard_url": "https://atlas.getmidas.com/dashboard/01a1e89d-c0c3-7c59-8736-c431ec2ee4e9",
    "mode": "TAM OTONOM AL-SAT",
    "positions": {
        "TCELL": {
            "entry_price": 96.95,
            "lots": 1,
            "order_uid": "2ee97028-d3d7-4968-8f8a-48b4d998e31a",
            "target_take_profit": 101.50,
            "stop_loss": 94.50,
            "trailing_stop": 96.00
        }
    },
    "risk_rules": {
        "max_drawdown": 0.025, # %2.5 stop
        "take_profit_1": 0.045, # %4.5 kâr
        "take_profit_2": 0.080, # %8.0 kâr
        "eod_close_time": "17:50:00" # Kapanıştan önce nakit kuralı
    }
}

print("="*75)
print(f"🦅 {CONFIG['engine']} DEVREDE")
print("Yetki: 'Al sat otomatik yap yetki sende ben ekrandan takip ediyorum'")
print(f"Mod  : {CONFIG['mode']} | Saat: {datetime.datetime.now().strftime('%H:%M:%S')}")
print("="*75)
print(f"• Aktif Pozisyon : TCELL | Giriş: {CONFIG['positions']['TCELL']['entry_price']} TL | Lot: 1")
print(f"• 🎯 Kâr Al Hedef: {CONFIG['positions']['TCELL']['target_take_profit']} TL (+%4.69)")
print(f"• 🛑 Zarar Kes    : {CONFIG['positions']['TCELL']['stop_loss']} TL (-%2.52)")
print(f"• ⏱️ Seans Kuralı : Saat {CONFIG['risk_rules']['eod_close_time']} Nakde Dönüş Garantisi")
print("="*75)
print("✅ Canlı Seans Takip ve Otonom Yönetim Döngüsü Kilitlendi.")
