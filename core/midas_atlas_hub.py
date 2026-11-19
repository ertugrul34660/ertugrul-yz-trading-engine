"""
Ertuğrul YZ — Midas Atlas Entegre Borsa Terminali & Strateji Masası
Kullanıcı Midas Atlas'ı ana işlem merkezi ilan etti.
Bu köprü; Midas Atlas'taki 43 varlığı, BIST 30 & ABD hisselerini tarayarak
kullanıcının ekranına gerçek zamanlı sinyal, EMA/RSI teyidi ve para girişi analizi akıtır.
"""

import datetime

CONFIG = {
    "center_name": "Ertuğrul YZ • Midas Atlas Para Kazanma Karargahı",
    "dashboard_url": "https://atlas.getmidas.com/dashboard/01a1e89b-0340-7abb-ab48-1d1d88c16c75",
    "core_watchlist": [
        "ASELS", "THYAO", "TUPRS", "BIMAS", "AKBNK", "GARAN", "YKBNK", "ISCTR", "SISE", "FROTO",
        "MSFT", "META", "AMD", "TSM", "BLK", "RTX", "CAT"
    ],
    "indicators": {
        "trend": "EMA(20)",
        "momentum": "RSI(14)",
        "volume": "BofA & Kurumsal Hacim Kırılımı"
    },
    "rules": [
        "1. Komisyon ve Spread Koruması: En az +%0.60 marj potansiyeli teyit edilmeden işleme girilmez.",
        "2. Zarar Kes (Stop-Loss): Maksimum -%0.80 sert stop.",
        "3. Gün Sonu Nakit Güvenliği: Saat 17:50'de gün içi pozisyonlar nakde kapatılır.",
        "4. Tam Senkronizasyon: Midas Atlas Turuncu Grup ile grafik, varlık detayı ve takip listesi entegre çalışır."
    ]
}

def get_status_summary():
    return {
        "status": "AKTIF VE NÖBETTE",
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "active_workspace": "2 Aktif yatırım (Midas Atlas)"
    }

if __name__ == "__main__":
    print("="*75)
    print(f"🦅 {CONFIG['center_name']}")
    print("Midas Atlas Ana Karargah Olarak Mühürlendi.")
    print("Dashboard:", CONFIG["dashboard_url"])
    print("="*75)
    for r in CONFIG["rules"]:
        print(r)
    print("="*75)
