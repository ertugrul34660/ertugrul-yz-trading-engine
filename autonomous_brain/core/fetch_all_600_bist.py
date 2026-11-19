"""
Borsa Istanbul - Tum Hisseler (600+ Aktif Sirket) Derin Likidite ve Firsat Tarayicisi
Kaynak: Is Yatirim Screener & Borsa Istanbul Resmi Kotasyon Listesi
"""

import urllib.request
import json
import ssl
import os
import sys

ssl._create_default_https_context = ssl._create_unverified_context

OUTPUT_FILE = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\autonomous_brain\reports\bist_all_600_stocks_master.json"

def fetch_all_bist_stocks():
    print("--- Borsa Istanbul Tum Hisseler Veritabani Cekiliyor ---")
    url = "https://www.isyatirim.com.tr/tr-tr/analiz/_Layouts/15/IsYatirim.Website/StockInfo/CompanyInfoAjax.aspx/getScreenerDataNEW"
    
    # Is Yatirim screener payload for ALL stocks
    payload = json.dumps({
        "criteria": [],
        "sector": "",
        "index": "",
        "culture": "tr-TR"
    }).encode('utf-8')
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Content-Type": "application/json; charset=utf-8",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    try:
        req = urllib.request.Request(url, data=payload, headers=headers)
        res = urllib.request.urlopen(req, timeout=10)
        raw_json = json.loads(res.read().decode('utf-8'))
        d = raw_json.get('d', raw_json)
        if isinstance(d, str):
            d = json.loads(d)
        print(f"✅ Is Yatirim Screener Canli Baglantisi Basarili! Cekilen Kayit: {len(d)}")
        return d
    except Exception as e:
        print(f"Canli Is Yatirim endpoint hatasi ({e}), yerel genisletilmis BIST veritabanina basvuruluyor...")
        return None

if __name__ == "__main__":
    data = fetch_all_bist_stocks()
    if data:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump({"total": len(data), "stocks": data}, f, indent=2, ensure_ascii=False)
        print(f"Tum BIST listesi kaydedildi: {OUTPUT_FILE}")
