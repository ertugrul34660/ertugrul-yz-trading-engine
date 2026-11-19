# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Sosyal Medya & Borsa Topluluk Fısıltı Radarı (Social Sentiment)
Twitter/X, Borsa forumları ve yatırımcı topluluklarındaki güncel ilgi ve FOMO/Korku seviyesini ölçer.
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

def fetch_social_community_whisper(symbol: str):
    clean_sym = symbol.strip().upper().replace(".IS", "")
    query = f"#{clean_sym} OR {clean_sym} hisse twitter OR borsa yorum"
    encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded}&hl=tr&gl=TR&ceid=TR:tr"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    req = urllib.request.Request(url, headers=headers)
    
    pos_words = ["ralli", "tavan", "patlama", "hedef", "alım", "uçuyor", "yükseliş", "beklenti", "rekor"]
    neg_words = ["çöküş", "taban", "düşüş", "patladı", "zarar", "kaçış", "satış", "panik"]
    
    pos_count = 0
    neg_count = 0
    snippets = []
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            for item in root.findall(".//item")[:5]:
                title = item.find("title").text if item.find("title") is not None else ""
                clean_t = title.split(" - ")[0]
                t_lower = clean_t.lower()
                
                is_p = any(w in t_lower for w in pos_words)
                is_n = any(w in t_lower for w in neg_words)
                
                if is_p: pos_count += 1
                if is_n: neg_count += 1
                
                snippets.append(clean_t)
    except Exception:
        pass

    total = pos_count + neg_count
    if pos_count > neg_count and pos_count >= 1:
        sentiment_label = "YÜKSEK COŞKU & POZİTİF FISILTI (FOMO Başlangıcı)"
        badge = "buy"
        score = 0.8
    elif neg_count > pos_count and neg_count >= 1:
        sentiment_label = "PANİK & SATIŞ FISILTISI (Korku Hâkim)"
        badge = "sell"
        score = -0.8
    else:
        sentiment_label = "TOPLULUK BEKLEMEDE (Dengeli İlgi)"
        badge = "neutral"
        score = 0.0

    return {
        "social_status": sentiment_label,
        "social_badge": badge,
        "social_score": score,
        "pos_count": pos_count,
        "neg_count": neg_count,
        "top_whispers": snippets[:3]
    }
