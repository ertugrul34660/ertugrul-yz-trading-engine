# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Para Giriş-Çıkışı (Money Flow & Balina Hacmi Radarı)
Hissenin MFI (Money Flow Index), Chaikin Para Akışı (CMF) ve hacimli kurumsal para girişini tespit eder.
"""

def calculate_money_flow(highs, lows, closes, volumes, period=14):
    """
    MFI (Money Flow Index) ve Net Kurumsal Para Akışı Analizi
    """
    if len(closes) < period + 1:
        return {
            "mfi": 50.0,
            "flow_status": "DENGELİ PARA AKIŞI",
            "flow_badge": "neutral",
            "flow_score": 0.0,
            "whale_inflow": False,
            "description": "Veri geçmişi yetersiz, para akışı dengeli."
        }
        
    typical_prices = [(highs[i] + lows[i] + closes[i]) / 3.0 for i in range(len(closes))]
    raw_money_flows = [typical_prices[i] * volumes[i] for i in range(len(closes))]
    
    pos_flow = 0.0
    neg_flow = 0.0
    
    # Son 14 bar
    start_idx = len(closes) - period
    for i in range(start_idx, len(closes)):
        if typical_prices[i] > typical_prices[i - 1]:
            pos_flow += raw_money_flows[i]
        elif typical_prices[i] < typical_prices[i - 1]:
            neg_flow += raw_money_flows[i]
            
    if neg_flow == 0:
        mfi = 100.0
    else:
        money_ratio = pos_flow / neg_flow
        mfi = 100.0 - (100.0 / (1.0 + money_ratio))
        
    mfi = round(mfi, 1)
    
    # Hacimli Balina Girişi Kontrolü (Son barda hacim 20 günlük ortalamanın 1.5 katı ve fiyat artıda)
    avg_vol = sum(volumes[-20:]) / 20 if len(volumes) >= 20 else volumes[-1]
    is_whale = (volumes[-1] > avg_vol * 1.4) and (closes[-1] >= closes[-2] if len(closes) > 1 else True)
    
    # Karar ve Puanlama
    flow_score = 0.0
    if mfi > 75:
        flow_status = "GÜÇLÜ KURUMSAL PARA GİRİŞİ (Akümülasyon)"
        flow_badge = "buy"
        flow_score = 2.0
    elif mfi >= 55:
        flow_status = "NET PARA GİRİŞİ POZİTİF"
        flow_badge = "buy"
        flow_score = 1.0
    elif mfi < 25:
        flow_status = "DİPTE PARA ÇIKIŞI BİTTİ (Toplama Bölgesi)"
        flow_badge = "buy"
        flow_score = 1.5
    elif mfi <= 40:
        flow_status = "NET PARA ÇIKIŞI VAR (Satıcılar Baskın)"
        flow_badge = "sell"
        flow_score = -1.5
    else:
        flow_status = "DENGELİ PARA AKIŞI"
        flow_badge = "neutral"
        flow_score = 0.0
        
    if is_whale and flow_score >= 0:
        flow_status += " + 🐋 BALİNA ALIMI TESPİT EDİLDİ"
        flow_score += 1.0
        
    return {
        "mfi": mfi,
        "flow_status": flow_status,
        "flow_badge": flow_badge,
        "flow_score": round(flow_score, 1),
        "whale_inflow": is_whale,
        "description": f"MFI (Para Akış Endeksi): {mfi}. Kurumsal alıcıların tahtadaki iştahı {'yüksek' if mfi>=50 else 'zayıf'}."
    }
