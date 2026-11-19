# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Otomatik Destek, Direnç ve Pivot Seviyeleri (Milimetrik Fiyat Radarı)
Classic Pivot, Fibonacci Seviyeleri ve Kırılım Eşikleri (R1, R2, R3, S1, S2, S3)
"""

def calculate_pivot_points(high: float, low: float, close: float):
    """
    Önceki seansın Yüksek, Düşük ve Kapanış fiyatlarına göre 
    Classic ve Fibonacci Pivot noktalarını hesaplar.
    """
    pp = (high + low + close) / 3.0
    rng = high - low
    
    # Classic Pivot Seviyeleri
    r1 = (2 * pp) - low
    s1 = (2 * pp) - high
    r2 = pp + rng
    s2 = pp - rng
    r3 = high + 2 * (pp - low)
    s3 = low - 2 * (high - pp)
    
    # Fibonacci Pivot Seviyeleri
    fib_r1 = pp + (0.382 * rng)
    fib_r2 = pp + (0.618 * rng)
    fib_r3 = pp + (1.000 * rng)
    fib_s1 = pp - (0.382 * rng)
    fib_s2 = pp - (0.618 * rng)
    fib_s3 = pp - (1.000 * rng)
    
    # Mevcut Fiyatın Konumu
    if close >= r2:
        level_status = "GÜÇLÜ DİRENÇ ÜSTÜ (R2 Kırıldı, Ralli Alanı)"
        level_badge = "buy"
        level_score = 1.0
    elif close >= r1:
        level_status = "R1 DİRENCİ TEST EDİLİYOR"
        level_badge = "buy"
        level_score = 0.5
    elif close >= pp:
        level_status = "PİVOT ÜZERİNDE POZİTİF BÖLGEDE"
        level_badge = "buy"
        level_score = 0.5
    elif close <= s2:
        level_status = "AŞIRI SATIM DESTEK BÖLGESİ (S2 Seviyesi)"
        level_badge = "buy"  # Dip tepkisi potansiyeli
        level_score = 0.5
    else:
        level_status = "PİVOT ALTI BASKI (Destek Aranıyor)"
        level_badge = "sell"
        level_score = -0.5

    return {
        "pivot": round(pp, 2),
        "r1": round(r1, 2),
        "r2": round(r2, 2),
        "r3": round(r3, 2),
        "s1": round(s1, 2),
        "s2": round(s2, 2),
        "s3": round(s3, 2),
        "fib_r1": round(fib_r1, 2),
        "fib_r2": round(fib_r2, 2),
        "fib_s1": round(fib_s1, 2),
        "fib_s2": round(fib_s2, 2),
        "level_status": level_status,
        "level_badge": level_badge,
        "level_score": level_score,
        "summary": f"Ana Pivot: {round(pp,2)} TL | 1. Destek: {round(s1,2)} TL | 1. Direnç: {round(r1,2)} TL"
    }
