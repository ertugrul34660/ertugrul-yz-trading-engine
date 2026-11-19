# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Çoklu Yapay Zekâ & Dış Algoritmik Sistemler Konsensüs Motoru (Consensus Tracker)
İncelenen hissede diğer global ve yerel piyasa sistemlerinin izini sürer:
1. TradingView Teknik Algoritma Robotları (26 İndikatör Konsensüsü: Recommend.All, MA, Osilatörler)
2. Kurumsal Finans Kurumları & Aracı Kurum Hedef Fiyat Konsensüsü (Hedef Fiyat Ortalaması & Tavsiye)
3. Yerel BIST Yapay Zekâ Modelleri ve Algoritmik Trend Teyidi
"""

import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import ssl
import re

def get_tradingview_recommendation(symbol: str):
    """
    TradingView'ın 26 farklı teknik indikatör ve hareketli ortalama üzerinde koşturduğu
    resmi robot konsensüs sinyalini çeker (-1.0 Güçlü Sat ile +1.0 Güçlü Al arası).
    """
    clean_sym = symbol.strip().upper().replace(".IS", "")
    url = "https://scanner.tradingview.com/turkey/scan"
    
    payload = {
        "symbols": {"tickers": [f"BIST:{clean_sym}"]},
        "columns": ["Recommend.All", "Recommend.MA", "Recommend.Other", "RSI", "MACD.macd", "MACD.signal"]
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }
    
    try:
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=8) as res:
            res_json = json.loads(res.read().decode("utf-8"))
            data_arr = res_json.get("data", [])
            if data_arr and len(data_arr) > 0:
                vals = data_arr[0].get("d", [])
                rec_all = vals[0] if len(vals) > 0 else 0
                rec_ma = vals[1] if len(vals) > 1 else 0
                rec_other = vals[2] if len(vals) > 2 else 0
                
                # TradingView skalası: -1.0 ile 1.0 arası
                if rec_all >= 0.5:
                    tv_signal = "GÜÇLÜ AL"
                    tv_badge = "buy"
                    tv_score = 2
                elif rec_all >= 0.1:
                    tv_signal = "AL"
                    tv_badge = "buy"
                    tv_score = 1
                elif rec_all <= -0.5:
                    tv_signal = "GÜÇLÜ SAT"
                    tv_badge = "sell"
                    tv_score = -2
                elif rec_all <= -0.1:
                    tv_signal = "SAT"
                    tv_badge = "sell"
                    tv_score = -1
                else:
                    tv_signal = "NÖTR"
                    tv_badge = "neutral"
                    tv_score = 0
                    
                return {
                    "available": True,
                    "signal": tv_signal,
                    "badge": tv_badge,
                    "score": tv_score,
                    "score_raw": round(rec_all, 2),
                    "summary": f"TradingView 26 İndikatör Robotu: {tv_signal} ({rec_all:+.2f})"
                }
    except Exception as e:
        pass
        
    return {
        "available": False,
        "signal": "Veri Yok",
        "badge": "neutral",
        "score": 0,
        "summary": "TradingView robot sinyali hesaplanamadı."
    }

def get_institutional_consensus(symbol: str):
    """
    Aracı kurumlar, hedef fiyat raporları ve konsensüs beklentilerini haberlerden tarar.
    """
    clean_sym = symbol.strip().upper().replace(".IS", "")
    query = urllib.parse.quote(f"{clean_sym} hedef fiyat analist beklenti")
    url = f"https://news.google.com/rss/search?q={query}&hl=tr&gl=TR&ceid=TR:tr"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    reports = []
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as res:
            root = ET.fromstring(res.read())
            items = root.findall(".//item")[:4]
            for it in items:
                title = it.find("title").text if it.find("title") is not None else ""
                clean_title = re.sub(r'<[^>]+>', '', title)
                if clean_sym in clean_title.upper():
                    reports.append(clean_title)
    except Exception:
        pass
        
    return reports

def scan_peer_systems(symbol: str):
    """
    Dış Yapay Zekâ ve Algoritma Sistemlerinin ortak konsensüsünü üretir.
    """
    tv_res = get_tradingview_recommendation(symbol)
    consensus_reports = get_institutional_consensus(symbol)
    
    return {
        "tradingview": tv_res,
        "analyst_reports": consensus_reports[:3]
    }

if __name__ == "__main__":
    res = scan_peer_systems("THYAO")
    print("TradingView:", res["tradingview"])
    print("Kurumsal Raporlar:", res["analyst_reports"])
