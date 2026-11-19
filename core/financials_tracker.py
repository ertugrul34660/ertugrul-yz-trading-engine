# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Borsa İstanbul Bilanço & Temel Analiz Avcısı (Financial & Balance Sheet Engine)
BIST şirketlerinin resmi finansal tablolarını, net kârlarını, F/K ve özkaynak kârlılıklarını çeker.
1. Net Kâr (Net Income)
2. Toplam Gelir / Ciro (Revenue)
3. Fiyat / Kazanç Oranı (F/K - P/E Ratio)
4. Hisse Başına Kâr (HBK / EPS)
5. Özkaynak Kârlılığı (ROE %)
6. Borçluluk / Finansal Sağlık Notu (A+, A, B, C)
"""

import urllib.request
import json
import ssl

def format_currency_human(val):
    if val is None:
        return "Açıklanmadı"
    abs_val = abs(val)
    if abs_val >= 1_000_000_000:
        return f"{val / 1_000_000_000:.2f} Milyar TL"
    elif abs_val >= 1_000_000:
        return f"{val / 1_000_000:.2f} Milyon TL"
    elif abs_val >= 1_000:
        return f"{val / 1_000:.2f} Bin TL"
    return f"{val:.2f} TL"

def fetch_company_fundamentals(symbol: str):
    """
    Seçilen hissenin bilanço, kârlılık ve temel finansal oranlarını çeker.
    """
    clean_sym = symbol.strip().upper().replace(".IS", "")
    ticker = f"BIST:{clean_sym}"
    
    url = "https://scanner.tradingview.com/turkey/scan"
    payload = {
        "symbols": {"tickers": [ticker]},
        "columns": [
            "name",
            "close",
            "total_revenue",              # Yıllık Ciro
            "net_income",                 # Yıllık Net Kâr
            "price_earnings_ttm",         # Fiyat/Kazanç (F/K)
            "earnings_per_share_basic_ttm", # Hisse Başına Kâr (HBK)
            "return_on_equity",           # Özkaynak Kârlılığı (%)
            "debt_to_equity"              # Borç / Özkaynak Oranı
        ]
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }
    
    try:
        ctx = ssl._create_unverified_context()
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=6) as res:
            data = json.loads(res.read().decode("utf-8"))
            row = data.get("data", [])
            if not row or len(row) == 0:
                raise ValueError("Bilanço verisi bulunamadı")
                
            d = row[0].get("d", [])
            revenue = d[2]
            net_income = d[3]
            pe_ratio = d[4]
            eps = d[5]
            roe = d[6]
            debt_ratio = d[7]
            
            # Finansal Sağlık Notu Hesaplama
            health_score = "B (Dengeli)"
            health_badge = "neutral"
            if net_income and net_income > 0 and pe_ratio and pe_ratio < 10 and (roe and roe > 15):
                health_score = "A+ (Mükemmel Bilanço)"
                health_badge = "buy"
            elif net_income and net_income > 0 and (not debt_ratio or debt_ratio < 1.5):
                health_score = "A (Güçlü Bilanço)"
                health_badge = "buy"
            elif net_income and net_income < 0:
                health_score = "C (Net Zararda)"
                health_badge = "sell"
                
            pe_str = f"{pe_ratio:.2f}" if pe_ratio is not None else "Hesaplanamıyor"
            eps_str = f"{eps:.2f} TL" if eps is not None else "Açıklanmadı"
            roe_str = f"%{roe:.1f}" if roe is not None else "Veri Yok"
            
            summary_text = (
                f"{clean_sym}, son 12 ayda {format_currency_human(net_income)} net kâr elde etti. "
                f"F/K Oranı {pe_str} seviyesinde ve hisse başına kârı {eps_str}. "
                f"Özkaynak kârlılığı ({roe_str}) şirketin verimli çalıştığını gösteriyor."
            )
            
            return {
                "success": True,
                "symbol": clean_sym,
                "net_income_str": format_currency_human(net_income),
                "revenue_str": format_currency_human(revenue),
                "pe_ratio": pe_str,
                "eps": eps_str,
                "roe": roe_str,
                "health_score": health_score,
                "health_badge": health_badge,
                "summary": summary_text
            }
            
    except Exception as e:
        return {
            "success": False,
            "symbol": clean_sym,
            "net_income_str": "Bilanço Açıklanmadı",
            "revenue_str": "Veri Alınamadı",
            "pe_ratio": "Nötr",
            "eps": "-",
            "roe": "-",
            "health_score": "B (Standart)",
            "health_badge": "neutral",
            "summary": f"{clean_sym} için resmi bilanço ve finansal tablo akışı taranıyor."
        }

if __name__ == "__main__":
    test = fetch_company_fundamentals("THYAO")
    print("THYAO Bilanço & Temel Analiz:", json.dumps(test, ensure_ascii=False, indent=2))
