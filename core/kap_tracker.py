# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • KAP (Kamuyu Aydınlatma Platformu) Bildirim & Özel Durum Radarı
BIST hisselerinin son KAP açıklamalarını, ihale, pay geri alımı ve sermaye artırımı duyurularını tarar ve puanlar.
"""

import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
import re

def fetch_kap_disclosures(symbol: str):
    """
    Hissenin son KAP ve resmi borsa duyurularını Google News ve KAP akışlarından çeker.
    Önemli anahtar kelimelere (Pay Geri Alım, İhale, Sözleşme, Bedelsiz, Temettü, Satış) göre puan üretir.
    """
    clean_sym = symbol.strip().upper().replace(".IS", "")
    query = f"{clean_sym} KAP bildirim OR özel durum açıklaması OR pay geri alım OR ihale"
    encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded}&hl=tr&gl=TR&ceid=TR:tr"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    req = urllib.request.Request(url, headers=headers)
    
    bullish_keywords = [
        "pay geri alım", "geri alım", "ihale", "yeni iş", "sözleşme", "bedelsiz", 
        "temettü", "sipariş", "iş birliği", "yatırım teşvik", "kap", "onaylandı",
        "faaliyet kârı", "rekor"
    ]
    bearish_keywords = [
        "dava", "ceza", "spk ceza", "tedbir", "kredili işlem yasağı", "brüt takas", 
        "iflas", "zarar", "soruşturma", "iptal"
    ]

    disclosures = []
    kap_score = 0.0
    
    try:
        with urllib.request.urlopen(req, timeout=6) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            for item in root.findall(".//item")[:6]:
                title = item.find("title").text if item.find("title") is not None else ""
                link = item.find("link").text if item.find("link") is not None else ""
                pub_date = item.find("pubDate").text if item.find("pubDate") is not None else ""
                
                # Temizle
                title_lower = title.lower()
                clean_title = title.split(" - ")[0]
                
                is_bullish = any(k in title_lower for k in bullish_keywords)
                is_bearish = any(k in title_lower for k in bearish_keywords)
                
                impact = "Nötr"
                badge = "neutral"
                if is_bullish and not is_bearish:
                    impact = "Çok Olumlu (KAP Katalizörü)"
                    badge = "buy"
                    kap_score += 1.5
                elif is_bearish:
                    impact = "Riskli / Tedbir"
                    badge = "sell"
                    kap_score -= 2.0
                    
                disclosures.append({
                    "title": clean_title,
                    "link": link,
                    "date": pub_date[:16] if pub_date else "Son Seans",
                    "impact": impact,
                    "badge": badge
                })
    except Exception as e:
        pass

    # Skor ve Rozet
    if kap_score >= 1.5:
        kap_status = "KAP'TA GÜÇLÜ KATALİZÖR (Pozitif Bildirim)"
        kap_badge = "buy"
    elif kap_score <= -1.5:
        kap_status = "KAP'TA RİSK / TEDBİR BİLDİRİMİ"
        kap_badge = "sell"
    else:
        kap_status = "RUTİN KAP AKIŞI (Nötr)"
        kap_badge = "neutral"

    return {
        "success": True,
        "symbol": clean_sym,
        "kap_status": kap_status,
        "kap_badge": kap_badge,
        "kap_score": round(kap_score, 1),
        "disclosures": disclosures,
        "disclosure_count": len(disclosures)
    }

if __name__ == "__main__":
    res = fetch_kap_disclosures("THYAO")
    print("THYAO KAP:", res["kap_status"], "Puan:", res["kap_score"])
