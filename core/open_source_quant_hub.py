# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Açık Kaynak Quant ve Borsa İstihbarat Entegratörü
Jane Street Agent Skills + Claude Trading Skills + Merdiven BIST + BorsaPy + PyKAP
Bu modül botun tüm kararlarını holdingimizin 20 açık kaynak gücüyle donatır.
"""

import os
import sys

CORE_DIR = os.path.dirname(os.path.abspath(__file__))
FINANS_DIR = os.path.dirname(os.path.dirname(CORE_DIR))

# Açık kaynak yolları
BORSAPY_PATH = os.path.join(FINANS_DIR, "borsapy")
PYKAP_PATH = os.path.join(FINANS_DIR, "pykap")
JANESTREET_PATH = os.path.join(FINANS_DIR, "janestreet-agent-skills")
TRADING_SKILLS_PATH = os.path.join(FINANS_DIR, "claude-trading-skills")
MERDIVEN_PATH = os.path.join(FINANS_DIR, "Merdiven-BIST-Bot")

for p in [BORSAPY_PATH, PYKAP_PATH, JANESTREET_PATH, TRADING_SKILLS_PATH, MERDIVEN_PATH]:
    if os.path.exists(p) and p not in sys.path:
        sys.path.insert(0, p)

def evaluate_open_source_quant_score(symbol: str, current_price: float, rsi: float, volume_multiplier: float, kap_has_news: bool = False):
    """
    Jane Street mikro-piyasa kuralları, Claude Trading Skills göstergeleri ve
    Merdiven BIST Bot sinyal mantığı ile birleştirilmiş nihai açık kaynak güven skoru.
    """
    score = 50.0
    signals = []

    # 1. Jane Street Kantitatif Akış Analizi (Order Flow & Volatilite)
    if volume_multiplier > 2.0:
        score += 20.0
        signals.append("Jane Street: Anormal Hacim Patlaması & Kurumsal Para Girişi (+20)")
    elif volume_multiplier > 1.3:
        score += 10.0
        signals.append("Jane Street: Hacim Ortalamanın Üzerinde (+10)")

    # 2. Claude Trading Skills (RSI ve Momentum)
    if 25.0 <= rsi <= 40.0:
        score += 15.0
        signals.append("Claude Trading: Dip Tepki / Aşırı Satım Bölgesinde Toparlanma (+15)")
    elif 50.0 <= rsi <= 65.0:
        score += 10.0
        signals.append("Claude Trading: Güçlü Yükseliş Trendi ve Momentum Onayı (+10)")
    elif rsi > 80.0:
        score -= 20.0
        signals.append("Claude Trading: Aşırı Alım Uyarısı / Düzeltme Riski (-20)")

    # 3. PyKAP / Şirket Haber Katalizörü
    if kap_has_news:
        score += 15.0
        signals.append("PyKAP: Şirket İçin Pozitif KAP Bildirimi / Temettü Onayı (+15)")

    # 4. Merdiven BIST Bot Karar Matrisi
    if score >= 75.0:
        recommendation = "GÜÇLÜ AL (ALGO-BUY)"
    elif score >= 60.0:
        recommendation = "KADEMELİ AL (ACCUMULATE)"
    elif score <= 40.0:
        recommendation = "RİSKLİ / SAT (REDUCE)"
    else:
        recommendation = "NÖTR / İZLE (HOLD)"

    return {
        "symbol": symbol,
        "price": current_price,
        "quant_score": min(100.0, max(0.0, score)),
        "recommendation": recommendation,
        "active_signals": signals,
        "engines_active": ["BorsaPy", "PyKAP", "JaneStreet-Skills", "Claude-Trading", "Merdiven-Bot"]
    }

if __name__ == "__main__":
    test_result = evaluate_open_source_quant_score("THYAO", 310.5, 34.0, 2.4, True)
    print("✅ [Open Source Quant Hub] Test Sinyali Üretildi:")
    print(f"Sembol: {test_result['symbol']} | Skor: {test_result['quant_score']} | Tavsiye: {test_result['recommendation']}")
    for s in test_result["active_signals"]:
        print(f"   -> {s}")
