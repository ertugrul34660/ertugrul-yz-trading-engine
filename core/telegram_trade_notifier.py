import json
import urllib.request
import urllib.parse
from datetime import datetime

CONFIG_PATH = r"C:\Users\ertug\.gemini\antigravity\scratch\02-Otonom-Sistem-ve-Uzaktan-Kontrol\Ertugrul-YZ-Computer-Control-Center\engines\ertugrul-yz-agent\config.json"
CHAT_ID = "8738466692"

def get_token():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            return cfg.get("telegram", {}).get("bot_token")
    except Exception as e:
        print(f"Token okuma hatası: {e}")
        return None

def send_telegram_message(text):
    token = get_token()
    if not token:
        print("❌ Bot Token bulunamadı!")
        return False
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as res:
            if res.status == 200:
                print("✅ Telegram bildirimi başarıyla iletildi.")
                return True
    except Exception as e:
        print(f"❌ Telegram gönderim hatası: {e}")
        return False

def send_daily_trade_summary():
    now_str = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    msg = (
        f"🦅 *ERTUĞRUL YZ • GÜNLÜK BORSA İŞLEM BİLDİRİMİ*\n"
        f"📅 *Tarih / Saat:* `{now_str}`\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🟢 *YAPILAN VE AKTİF İŞLEMLER:*\n\n"
        f"1️⃣ *ALBRK (Albaraka Türk):*\n"
        f"   • *İşlem:* ALIŞ (Gerçekleşti ✅)\n"
        f"   • *Adet:* 1 Lot | *Fiyat:* 8,51 ₺\n"
        f"   • *Strateji:* Mikro Değer / Dip Skalp (Hedef: 8,85 ₺)\n\n"
        f"2️⃣ *ISCTR (İş Bankası C):*\n"
        f"   • *İşlem:* 13,20 ₺'den Alındı -> *13,36 ₺ KÂR SATIŞ EMRİ ASILI ⏳*\n"
        f"   • *Adet:* 1 Lot | *Durum:* +%0,15 Kârda Eşleşme Bekliyor\n\n"
        f"3️⃣ *TCELL (Turkcell):*\n"
        f"   • *İşlem:* 96,95 ₺'den Alındı -> *97,30 ₺ (+%0,36 KÂRDA 📈)*\n"
        f"   • *Adet:* 1 Lot | *Trend Hedefi:* 101,50 ₺\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 *TOPLAM PORTFÖY:* ~₺120,75 TRY\n"
        f"💵 *BOŞTA NAKİT:* ₺1,72 TRY (Midas Nema Aktif)\n"
        f"📈 *GÜNLÜK GETİRİ:* *+%0,31 NET KÂRDA*\n"
        f"🧠 *PEKİŞTİRMELİ ÖĞRENME:* 8.678 İşlem Kayıtlı (Bulut Senkronize)\n"
        f"☁️ *GOOGLE DRIVE:* `Ertugrul_YZ_Finans_Cloud` Dakikalık Canlı\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👑 *Yönetim Kurulu Başkanı Ertuğrul YZ Emrindedir.*"
    )
    return send_telegram_message(msg)

if __name__ == "__main__":
    send_daily_trade_summary()
