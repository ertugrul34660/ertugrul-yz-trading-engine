# -*- coding: utf-8 -*-
import urllib.request
import json

queries = ['quantitative-trading+language:python', 'trading-bot+stars:>5000']
print("=== DÜNYA STANDARTLARINDA GITHUB QUANT TRADING REPOLARI TARAMASI ===")

for q in queries:
    url = f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page=5"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for item in data.get('items', [])[:4]:
                name = item.get('full_name')
                stars = item.get('stargazers_count')
                desc = item.get('description') or ''
                print(f"★ {stars:>6} Stars | {name:<35} | {desc[:90]}")
    except Exception as e:
        print("Hata:", e)
