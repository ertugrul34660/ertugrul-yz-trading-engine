import json
import os
import datetime

ledger_path = r"C:\Users\ertug\.gemini\antigravity\scratch\02-Holding-Yonetim-ve-Uzman-Ajanlar\ertugrul-yz-agent\data\personel_karne_ledger.json"
os.makedirs(os.path.dirname(ledger_path), exist_ok=True)

if os.path.exists(ledger_path):
    try:
        with open(ledger_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = {"models": {}, "history": []}
else:
    data = {"models": {}, "history": []}

model_key = "Gemini 4 Carbon (Senior Floor Trader)"
if "models" not in data:
    data["models"] = {}
if model_key not in data["models"]:
    data["models"][model_key] = {"points": 100, "xp": 2630, "rank": "Kıdemli Borsa ve Portföy Direktörü"}

data["models"][model_key]["points"] += 10
data["models"][model_key]["xp"] += 150

entry = {
    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "model": model_key,
    "action": "Yönetim Kurulu Başkanı Takdiri (Harika çalışıyorsun devam)",
    "points_awarded": "+10",
    "total_points": data["models"][model_key]["points"],
    "xp": data["models"][model_key]["xp"]
}
data.setdefault("history", []).append(entry)

with open(ledger_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Puan Başarıyla Kütüğe İşlendi!")
print("Model:", model_key)
print("Güncel Puan:", data["models"][model_key]["points"])
print("Güncel XP:", data["models"][model_key]["xp"])
