import pandas as pd
import numpy as np

class BISTTechnicalAnalyzer:
    def __init__(self, rsi_period=14, ema_short=20, ema_long=50):
        self.rsi_period = rsi_period
        self.ema_short = ema_short
        self.ema_long = ema_long

    def calculate_indicators(self, df):
        """
        Kapanış (Close) fiyatlarını içeren DataFrame üzerine
        RSI, MACD ve EMA indikatörlerini ekler.
        """
        data = df.copy()

        # 1. Üstel Hareketli Ortalamalar (EMA 20 ve EMA 50)
        data['EMA_Short'] = data['Close'].ewm(span=self.ema_short, adjust=False).mean()
        data['EMA_Long'] = data['Close'].ewm(span=self.ema_long, adjust=False).mean()

        # 2. RSI (Göreceli Güç Endeksi - Wilder's Smoothing yöntemi)
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).ewm(alpha=1/self.rsi_period, adjust=False).mean()
        loss = (-delta.where(delta < 0, 0)).ewm(alpha=1/self.rsi_period, adjust=False).mean()
        
        rs = gain / (loss.replace(0, np.nan))
        data['RSI'] = 100 - (100 / (1 + rs))
        data['RSI'] = data['RSI'].fillna(50.0)

        # 3. MACD (12, 26, 9 Standart Parametreler)
        ema_12 = data['Close'].ewm(span=12, adjust=False).mean()
        ema_26 = data['Close'].ewm(span=26, adjust=False).mean()
        data['MACD'] = ema_12 - ema_26
        data['MACD_Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
        data['MACD_Hist'] = data['MACD'] - data['MACD_Signal']

        return data

    def generate_signal(self, df):
        """
        Son mum verisine göre otonom ajan için AL / SAT / BEKLE kararı üretir.
        """
        analyzed_df = self.calculate_indicators(df)
        
        if len(analyzed_df) < 2:
            return {"signal": "BEKLE", "reason": "Yetersiz geçmiş veri."}

        # Son iki satırı al (kesişimleri yakalamak için)
        prev = analyzed_df.iloc[-2]
        curr = analyzed_df.iloc[-1]

        rsi_val = round(curr['RSI'], 2)
        macd_val = round(curr['MACD'], 4)
        macd_sig = round(curr['MACD_Signal'], 4)
        ema_s = round(curr['EMA_Short'], 2)
        ema_l = round(curr['EMA_Long'], 2)

        # --- ALIM KOŞULLARI ---
        # 1. RSI aşırı satım bölgesinden (35 altı) yukarı dönüyorsa
        # 2. MACD çizgisi Sinyal çizgisini yukarı kesiyorsa
        # 3. Kısa vadeli EMA, uzun vadeli EMA üzerindeyse (Yükseliş trendi teyidi)
        macd_bullish_cross = (prev['MACD'] <= prev['MACD_Signal']) and (curr['MACD'] > curr['MACD_Signal'])
        trend_up = curr['EMA_Short'] > curr['EMA_Long']

        if (curr['RSI'] < 45 and macd_bullish_cross) or (trend_up and macd_bullish_cross and curr['RSI'] < 65):
            return {
                "signal": "AL",
                "price": float(curr['Close']),
                "rsi": rsi_val,
                "macd": macd_val,
                "reason": f"MACD yukarı kesiş yaptı, RSI ({rsi_val}) uygun seviyede ve trend pozitif."
            }

        # --- SATIM KOŞULLARI ---
        # 1. RSI aşırı alım bölgesine (70 üstü) ulaştıysa
        # 2. VEYA MACD çizgisi Sinyal çizgisini aşağı kesiyorsa
        macd_bearish_cross = (prev['MACD'] >= prev['MACD_Signal']) and (curr['MACD'] < curr['MACD_Signal'])

        if curr['RSI'] > 70 or macd_bearish_cross:
            return {
                "signal": "SAT",
                "price": float(curr['Close']),
                "rsi": rsi_val,
                "macd": macd_val,
                "reason": f"Aşırı alım bölgesi (RSI: {rsi_val}) veya MACD aşağı kesişi tespit edildi."
            }

        return {
            "signal": "BEKLE",
            "price": float(curr['Close']),
            "rsi": rsi_val,
            "macd": macd_val,
            "reason": "Belirgin bir kesişim veya aşırı alım/satım sinyali yok."
        }

if __name__ == "__main__":
    np.random.seed(42)
    fiyatlar = np.cumsum(np.random.randn(60) * 0.5) + 50.0
    ornek_df = pd.DataFrame({'Close': fiyatlar})

    analyzer = BISTTechnicalAnalyzer()
    karar = analyzer.generate_signal(ornek_df)
    print(f"Son Fiyat: {round(karar['price'], 2)} TL | Sinyal: {karar['signal']} | Neden: {karar['reason']}")
