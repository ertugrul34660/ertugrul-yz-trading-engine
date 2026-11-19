import urllib.request
import json
import time

symbols = ['THYAO', 'GARAN', 'KCHOL', 'ASELS', 'ISCTR', 'TUPRS', 'AKBNK', 'BIMAS', 'EREGL', 'SISE', 'SAHOL', 'YKBNK']
candidates = []

for s in symbols:
    try:
        url = f'http://127.0.0.1:5055/api/analyze?symbol={s}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            d = json.loads(resp.read().decode('utf-8'))
            action = d.get('action')
            conf_str = d.get('confidence', '%0').replace('%', '').strip()
            conf = float(conf_str) if conf_str.replace('.', '').isdigit() else 50.0
            price = float(d.get('current_price') or 0)
            bofa = d.get('bofa_action', '')
            mf = d.get('money_flow', {}).get('flow_status', '')
            rsi = float(d.get('rsi') or 50)
            score = 0
            if action == 'AL': score += 50
            elif action == 'SAT': score -= 50
            score += conf * 0.3
            if 'ALIM' in bofa.upper() or 'POZİTİF' in bofa.upper() or 'SMART' in bofa.upper(): score += 15
            if 'POZİTİF' in mf.upper() or 'GİRİŞ' in mf.upper(): score += 15
            if 40 <= rsi <= 68: score += 10 # Saglikli yukselis
            
            candidates.append({
                'symbol': s,
                'price': price,
                'action': action,
                'confidence': conf,
                'bofa': bofa,
                'money_flow': mf,
                'rsi': rsi,
                'tp1': d.get('tp1_price'),
                'tp1_pct': d.get('tp1_pct'),
                'tp2': d.get('tp2_price'),
                'tp2_pct': d.get('tp2_pct'),
                'stop': d.get('stop_loss'),
                'risk': d.get('risk_badge'),
                'composite_score': round(score, 2)
            })
    except Exception as e:
        print(f'Hata {s}:', e)

candidates.sort(key=lambda x: x['composite_score'], reverse=True)
print('=== TITAN v7.0 EN YUKSEK POTANSIYELLI ADAYLAR ===')
for c in candidates:
    print(f"{c['symbol']:<6} | Fiyat: {c['price']:>6.2f} TL | Karar: {c['action']:<4} | Guven: %{c['confidence']:<2} | Skor: {c['composite_score']:>5} | BofA: {c['bofa'][:25]}")

with open('C:/Users/ertug/.gemini/antigravity/scratch/04-Finans-Borsa-ve-Ticaret/ertugrul-yz-alsat-botu/data/candidates.json', 'w', encoding='utf-8') as f:
    json.dump(candidates, f, ensure_ascii=False, indent=2)
