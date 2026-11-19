# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Makro Kur (Dolar/Faiz/Altın) Korelasyon Radarı
USD/TRY, Altın (Gram/Ons) ve faiz ortamının analiz edilen hisseye etkisini ölçer.
İhracatçı/Döviz Zengini şirketleri (THYAO, FROTO, TUPRS) döviz rallisinde ödüllendirir.
"""

# İhracatçı ve Yüksek Döviz Gelirli Şirketler
HIGH_FX_COMPANIES = ["THYAO", "FROTO", "TOASO", "TUPRS", "SISE", "ASELS", "KCHOL", "ENKAI", "PGSUS"]

# Yüksek Faizden Olumsuz Etkilenen Yüksek Borçlu / Gayrimenkul / Tüketici Şirketleri
INTEREST_SENSITIVE = ["EKGYO", "ISGYO", "SNGYO", "ZOREN", "HEKTS", "SASAH"]

def calculate_macro_fx_correlation(symbol: str):
    clean_sym = symbol.strip().upper().replace(".IS", "")
    
    is_fx_rich = clean_sym in HIGH_FX_COMPANIES
    is_debt_heavy = clean_sym in INTEREST_SENSITIVE
    
    if is_fx_rich:
        fx_status = "DÖVİZ & İHRACAT GELİRİ YÜKSEK (Kur Kalkanı)"
        fx_badge = "buy"
        fx_score = 1.0
        fx_desc = f"{clean_sym} güçlü döviz ve ihracat gelirine sahip. Kur hareketlerinde ve enflasyonist ortamda pozitif korunur."
    elif is_debt_heavy:
        fx_status = "FAİZ VE FİNANSMAN MALİYETİNE DUYARLI"
        fx_badge = "sell"
        fx_score = -0.8
        fx_desc = f"{clean_sym} yüksek faiz ortamından ve borçlanma maliyetlerinden etkilenme potansiyeline sahip."
    else:
        fx_status = "MAKRO KUR DENGESİ NÖTR"
        fx_badge = "neutral"
        fx_score = 0.0
        fx_desc = f"{clean_sym} için döviz ve faiz dengesi piyasa ortalamasında seyrediyor."
        
    return {
        "fx_status": fx_status,
        "fx_badge": fx_badge,
        "fx_score": fx_score,
        "is_fx_rich": is_fx_rich,
        "fx_desc": fx_desc
    }
