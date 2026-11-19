import urllib.request
import json
import time

symbols = ['THYAO', 'GARAN', 'ASELS', 'KCHOL', 'TUPRS', 'ISCTR', 'AKBNK', 'BIMAS', 'EREGL', 'SISE', 'SAHOL', 'YKBNK']
candidates = []

print("=== 10 DAKIKALIK HIZLI SCALPING MOTORU: EN YUKSEK MOMENTUM TARAMASI ===")

for s in symbols:
    try:
        url = f'http://127.0.0.1:5055/api/analyze?symbol={s}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            d = json.loads(resp.read().decode('utf-8'))
            price = float(d.get('current_price') or 0.0)
            change = float(d.get('change_pct') or 0.0)
            rsi = float(d.get('rsi') or 50.0)
            vol_str = d.get('volume_surge', '1.0x')
            vol = float(vol_str.split('x')[0]) if 'x' in vol_str else 1.0
            tv = d.get('tv_signal', 'BEKLE')
            
            # Scalping Skoru: Fiyat hareketliliği + Hacim desteği + Pozitif RSI
            score = 0
            if change > 0: score += 40
            if '1.5' in vol_str or '2.' in vol_str or vol > 1.3: score += 30
            if 50 <= rsi <= 72: score += 20
            if 'AL' in tv.upper(): score += 10
            
            candidates.append({
                'symbol': s,
                'price': price,
                'change_pct': change,
                'rsi': rsi,
                'volume': vol_str,
                'tv': tv,
                'scalp_score': score
            })
    except Exception as e:
        pass

candidates.sort(key=lambda x: x['scalp_score'], reverse=True)
for c in candidates[:5]:
    print(f"{c['symbol']:<6} | Fiyat: {c['price']:>6.2f} TL | Değişim: %{c['change_pct']:>5.2f} | RSI: {c['rsi']:>4.1f} | Hacim: {c['volume']} | Skor: {c['scalp_score']}")
