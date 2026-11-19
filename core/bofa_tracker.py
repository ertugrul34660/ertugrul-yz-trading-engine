# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • BofA (Bank of America) & Kurumsal Para Avcısı (Smart Money Tracker)
BIST piyasasında BofA'nın (Bank of America) girdiği, topladığı veya boşalttığı hisseleri tespit eder.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re

BOFA_BUY_TERMS = [
    "alım", "aldi", "aldı", "topladı", "toplarken", "girdi", "yuklu alim", "yüklü alım",
    "dev alım", "en çok alım", "bofa alım", "bofa'dan alım", "bofa aldı", "para girişi", "pozitif"
]

BOFA_SELL_TERMS = [
    "satış", "satti", "sattı", "çıktı", "bosaltti", "boşalttı", "yuklu satis", "yüklü satış",
    "dev satış", "en çok satış", "bofa satış", "bofa sattı", "para çıkışı", "satarken", "negatif"
]

def scan_bofa_action(symbol: str):
    """
    Seçili hissede Bank of America'nın (BofA) son ayak izlerini araştırır.
    """
    clean_sym = symbol.strip().upper().replace(".IS", "")
    query = urllib.parse.quote(f"BofA {clean_sym} Bank of America")
    url = f"https://news.google.com/rss/search?q={query}&hl=tr&gl=TR&ceid=TR:tr"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    bofa_action = "NÖTR / İZLENİYOR"
    bofa_badge = "neutral"
    bofa_score = 0
    bofa_details = []
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as res:
            root = ET.fromstring(res.read())
            items = root.findall(".//item")[:5]
            
            buy_matches = 0
            sell_matches = 0
            
            for it in items:
                title = it.find("title").text if it.find("title") is not None else ""
                title_clean = re.sub(r'<[^>]+>', '', title)
                low_title = title_clean.lower()
                
                # BofA ve Hisse adı aynı başlıkta geçiyor mu?
                has_bofa = ("bofa" in low_title or "bank of america" in low_title)
                has_sym = clean_sym.lower() in low_title
                
                if has_bofa and has_sym:
                    is_buy = any(term in low_title for term in BOFA_BUY_TERMS)
                    is_sell = any(term in low_title for term in BOFA_SELL_TERMS)
                    
                    if is_buy and not is_sell:
                        buy_matches += 1
                        bofa_details.append(f"🟢 Alım/Giriş: {title_clean}")
                    elif is_sell and not is_buy:
                        sell_matches += 1
                        bofa_details.append(f"🔴 Satış/Çıkış: {title_clean}")
                    elif is_buy and is_sell:
                        # Başlıkta iki hisse karşılaştırması olabilir (Örn: THYAO aldı, ASELS sattı)
                        # Sembolün hangi kelimeye yakın olduğunu analiz et
                        pos_sym = low_title.find(clean_sym.lower())
                        pos_alim = max(low_title.find("al"), low_title.find("girdi"))
                        pos_satis = max(low_title.find("sat"), low_title.find("çıktı"))
                        
                        if abs(pos_sym - pos_alim) < abs(pos_sym - pos_satis):
                            buy_matches += 1
                            bofa_details.append(f"🟢 Alım/Giriş: {title_clean}")
                        else:
                            sell_matches += 1
                            bofa_details.append(f"🔴 Satış/Çıkış: {title_clean}")
                            
            if buy_matches > sell_matches:
                bofa_action = "BOFA DEV ALIMDA (SMART MONEY GİRİŞİ)"
                bofa_badge = "buy"
                bofa_score = +2
            elif sell_matches > buy_matches:
                bofa_action = "BOFA SATIŞTA / TAHTAYI BOŞALTIYOR"
                bofa_badge = "sell"
                bofa_score = -2
            elif buy_matches > 0 and buy_matches == sell_matches:
                bofa_action = "BOFA ÇİFT YÖNLÜ TESTERE İŞLEMİNDE"
                bofa_badge = "neutral"
                bofa_score = 0
            else:
                bofa_action = "BOFA'NIN BELİRGİN BASKISI / ALIMI YOK"
                bofa_badge = "neutral"
                bofa_score = 0
                
    except Exception as e:
        bofa_action = "BofA takas verisi anlık taranıyor"
        
    return {
        "bofa_action": bofa_action,
        "bofa_badge": bofa_badge,
        "bofa_score": bofa_score,
        "bofa_details": bofa_details[:3]
    }

if __name__ == "__main__":
    print(scan_bofa_action("THYAO"))
    print(scan_bofa_action("ASELS"))
