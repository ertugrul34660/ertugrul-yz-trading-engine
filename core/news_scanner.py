# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Borsa Haber & Yorum Algı Puanlama Motoru (Sentiment & Comment Scorer)
1. Hisse hakkındaki internet haberlerini ve piyasa yorumlarını tarar.
2. Her bir haberi/yorumu kelime ağırlıklarıyla matematiksel olarak puanlar (+2, +1, -1, -2).
3. 0-100 arasında 'Piyasa Algı & Yorum Puanı' üretir:
   - 80-100: ÇOK OLUMLU (Yatırımcı ve medya arkasında)
   - 60-79: OLUMLU (İyi beklentiler hakim)
   - 40-59: NÖTR / DENGELİ (Karışık yorumlar)
   - 0-39: OLUMSUZ (Haber baskısı ve şikayet var)
4. Bu puanı doğrudan Titan v6.0 karar motorunun toplam skoruna yansıtır.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
import json

# Güçlü Olumlu Anahtar Kelimeler (+2 Puan)
STRONG_POSITIVE = [
    "rekor", "tavan", "patlama", "büyük kâr", "dev ihale", "dev sipariş", "yüksek kâr", 
    "beklentileri aştı", "güçlü bilanço", "uçuşa geçti", "al tavsiyesi", "hedef yükseldi", "bofa topluyor"
]

# Ilımlı Olumlu Anahtar Kelimeler (+1 Puan)
MILD_POSITIVE = [
    "yükseldi", "arttı", "kâr", "alım", "alim", "hedef", "bofa", "guclu", "güçlü", "büyüme", 
    "dev işlem", "sözleşme", "anlaşma", "temettü", "onay", "pozitif", "fırsat", "destek", "toparlanma"
]

# Güçlü Olumsuz Anahtar Kelimeler (-2 Puan)
STRONG_NEGATIVE = [
    "taban", "ağır zarar", "dava", "soruşturma", "ceza", "iflas", "kriz", "büyük çöküş", 
    "sert düştü", "beklentilerin altında", "satış dalgası", "bofa boşalttı", "panik"
]

# Ilımlı Olumsuz Anahtar Kelimeler (-1 Puan)
MILD_NEGATIVE = [
    "düştü", "zarar", "satış", "risk", "geriledi", "kayıp", "uyarı", "iptal", "baskı", 
    "negatif", "düşüş", "zayıf", "endişe", "duraksama"
]

def score_comment_text(text: str):
    """
    Tek bir haber veya yorum başlığını puanlar.
    """
    lower = text.lower()
    score = 0
    tags = []

    for w in STRONG_POSITIVE:
        if w in lower:
            score += 2
            tags.append(f"+2 ({w})")
            break

    if score == 0:
        for w in MILD_POSITIVE:
            if w in lower:
                score += 1
                tags.append(f"+1 ({w})")
                break

    for w in STRONG_NEGATIVE:
        if w in lower:
            score -= 2
            tags.append(f"-2 ({w})")
            break

    if score >= 0:
        for w in MILD_NEGATIVE:
            if w in lower:
                score -= 1
                tags.append(f"-1 ({w})")
                break

    if score > 0:
        sentiment = "Olumlu"
    elif score < 0:
        sentiment = "Olumsuz"
    else:
        sentiment = "Nötr"

    return score, sentiment

