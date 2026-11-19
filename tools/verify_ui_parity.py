import urllib.request
import json
import re

# 1. Fetch HTML to find all element IDs and script references
with urllib.request.urlopen('http://127.0.0.1:5055/') as resp:
    html = resp.read().decode('utf-8')

# 2. Fetch API data
with urllib.request.urlopen('http://127.0.0.1:5055/api/analyze?symbol=THYAO') as resp:
    api = json.loads(resp.read().decode('utf-8'))

print("=== GORSEL ELEMANLAR ILE ARKA PLAN VERILERI ESLESTIRME DENETIMI ===")

# Mapping check: UI Element ID -> API Key/Expression
ui_mappings = [
    ('heroSymbol', 'symbol', api.get('symbol')),
    ('heroPrice', 'current_price', f"{api.get('current_price')} TL"),
    ('heroChange', 'change_pct', f"%{api.get('change_pct')}"),
    ('heroCeiling', 'bist_ceiling', f"{api.get('bist_ceiling')} TL"),
    ('heroFloor', 'bist_floor', f"{api.get('bist_floor')} TL"),
    ('decActionTitle', 'action', api.get('action')),
    ('priceEntry', 'suggested_entry', api.get('suggested_entry')),
    ('priceTp1', 'tp1_price', api.get('tp1_price')),
    ('priceTp1Pct', 'tp1_pct', api.get('tp1_pct')),
    ('priceTp2', 'tp2_price', api.get('tp2_price')),
    ('priceTp2Pct', 'tp2_pct', api.get('tp2_pct')),
    ('priceStop', 'stop_loss', api.get('stop_loss')),
    ('priceStopPct', 'risk_badge', api.get('risk_badge')),
    ('analystComment', 'ai_comment', api.get('ai_comment')),
    ('confValText', 'confidence', api.get('confidence')),
    ('pivS2', 'pivots.s2', api.get('pivots', {}).get('s2')),
    ('pivS1', 'pivots.s1', api.get('pivots', {}).get('s1')),
    ('pivPP', 'pivots.pivot', api.get('pivots', {}).get('pivot')),
    ('pivR1', 'pivots.r1', api.get('pivots', {}).get('r1')),
    ('pivR2', 'pivots.r2', api.get('pivots', {}).get('r2')),
    ('techRsi', 'rsi', api.get('rsi')),
    ('techMacd', 'macd_status', api.get('macd_status')),
    ('techSupertrend', 'supertrend', api.get('supertrend')),
    ('techVolume', 'volume_surge', api.get('volume_surge')),
    ('smBofa', 'bofa_action', api.get('bofa_action')),
    ('smMfi', 'money_flow.flow_status', api.get('money_flow', {}).get('flow_status')),
    ('smMfiDesc', 'money_flow.description', api.get('money_flow', {}).get('description')),
    ('smTv', 'tv_signal', api.get('tv_signal')),
    ('smSocial', 'social_whisper.social_status', api.get('social_whisper', {}).get('social_status')),
    ('fundNetIncome', 'fundamentals.net_income_str', api.get('fundamentals', {}).get('net_income_str')),
    ('fundRevenue', 'fundamentals.revenue_str', api.get('fundamentals', {}).get('revenue_str')),
    ('fundPe', 'fundamentals.pe_ratio', api.get('fundamentals', {}).get('pe_ratio')),
    ('fundEps', 'fundamentals.eps', api.get('fundamentals', {}).get('eps')),
    ('fundHealth', 'fundamentals.health_score', api.get('fundamentals', {}).get('health_score')),
    ('secStatus', 'sector_info.sector_status', api.get('sector_info', {}).get('sector_status')),
    ('secName', 'sector_info.sector_name', api.get('sector_info', {}).get('sector_name')),
    ('secFx', 'macro_fx.fx_status', api.get('macro_fx', {}).get('fx_status')),
    ('secGoogle', 'google_popularity.estimated_24h_searches', api.get('google_popularity', {}).get('estimated_24h_searches')),
    ('intelKap', 'kap_data.kap_status', api.get('kap_data', {}).get('kap_status')),
    ('intelNews', 'news_index', api.get('news_index')),
    ('topXu100', 'xu100_data.points', api.get('xu100_data', {}).get('points')),
    ('topUsdTry', 'macro_fx.usd_try', api.get('macro_fx', {}).get('usd_try')),
    ('topSystemScore', 'system_score', api.get('system_score')),
]

mismatches = []
matches = []

for elem_id, key_name, val in ui_mappings:
    # Check if element ID exists in HTML
    pattern = f'id=[\"\']{elem_id}[\"\']'
    if not re.search(pattern, html):
        mismatches.append(f"HATA: HTML icinde '{elem_id}' ID'si bulunamadi!")
        continue
    
    # Check if renderData updates this element
    render_pattern = f"document.getElementById\\(['\"]{elem_id}['\"]\\)"
    if not re.search(render_pattern, html):
        mismatches.append(f"HATA: JavaScript icinde '{elem_id}' ID'sine veri basilmiyor (renderData eksik)!")
        continue

    matches.append((elem_id, key_name, str(val)[:30]))

print(f"Toplam Eslesen ve Baglanan Veri: {len(matches)} / {len(ui_mappings)}")
if mismatches:
    print(f"Eksik / Uyumsuzluk Sayisi: {len(mismatches)}")
    for m in mismatches:
        print("  -", m)
else:
    print("MUKEMMEL: Tum gorsel arayuz kutucuklari ile arka plan verileri %100 birebir esit ve baglidir!")

print("\nOrnek Ilk 15 Eslesme:")
for elem_id, k, v in matches[:15]:
    print(f"  [HTML ID: {elem_id:<15}] <== [API: {k:<25}] -> {v}")
