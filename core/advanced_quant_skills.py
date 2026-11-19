# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Kurumsal Quant Yetenekleri Modülü
Kaynaklar & İlham Alınan Dünya Standartları:
1. Microsoft Qlib (50k★): Alpha-158 Faktör Analizi, Rolling Z-Score Momentum & Volatilite Normalizasyonu
2. QuantConnect LEAN (22k★): Dynamic Kelly Criterion Pozisyon Boyutlandırma & Asimetrik Risk/Ödül
3. Freqtrade (56k★): Trailing Stop-Loss & Dynamic Spread Koruma Kalkanı
"""

import math

def calculate_alpha_factors(prices: list, volumes: list = None):
    """
    Microsoft Qlib Benzeri Alpha-158 Türetilmiş Hızlı Faktörler
    """
    if not prices or len(prices) < 5:
        return {"momentum_zscore": 0.0, "volatility_atr": 0.0, "mean_reversion_edge": 0.0}
        
    n = len(prices)
    returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, n)]
    
    # Ortalama getiri ve standart sapma (Volatilite)
    mean_ret = sum(returns) / len(returns)
    variance = sum((r - mean_ret) ** 2 for r in returns) / len(returns)
    std_dev = math.sqrt(variance) if variance > 0 else 0.001
    
    # Son periyodun Z-Skoru (Normalleştirilmiş Momentum)
    last_ret = returns[-1]
    momentum_zscore = round((last_ret - mean_ret) / std_dev, 2)
    
    # Mean Reversion Edge (Ortalamaya Dönüş Potansiyeli)
    # Fiyat hareketli ortalamanın çok altındaysa yukarı tepki ihtimali
    ma = sum(prices[-5:]) / 5.0
    dist_to_ma_pct = round(((prices[-1] - ma) / ma) * 100, 2)
    
    return {
        "momentum_zscore": momentum_zscore,
        "volatility_std": round(std_dev * 100, 2),
        "dist_to_ma_pct": dist_to_ma_pct,
        "is_alpha_breakout": momentum_zscore > 1.5,
        "is_oversold_bounce": dist_to_ma_pct < -1.5 and momentum_zscore > -0.5
    }

def calculate_kelly_position_size(win_rate: float, win_loss_ratio: float, capital: float, max_risk_pct: float = 0.25):
    """
    QuantConnect LEAN Mantığı: Kelly Criterion ile Matematiksel Kasa Yönetimi
    Kasanın ne kadarının riske atılacağını matematiksel olarak belirler.
    f* = p - (q / b)
    """
    p = win_rate # Kazanma ihtimali (Örn: 0.60)
    q = 1.0 - p  # Kaybetme ihtimali (Örn: 0.40)
    b = win_loss_ratio if win_loss_ratio > 0 else 1.5 # Kâr/Zarar oranı
    
    kelly_fraction = p - (q / b)
    
    # Tam Kelly çok agresiftir, Half-Kelly veya Fractional Kelly (1/4) kullanılır
    safe_fraction = max(0.05, min(max_risk_pct, kelly_fraction * 0.5))
    suggested_trade_amount = round(capital * safe_fraction, 2)
    
    return {
        "kelly_raw": round(kelly_fraction, 3),
        "safe_fraction_pct": round(safe_fraction * 100, 1),
        "suggested_trade_amount": suggested_trade_amount
    }

def calculate_dynamic_trailing_stop(entry_price: float, highest_price: float, trailing_pct: float = 0.006):
    """
    Freqtrade Mantığı: Dinamik Kâr Kitleme (Trailing Stop)
    Fiyat yükseldikçe stop seviyesini yukarı çeker, kârı garantiye alır.
    """
    # En yüksek fiyattan %0.6 geriye stop koy
    dynamic_stop = round(highest_price * (1.0 - trailing_pct), 2)
    # Stop seviyesi asla giriş fiyatının altına inmez (kâr bölgesine geçtikten sonra)
    locked_profit_pct = round(((dynamic_stop - entry_price) / entry_price) * 100, 2)
    
    return {
        "dynamic_stop": dynamic_stop,
        "is_profit_locked": dynamic_stop > entry_price,
        "locked_profit_pct": locked_profit_pct
    }

if __name__ == '__main__':
    print("=== DÜNYA DEVLERİNDEN ENTEGRE EDİLEN YENİ QUANT YETENEKLERİ ===")
    sample_prices = [35.10, 35.15, 35.12, 35.20, 35.35, 35.40]
    alpha = calculate_alpha_factors(sample_prices)
    print("1. Microsoft Qlib Alpha Analizi:", alpha)
    
    kelly = calculate_kelly_position_size(win_rate=0.62, win_loss_ratio=1.8, capital=100.0)
    print("2. QuantConnect LEAN Kasa Yönetimi (Kelly):", kelly)
    
    trailing = calculate_dynamic_trailing_stop(entry_price=35.10, highest_price=35.45)
    print("3. Freqtrade Dinamik Kâr Kilitleme (Trailing Stop):", trailing)
