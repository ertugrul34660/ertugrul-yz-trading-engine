# -*- coding: utf-8 -*-
import urllib.request
import json

test_stocks = ["THYAO", "BIMAS", "TUPRS", "DOAS", "AAPL"]

print("==========================================================================")
print("       ERTUĞRUL YZ • BORSA AL-SAT KARAR TERMINALI CANLI TESTI")
print("==========================================================================")

for s in test_stocks:
    try:
        url = f"http://localhost:5055/api/analyze?symbol={s}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        res = urllib.request.urlopen(req, timeout=12)
        d = json.loads(res.read().decode("utf-8"))
        
        if d.get("success"):
            print(f"\n[+] Hisse: {d['symbol']} ({d['current_price']} {d['currency']})")
            print(f"    • Karar: {d['badge_text']} (Güven: {d['confidence']})")
            print(f"    • Emir: {d['suggested_entry']} 'den Al -> {d['target_price']} 'ye Sat")
            print(f"    • Net Hedef Kâr: {d['profit_badge']} | Stop Sınırı: {d['stop_loss']} ({d['risk_badge']})")
            print(f"    • BofA Durumu: {d['bofa_action']}")
            print(f"    • TradingView Robotları: {d['tv_signal']} (Skor: {d['tv_score_raw']})")
            print(f"    • Haber Havası: {d['news_sentiment']}")
        else:
            print(f"\n[-] Hisse: {s} -> Hata: {d.get('error')}")
    except Exception as e:
        print(f"\n[-] Hisse: {s} -> Bağlantı Hatası: {e}")

print("\n==========================================================================")
print("                      TEST BAŞARIYLA TAMAMLANDI")
print("==========================================================================")
