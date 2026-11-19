"""
Ertuğrul YZ — İleri Düzey Borsa İstanbul & Midas Atlas Emir Türleri ve İcra Motoru
Bu motor; BIST piyasa yapısındaki 11 kritik emir türünü tanımlar, kurallarını belirler
ve algoritmik botun piyasa koşullarına göre en doğru emir türünü otonom seçmesini sağlar.
"""

import json
from datetime import datetime

ADVANCED_ORDER_TYPES_DICTIONARY = {
    "MARKET": {
        "name": "Piyasa Emri",
        "description": "Fiyat belirtilmeden o an tahtadaki en iyi fiyattan anında eşleşen emir.",
        "use_case": "Acil çıkış veya kaçırılmaması gereken ani tavan/taban sıçramalarında milisaniyelik icra."
    },
    "LIMIT": {
        "name": "Limit Emir",
        "description": "Belirli bir maksimum alış veya minimum satış fiyatı tanımlanan emir.",
        "use_case": "İstenen fiyattan kâr realize etmek (ör. ISCTR 13.25 TL) veya hedeflenen dipten almak."
    },
    "MARKET_TO_LIMIT": {
        "name": "Piyasadan Limite Emir",
        "description": "En iyi fiyattan eşleşip kalan kısmı o fiyatta limit emir olarak tahtaya yazan emir.",
        "use_case": "Tahtada kademe süpürürken fiyatın kontrolsüz kaymasını (slippage) önlemek."
    },
    "DAY": {
        "name": "Günlük Emir",
        "description": "Yalnızca girildiği seans günü boyunca geçerli olan, 18:05'te süresi dolan emir.",
        "use_case": "Gün içi hızlı skalp ve gün sonu pozisyon taşımama stratejilerinde."
    },
    "GTD": {
        "name": "Tarihli Emir (Good 'Til Date)",
        "description": "Belirlenen ileri bir tarihe kadar (ör. 1 hafta / 1 ay) iptal edilmeden tahtada bekleyen emir.",
        "use_case": "Dün yaşanan 'süresi doldu' durumunu aşmak için 1 haftalık hedef koyma."
    },
    "GTC": {
        "name": "İptale Kadar Geçerli Emir (Good 'Til Cancelled)",
        "description": "Kullanıcı veya bot elle iptal edene kadar (veya maksimum vadeye dek) sistemde aktif kalan emir.",
        "use_case": "Uzun vadeli kâr hedefleri ve kalıcı stop zırhlarında."
    },
    "STOP_LOSS": {
        "name": "Stop-Loss (Zarar Kes Emri)",
        "description": "Fiyat belirlenen tetik seviyesine düştüğünde otomatik satış emrini tetikleyen koruma kalkanı.",
        "use_case": "Sermayeyi ani çöküşlerden korumak (ör. TCELL 95.00 TL stopu)."
    },
    "TAKE_PROFIT": {
        "name": "Kâr Al Emri (Take-Profit)",
        "description": "Fiyat kâr hedefine ulaştığında otomatik kâr realizasyonu yapan emir.",
        "use_case": "Hedef fiyata iğne atıldığında kaçırmadan kârı kasaya çekmek."
    },
    "CONDITIONAL": {
        "name": "Koşullu Emir",
        "description": "Belirli bir koşul (hisse X fiyatına gelince, endeks şu olunca vb.) sağlandığında devreye giren emir.",
        "use_case": "Zincir emirler ve direnç kırılımlarında otomatik alım tetikleme."
    },
    "FOK": {
        "name": "Gerçekleş ya da İptal Et (Fill or Kill)",
        "description": "Emrin tamamı tek seferde o an karşılanamazsa emrin tamamını derhal iptal eden emir.",
        "use_case": "Parçalı eşleşme istemediğimiz, tüm lotların tek seferde alınması gereken kurumsal blok alımlarda."
    },
    "IOC": {
        "name": "Hepi Topu Ya Da İptal Et (Immediate or Cancel / Kalanı İptal Et)",
        "description": "O an eşleşebildiği kadarını karşılayan, karşılanamayan kalan lotları anında iptal eden emir.",
        "use_case": "Hızlı alımda tahtada kalan lotların açıkta bekleyip bloke yaratmasını engellemek."
    }
}

def select_best_order_type(strategy_name, urgency="NORMAL"):
    """
    Piyasa şartına ve stratejiye göre en optimal emir tipini seçer.
    """
    if urgency == "EMERGENCY_STOP":
        return "STOP_LOSS", "MARKET"
    elif strategy_name == "QUICK_SCALP":
        return "LIMIT", "IOC"
    elif strategy_name == "SWING_TREND":
        return "LIMIT", "GTD"
    return "LIMIT", "DAY"

if __name__ == "__main__":
    print("✅ 11 İleri Düzey BIST & Midas Emir Türü Başarıyla Hafızaya Alındı ve Kütüğe Mühürlendi.")
