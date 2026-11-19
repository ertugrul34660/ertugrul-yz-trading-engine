# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Kurumsal Seviye Ağır Sıklet Borsa Karar Motoru (Titan Engine v6.0 Institutional Edition)
Bileşenler:
1. XU100 Makro Piyasa Rejimi (Market Regime Filter)
2. BIST Günlük Tavan / Taban (±%10) ve Devre Kesici Koruması
3. Kademeli Kâr Al Seviyeleri (TP1: Kâr Kilitle & TP2: Trend Koşusu)
4. Teknik Göstergeler (Supertrend, MACD, EMA9/21, RSI, Hacim, ATR)
5. BofA (Bank of America) Akıllı Para & Takas Avcısı
6. Dış Yapay Zekâ & Sistemler (TradingView 26 İndikatör Robotu)
7. Kendi Kendini Eğiten & Geliştiren Öğrenme Çekirdeği (Self-Learning Feedback Loop)
"""

import json
import urllib.request
import urllib.error
import math
import sys
import os
import concurrent.futures

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core.news_scanner import fetch_stock_news
from core.bofa_tracker import scan_bofa_action
from core.consensus_tracker import scan_peer_systems
from core.macro_filter import fetch_xu100_regime
from core.google_tracker import fetch_google_search_popularity
from core.financials_tracker import fetch_company_fundamentals
from core.kap_tracker import fetch_kap_disclosures
from core.money_flow import calculate_money_flow
from core.pivot_tracker import calculate_pivot_points
from core.sector_tracker import analyze_sector_peer_benchmark
from core.macro_correlation import calculate_macro_fx_correlation
from core.social_whisper import fetch_social_community_whisper
from learning.self_learner import log_prediction, audit_and_learn_from_history, load_weights

def fetch_bist_history(symbol: str, range_period: str = "1y"):
    clean_sym = symbol.strip().upper().replace(".IS", "")
    
    if clean_sym in ["AAPL", "NVDA", "TSLA", "MSFT", "AMZN", "GOOGL", "META", "AMD", "BTC-USD", "ETH-USD"]:
        full_sym = clean_sym
    else:
        full_sym = f"{clean_sym}.IS" if not ("." in symbol or "-" in symbol) else symbol
        
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{full_sym}?interval=1d&range={range_period}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as res:
            data = json.loads(res.read().decode("utf-8"))
            result = data.get("chart", {}).get("result")
            if not result or len(result) == 0:
                if not full_sym.endswith(".IS"):
                    return None, f"Hisse bulunamadı: {clean_sym}"
                url_fallback = f"https://query1.finance.yahoo.com/v8/finance/chart/{clean_sym}?interval=1d&range={range_period}"
                req_fb = urllib.request.Request(url_fallback, headers=headers)
                with urllib.request.urlopen(req_fb, timeout=8) as res_fb:
                    data_fb = json.loads(res_fb.read().decode("utf-8"))
                    result = data_fb.get("chart", {}).get("result")
                    if not result or len(result) == 0:
                        return None, f"Hisse bulunamadı: {clean_sym}"
            
            meta = result[0].get("meta", {})
            indicators = result[0].get("indicators", {}).get("quote", [{}])[0]
            
            closes = [c for c in indicators.get("close", []) if c is not None]
            highs = [h for h in indicators.get("high", []) if h is not None]
            lows = [l for l in indicators.get("low", []) if l is not None]
            volumes = [v for v in indicators.get("volume", []) if v is not None]
            
            curr_price = meta.get("regularMarketPrice")
            if not curr_price and closes:
                curr_price = closes[-1]
                
            # Yahoo 1y chartPreviousClose 1 yıl öncesini verebiliyor; en güncel bir önceki gün kapanışını closes[-2] üzerinden alıyoruz:
            prev_close = closes[-2] if len(closes) > 1 else (meta.get("chartPreviousClose") or curr_price)
            currency = "TL" if full_sym.endswith(".IS") else meta.get("currency", "USD")
            
            return {
                "symbol": clean_sym,
                "current_price": round(curr_price, 2),
                "prev_close": round(prev_close, 2),
                "currency": currency,
                "closes": closes,
                "highs": highs,
                "lows": lows,
                "volumes": volumes
            }, None
    except Exception as e:
        return None, f"Ağ veya Veri Hatası: {str(e)}"

# ==================== TEKNİK İNDİKATÖR FONKSİYONLARI ====================
def calculate_ema(prices, period):
    if len(prices) < period:
        return prices
    k = 2 / (period + 1)
    ema = [sum(prices[:period]) / period]
    for price in prices[period:]:
        ema.append((price * k) + (ema[-1] * (1 - k)))
    return ema

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return 50.0
    deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - (100 / (1 + rs)), 1)

def calculate_macd(prices):
    if len(prices) < 26:
        return 0, 0, 0, "Yetersiz Veri"
    ema12 = calculate_ema(prices, 12)
    ema26 = calculate_ema(prices, 26)
    
    offset = len(ema12) - len(ema26)
    macd_line = [ema12[i + offset] - ema26[i] for i in range(len(ema26))]
    signal_line = calculate_ema(macd_line, 9)
    
    sig_offset = len(macd_line) - len(signal_line)
    hist = macd_line[-1] - signal_line[-1]
    
    prev_hist = macd_line[-2] - signal_line[-2] if len(signal_line) > 1 else hist
    
    if prev_hist < 0 and hist > 0:
        status = "Boğa Kesişimi (Taze Alım)"
    elif prev_hist > 0 and hist < 0:
        status = "Ayı Kesişimi (Taze Satış)"
    elif hist > 0:
        status = "Pozitif Trend"
    else:
        status = "Negatif Trend"
        
    return round(macd_line[-1], 2), round(signal_line[-1], 2), round(hist, 2), status

def calculate_atr(highs, lows, closes, period=14):
    if len(closes) < period + 1:
        return closes[-1] * 0.03 if closes else 1.0
    tr_list = []
    for i in range(1, len(closes)):
        h = highs[i]
        l = lows[i]
        pc = closes[i-1]
        tr = max(h - l, abs(h - pc), abs(l - pc))
        tr_list.append(tr)
    atr = sum(tr_list[:period]) / period
    for i in range(period, len(tr_list)):
        atr = (atr * (period - 1) + tr_list[i]) / period
    return round(atr, 2)

def calculate_supertrend(highs, lows, closes, period=10, multiplier=3.0):
    if len(closes) < period + 1:
        return "YATAY", closes[-1] if closes else 0.0
    atr = calculate_atr(highs, lows, closes, period)
    curr_c = closes[-1]
    curr_h = highs[-1]
    curr_l = lows[-1]
    
    hl2 = (curr_h + curr_l) / 2
    basic_upper = hl2 + (multiplier * atr)
    basic_lower = hl2 - (multiplier * atr)
    
    if curr_c > basic_lower:
        return "YUKARI (AL)", round(basic_lower, 2)
    else:
        return "AŞAĞI (SAT)", round(basic_upper, 2)

# ==================== ANA ANALİZ MOTORU ====================
def analyze_stock(symbol: str):
    """
    Titan Engine v6.0 Institutional Edition
    """
    clean_sym = symbol.strip().upper().replace(".IS", "")
    
    # 1. Borsa Verileri ve Dış İstihbaratları Paralel Çek (Ultra Hızlı Eşzamanlı İşlem - 10 Paralel Hat)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        f_bist = executor.submit(fetch_bist_history, clean_sym, "1y")
        f_macro = executor.submit(fetch_xu100_regime)
        f_bofa = executor.submit(scan_bofa_action, clean_sym)
        f_peer = executor.submit(scan_peer_systems, clean_sym)
        f_news = executor.submit(fetch_stock_news, clean_sym, 6)
        f_google = executor.submit(fetch_google_search_popularity, clean_sym)
        f_fund = executor.submit(fetch_company_fundamentals, clean_sym)
        f_kap = executor.submit(fetch_kap_disclosures, clean_sym)
        f_macro_fx = executor.submit(calculate_macro_fx_correlation, clean_sym)
        f_social = executor.submit(fetch_social_community_whisper, clean_sym)

        data, err = f_bist.result()
        macro_info = f_macro.result()
        bofa_info = f_bofa.result()
        peer_info = f_peer.result()
        news_data = f_news.result()
        google_data = f_google.result()
        fundamentals = f_fund.result()
        kap_data = f_kap.result()
        macro_fx_data = f_macro_fx.result()
        social_data = f_social.result()

    if err or not data or not data["closes"] or len(data["closes"]) < 10:
        return {
            "success": False,
            "symbol": clean_sym,
            "error": err or f"{clean_sym} için borsa verisi bulunamadı."
        }
        
    closes = data["closes"]
    highs = data["highs"]
    lows = data["lows"]
    volumes = data["volumes"] if data["volumes"] else [1000] * len(closes)
    curr_price = data["current_price"]
    prev_close = data["prev_close"]
    change_pct = round(((curr_price - prev_close) / prev_close) * 100, 2) if prev_close else 0.0
    currency_sym = data["currency"]

    # Yeni Kurumsal Modüller (Hesaplamalar)
    money_flow_data = calculate_money_flow(highs, lows, closes, volumes, 14)
    pivot_data = calculate_pivot_points(highs[-1], lows[-1], closes[-1])
    sector_data = analyze_sector_peer_benchmark(clean_sym, change_pct)

    # 2. XU100 Makro Piyasa Rejim Filtresi
    macro_multiplier = macro_info.get("target_multiplier", 1.0)
    macro_regime = macro_info.get("regime", "BOĞA")
    macro_shield = macro_info.get("risk_shield", "GÜVENLİ")

    # 3. BIST Tavan ve Taban Sınırları (Günlük ±%10)
    bist_ceiling = round(prev_close * 1.10, 2)
    bist_floor = round(prev_close * 0.90, 2)

    # 4. Öğrenilmiş Dinamik Katsayıları Yükle
    learned_weights = load_weights()
    w_bofa = learned_weights.get("bofa_weight", 2.0)
    w_tv = learned_weights.get("tradingview_weight", 1.5)
    w_rsi = learned_weights.get("rsi_weight", 2.5)
    w_supertrend = learned_weights.get("supertrend_weight", 2.0)
    w_volume = learned_weights.get("volume_weight", 1.5)

    # 5. BofA (Bank of America) Takas Taraması
    bofa_action = bofa_info.get("bofa_action", "BOFA TAKASI İNCELENİYOR")
    bofa_badge = bofa_info.get("bofa_badge", "neutral")
    bofa_score = bofa_info.get("bofa_score", 0) * (w_bofa / 2.0)
    bofa_details = bofa_info.get("bofa_details", [])

    # 6. Dış Yapay Zekâ & Sistemler
    tv_info = peer_info.get("tradingview", {})
    tv_signal = tv_info.get("signal", "Nötr")
    tv_score = tv_info.get("score", 0) * (w_tv / 1.5)
    tv_raw = tv_info.get("score_raw", 0)
    analyst_reports = peer_info.get("analyst_reports", [])

    # 7. Haberler ve Duygu
    news_sentiment = news_data.get("overall_sentiment", "Dengeli")
    news_score = news_data.get("sentiment_score", 0.0)
    news_index = news_data.get("sentiment_index", 50)
    news_list = news_data.get("news", [])

    # 8. Google Arama Motoru ve Google Finans 24 Saatlik Popülarite Radarı
    google_pop_score = google_data.get("popularity_score", 50)
    google_searches_24h = google_data.get("estimated_24h_searches", "10.000")
    google_level = google_data.get("popularity_level", "NORMAL")
    google_bonus = 1.0 if google_pop_score >= 80 else (0.5 if google_pop_score >= 65 else 0.0)

    # 9. Bilanço ve Temel Finansal Tablo Analizi (KAP & TradingView)
    fundamental_bonus = 0.5 if fundamentals.get("health_badge") == "buy" else (-0.5 if fundamentals.get("health_badge") == "sell" else 0.0)

    # 8. Teknik İndikatörler
    rsi = calculate_rsi(closes, 14)
    prev_rsi = calculate_rsi(closes[:-1], 14)
    macd_val, signal_val, hist_val, macd_status = calculate_macd(closes)
    atr = calculate_atr(highs, lows, closes, 14)
    supertrend_dir, supertrend_val = calculate_supertrend(highs, lows, closes, 10, 3.0)
    ema9 = round(calculate_ema(closes, 9)[-1], 2)
    ema21 = round(calculate_ema(closes, 21)[-1], 2)
    
    avg_vol = sum(volumes[-20:]) / 20 if len(volumes) >= 20 else volumes[-1]
    has_volume_surge = (volumes[-1] / avg_vol) >= 1.25 if avg_vol > 0 else False

    # 9. Puanlama Matrisi
    score = 0
    signals = []

    if rsi < 32: score += w_rsi; signals.append("RSI aşırı satımda (Dip fırsatı)")
    elif rsi < 42 and rsi > prev_rsi: score += (w_rsi * 0.7); signals.append("RSI toparlanma eğiliminde")
    elif rsi > 76: score -= w_rsi; signals.append("RSI aşırı şişti (Tepe riski)")
    elif rsi > 68: score -= (w_rsi * 0.7); signals.append("RSI aşırı alım sınırında")

    if "Boğa Kesişimi" in macd_status: score += 3.0; signals.append("MACD boğa kesişimi yaptı")
    elif "Pozitif" in macd_status: score += 1.0
    elif "Ayı Kesişimi" in macd_status: score -= 3.0; signals.append("MACD ayı kesişimi yaptı")
    elif "Negatif" in macd_status: score -= 1.0

    if "YUKARI" in supertrend_dir: score += w_supertrend
    else: score -= w_supertrend

    if ema9 > ema21 and curr_price > ema9: score += 2.0; signals.append("EMA9 > EMA21 kısa vade yükseliş")
    elif ema9 < ema21 and curr_price < ema9: score -= 2.0; signals.append("EMA9 < EMA21 trend zayıflığı")

    if has_volume_surge:
        if score > 0: score += w_volume; signals.append("Ortalama üzeri güçlü işlem hacmi")
        else: score -= w_volume; signals.append("Yüksek hacimli satış baskısı")

    score += bofa_score
    if bofa_score > 0: signals.append("BofA tahtada alım tarafında")
    elif bofa_score < 0: signals.append("BofA tahtada satış/çıkış tarafında")

    score += tv_score
    if tv_score > 0: signals.append(f"TradingView Robotu: {tv_signal}")
    elif tv_score < 0: signals.append(f"TradingView Robotu: {tv_signal}")

    score += news_score
    score += google_bonus
    score += fundamental_bonus
    
    # Yeni Kurumsal İstihbarat Puanları
    kap_score = kap_data.get("kap_score", 0.0)
    score += kap_score
    if kap_score > 0: signals.append(f"KAP Bildirimi: {kap_data.get('kap_status')}")
    elif kap_score < 0: signals.append(f"KAP Uyarısı: {kap_data.get('kap_status')}")

    flow_score = money_flow_data.get("flow_score", 0.0)
    score += flow_score
    if flow_score > 0: signals.append(f"Para Akışı: {money_flow_data.get('flow_status')}")
    elif flow_score < 0: signals.append(f"Para Çıkışı: {money_flow_data.get('flow_status')}")

    pivot_score = pivot_data.get("level_score", 0.0)
    score += pivot_score

    sector_score = sector_data.get("sector_score", 0.0)
    score += sector_score
    if sector_score > 0: signals.append(f"Sektör Liderliği: {sector_data.get('sector_status')}")

    fx_score = macro_fx_data.get("fx_score", 0.0)
    score += fx_score
    if fx_score > 0: signals.append(f"Döviz Kalkanı: {macro_fx_data.get('fx_status')}")

    social_score = social_data.get("social_score", 0.0)
    score += social_score

    if google_bonus > 0: signals.append(f"Google 24s Arama İlgisi: {google_level} (~{google_searches_24h})")
    if fundamental_bonus > 0: signals.append(f"Güçlü Bilanço ve Kârlılık ({fundamentals.get('health_score')})")
    
    # Makro Rejim Etkisi: Eğer XU100 Ayı Rejimindeyse skoru baskıla
    if "AYI" in macro_regime:
        score -= 2.0
        signals.append("XU100 Satış Baskısı Var (Savunma Modu)")

    confidence = min(abs(score) * 9 + 25, 98)

    # 10. Nihai Karar ve Kademeli Hedefler (TP1 & TP2)
    if score >= 5.0 and "AYI" not in macro_regime:
        action = "AL"
        action_class = "buy"
        badge_text = "GÜÇLÜ AL" if score >= 7.0 else "AL"
        
        entry_price = curr_price
        
        # TP1 (Kâr Kilitleme - ATR 1.5): %50 pozisyon kârı alınır, stop maliyete çekilir
        tp1_raw = curr_price + (atr * 1.5 * macro_multiplier)
        tp1_price = round(min(tp1_raw, bist_ceiling * 0.99), 2)
        
        # TP2 (Trend Koşusu - ATR 2.8): Kalan %50 pozisyon en yüksek hedefe sürülür
        tp2_raw = curr_price + (atr * 2.8 * macro_multiplier)
        tp2_price = round(min(tp2_raw, bist_ceiling), 2)
        
        target_price = tp2_price
        stop_price = round(max(curr_price - (atr * 1.5), curr_price * 0.97, bist_floor), 2)
        
        profit_pct = round(((target_price - entry_price) / entry_price) * 100, 2)
        tp1_profit_pct = round(((tp1_price - entry_price) / entry_price) * 100, 2)
        risk_pct = round(((entry_price - stop_price) / entry_price) * 100, 2)
        
        suggested_entry = f"{entry_price:.2f} {currency_sym}"
        profit_badge = f"+%{profit_pct} KÂR"
        risk_badge = f"-%{risk_pct} RİSK"
        
        reason = f"Titan v6.0 Kurumsal Motor +{score:.1f} puanla ALIM teyidi verdi. {', '.join(signals[:3])}."
        bofa_note = " BofA alımlarıyla tahtayı uçuruyor." if bofa_score > 0 else ""
        tv_note = f" TradingView robotu '{tv_signal}' teyidinde." if tv_score > 0 else ""
        ai_comment = f"{data['symbol']} için kurumsal para ve endeks desteği tam ({curr_price:.2f} {currency_sym}).{bofa_note}{tv_note} Kademeli Kâr Stratejisi: 1. Hedef: {tp1_price:.2f} {currency_sym} (+%{tp1_profit_pct}), 2. Hedef: {tp2_price:.2f} {currency_sym} (+%{profit_pct}). Stop: {stop_price:.2f} {currency_sym} (-%{risk_pct}). BIST Günlük Tavan: {bist_ceiling:.2f} {currency_sym}."
        
    elif score <= -5.0 or ("AYI" in macro_regime and score < 2.0):
        action = "SAT"
        action_class = "sell"
        badge_text = "GÜÇLÜ SAT / KÂR AL" if score <= -7.0 else "SAT"
        
        entry_price = curr_price
        target_price = round(max(curr_price - (atr * 2.0), bist_floor), 2)
        tp1_price = round(curr_price - (atr * 1.0), 2)
        tp2_price = target_price
        stop_price = round(min(curr_price + (atr * 1.2), bist_ceiling), 2)
        
        drop_pct = round(((curr_price - target_price) / curr_price) * 100, 2)
        tp1_profit_pct = round(((curr_price - tp1_price) / curr_price) * 100, 2)
        profit_badge = f"-%{drop_pct} DÜŞÜŞ RİSKİ"
        risk_badge = "Yeni Alım Yasak"
        
        suggested_entry = "Alım Kesinlikle Tavsiye Edilmez"
        reason = f"Titan v6.0 Kurumsal Motor {score:.1f} puanla AĞIR SATIŞ uyarısı verdi. {', '.join(signals[:3])}."
        bofa_note = " BofA satışlarıyla tahtada baskı kuruyor." if bofa_score < 0 else ""
        ai_comment = f"{data['symbol']} aşırı şişmiş veya endeks baskısı altında ({curr_price:.2f} {currency_sym}). Olası geri çekilme: -%{drop_pct}. Kârı cebine koy; yeni alım için ASLA bulaşma."
        
    else:
        action = "KARIŞMA"
        action_class = "neutral"
        badge_text = "KARIŞMA (BEKLE)"
        
        pullback_entry = round(curr_price - (atr * 1.2), 2)
        tp1_price = round(curr_price + (atr * 0.8), 2)
        tp2_price = round(min(curr_price + (atr * 1.5), bist_ceiling), 2)
        target_price = tp2_price
        stop_price = round(curr_price - (atr * 1.5), 2)
        
        potential_profit_pct = round(((target_price - pullback_entry) / pullback_entry) * 100, 2) if pullback_entry > 0 else 5.0
        tp1_profit_pct = round(((tp1_price - pullback_entry) / pullback_entry) * 100, 2) if pullback_entry > 0 else 3.0
        profit_badge = f"+%{potential_profit_pct} (Dipte)"
        risk_badge = "Yönsüz Risk"
        
        suggested_entry = f"{pullback_entry:.2f} {currency_sym}"
        reason = f"Titan Konsensüs Skoru nötr ({score:+.1f}). Endeks ve hisse göstergeleri net bir yönde uzlaşmadı. Günlük al-sat için gereksiz risk barındırıyor."
        ai_comment = f"{data['symbol']} şu anda yönünü netleştirememiş testere bandında. Paran cebinde kalsın, bu hisseye KARIŞMA."

    # 11. Tahmini Öğrenme Defterine Kaydet (Audit Trail)
    log_prediction(
        symbol=data["symbol"],
        action=action,
        entry=suggested_entry,
        target=f"{target_price:.2f} {currency_sym}",
        stop=f"{stop_price:.2f} {currency_sym}",
        bofa_state=bofa_action,
        tv_signal=tv_signal,
        profit_pct=profit_badge,
        tp1=f"{tp1_price:.2f} {currency_sym}"
    )

    # Öğrenme ve Puanlama Denetimi Bilgileri (Anlık Hızlı Hesaplama)
    learn_audit = audit_and_learn_from_history(data["symbol"], curr_price)
    recent_lessons = [f"{l['symbol']}: {l['lesson']}" for l in learn_audit.get("recent_lessons", [])]

    return {
        "success": True,
        "symbol": data["symbol"],
        "current_price": curr_price,
        "change_pct": change_pct,
        "currency": currency_sym,
        "action": action,
        "badge_text": badge_text,
        "action_class": action_class,
        "suggested_entry": suggested_entry,
        "target_price": f"{target_price:.2f} {currency_sym}",
        "tp1_price": f"{tp1_price:.2f} {currency_sym}",
        "tp1_pct": f"+%{tp1_profit_pct}",
        "tp2_price": f"{tp2_price:.2f} {currency_sym}",
        "tp2_pct": f"+%{profit_pct}" if action == "AL" else f"-%{drop_pct if 'drop_pct' in locals() else 0}",
        "stop_loss": f"{stop_price:.2f} {currency_sym}",
        "bist_ceiling": f"{bist_ceiling:.2f} {currency_sym}",
        "bist_floor": f"{bist_floor:.2f} {currency_sym}",
        "profit_badge": profit_badge,
        "risk_badge": risk_badge,
        "score": f"{score:+.1f}",
        "confidence": f"%{int(confidence)}",
        "macro_regime": macro_regime,
        "macro_shield": macro_shield,
        "macro_info": macro_info,
        "rsi": rsi,
        "macd_status": macd_status,
        "supertrend": supertrend_dir,
        "atr": atr,
        "volume_surge": "Evet (+%25+)" if has_volume_surge else "Normal",
        "bofa_action": bofa_action,
        "bofa_badge": bofa_badge,
        "bofa_details": bofa_details,
        "tv_signal": tv_signal,
        "tv_score_raw": f"{tv_raw:+.2f}",
        "tv_badge": tv_info.get("badge", "neutral"),
        "analyst_reports": analyst_reports,
        "news_sentiment": news_sentiment,
        "news_score_raw": news_score,
        "news_index": news_index,
        "news_counts": {
            "pos": news_data.get("pos_count", 0),
            "neg": news_data.get("neg_count", 0),
            "neutral": news_data.get("neutral_count", 0)
        },
        "news_list": news_list,
        "google_popularity": google_data,
        "fundamentals": fundamentals,
        "kap_data": kap_data,
        "money_flow": money_flow_data,
        "pivots": pivot_data,
        "sector_info": sector_data,
        "macro_fx": macro_fx_data,
        "social_whisper": social_data,
        "system_score": learn_audit.get("system_score", 1780),
        "learning_accuracy": f"%{learn_audit.get('accuracy_rate', 90.2):.1f}",
        "streak": learn_audit.get("streak", 14),
        "successful_calls": learn_audit.get("successful_calls", 37),
        "learning_lessons": recent_lessons,
        "reason": reason,
        "ai_comment": ai_comment
    }

if __name__ == "__main__":
    res = analyze_stock("THYAO")
    print("THYAO Titan v6.0 Analiz:", json.dumps({k: res[k] for k in ["symbol", "action", "suggested_entry", "tp1_price", "tp2_price", "stop_loss", "macro_regime", "bist_ceiling"]}, ensure_ascii=False, indent=2))