def fetch_stock_news(symbol: str, max_items: int = 6):
    """
    Google News ve finans bültenlerinden haberleri çeker ve puanlar.
    """
    clean_sym = symbol.strip().upper().replace(".IS", "")
    query = urllib.parse.quote(f"{clean_sym} hisse")
    url = f"https://news.google.com/rss/search?q={query}&hl=tr&gl=TR&ceid=TR:tr"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    news_items = []
    total_raw_score = 0
    pos_items_count = 0
    neg_items_count = 0
    neutral_items_count = 0
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as res:
            xml_data = res.read()
            root = ET.fromstring(xml_data)
            
            items = root.findall(".//item")[:max_items]
            for it in items:
                title = it.find("title").text if it.find("title") is not None else ""
                link = it.find("link").text if it.find("link") is not None else "#"
                pub_date = it.find("pubDate").text if it.find("pubDate") is not None else ""
                
                title_clean = re.sub(r'<[^>]+>', '', title)
                item_score, sentiment = score_comment_text(title_clean)
                total_raw_score += item_score
                
                if sentiment == "Olumlu":
                    pos_items_count += 1
                elif sentiment == "Olumsuz":
                    neg_items_count += 1
                else:
                    neutral_items_count += 1
                    
                news_items.append({
                    "title": title_clean,
                    "link": link,
                    "date": pub_date[:16] if pub_date else "",
                    "sentiment": sentiment,
                    "score": item_score
                })
                
        # 0-100 Arasında Yorum & Algı Puanı Hesabı (Sentiment Index)
        # Nötr başlangıç 50 puandır. Her +1 puan skoru yukarı, her -1 aşağı çeker.
        sentiment_index = int(50 + (total_raw_score * 8.5))
        sentiment_index = max(10, min(sentiment_index, 98))  # 10 ile 98 arasında sınırla
        
        if sentiment_index >= 75:
            overall_sentiment = "Ağırlıklı Olumlu (Haber Desteği Güçlü)"
            sentiment_badge = "success"
            sentiment_impact = "+1.5 Puan (Pozitif İvme)"
        elif sentiment_index >= 60:
            overall_sentiment = "Pozitif Eğilimli (Yorumlar İyi)"
            sentiment_badge = "success"
            sentiment_impact = "+0.8 Puan (Hafif Destek)"
        elif sentiment_index <= 35:
            overall_sentiment = "Ağırlıklı Olumsuz (Yoğun Haber Baskısı)"
            sentiment_badge = "danger"
            sentiment_impact = "-1.5 Puan (Aşağı Yönlü Risk)"
        elif sentiment_index <= 45:
            overall_sentiment = "Hafif Negatif (Temkinli Yorumlar)"
            sentiment_badge = "warning"
            sentiment_impact = "-0.8 Puan (Baskı Var)"
        else:
            overall_sentiment = "Dengeli / Nötr Piyasa Yorumları"
            sentiment_badge = "neutral"
            sentiment_impact = "0.0 Puan (Nötr Etki)"

        return {
            "news": news_items,
            "overall_sentiment": overall_sentiment,
            "sentiment_score": round((sentiment_index - 50) / 25, 2),  # Titan motoru için -2.0 ile +2.0 arası çarpan
            "sentiment_index": sentiment_index,  # 0-100 puan
            "sentiment_badge": sentiment_badge,
            "sentiment_impact": sentiment_impact,
            "pos_count": pos_items_count,
            "neg_count": neg_items_count,
            "neutral_count": neutral_items_count,
            "total_evaluated": len(news_items)
        }
    except Exception as e:
        return {
            "news": [],
            "overall_sentiment": "Dengeli / Nötr Piyasa Yorumları",
            "sentiment_score": 0.0,
            "sentiment_index": 50,
            "sentiment_badge": "neutral",
            "sentiment_impact": "0.0 Puan (Nötr)",
            "pos_count": 0,
            "neg_count": 0,
            "neutral_count": 0,
            "total_evaluated": 0
        }

if __name__ == "__main__":
    res = fetch_stock_news("THYAO")
    print("Haber Puanı (0-100):", res["sentiment_index"])
    print("Genel Değerlendirme:", res["overall_sentiment"])
    print("Olumlu/Olumsuz Dağılımı:", f"{res['pos_count']} Olumlu / {res['neg_count']} Olumsuz")
    for n in res["news"]:
        print(f"[{n['sentiment']} | Skor: {n['score']:+}] {n['title']}")
