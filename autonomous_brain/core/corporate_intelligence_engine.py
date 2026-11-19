"""
Ertugrul YZ - Corporate Intelligence & Deep Risk Management Knowledge Base
Bu modül:
1. BIST ve radarımızdaki şirketlerin (THYAO, ASTOR, EREGL, AKBNK, TUPRS, BIMAS, ASELS vb.)
   arka planındaki kurumsal kimlikleri, yönetim kurulu başkanlarını, genel müdürlerini,
   faaliyet alanlarını ve ana gelir kaynaklarını hafızaya alır.
2. Temel risk faktörlerini (Döviz borcu, hammadde maliyeti, jeopolitik riskler, faiz duyarlılığı)
   ve teknik grafik davranış karakteristiğini (Destek/Direnç refleksleri, volatilite) kütüğe mühürler.
3. Al-sat kararlarında sadece tahta hareketine değil, şirketin kurumsal gücüne ve risk profiline göre
   en güvenli kalkanı oluşturur.
"""

import json
import os
from datetime import datetime

DB_PATH = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\autonomous_brain\memory\corporate_intelligence_knowledge_base.json"

CORPORATE_INTELLIGENCE = {
    "system_name": "ERTUGRUL_YZ_CORPORATE_INTELLIGENCE_VAULT",
    "updated_at": datetime.now().isoformat(),
    "risk_management_doctrine": {
        "rule_1": "Körlemesine tahtaya girilmez; şirketin arkasındaki sermaye, yönetim ve nakit akışı bilinir.",
        "rule_2": "Yüksek borçlu ve sığ hisselerden uzak durulur, BIST 30 lokomotifleri önceliklendirilir.",
        "rule_3": "Varantlarda kaldıraç çarpanı ve son kullanım tarihi (vade) riski sürekli tartılır.",
        "rule_4": "Zararına satış yasağı kurumsal gücü yüksek şirketlerde sermaye koruma kalkanıdır."
    },
    "companies": {
        "THYAO": {
            "name": "Türk Hava Yolları A.O.",
            "sektor": "Havacılık ve Lojistik",
            "yonetim": {
                "yonetim_kurulu_baskani": "Prof. Dr. Ahmet Bolat",
                "genel_mudur": "Bilal Ekşi"
            },
            "faaliyet_alani": "Yolcu taşımacılığı, hava kargo (Turkish Cargo), teknik bakım (Turkish Technic) ve küresel uçuş ağı.",
            "gelir_kaynaklari": "Uluslararası yolcu biletleri (%80+ döviz geliri), kargo taşımacılığı.",
            "risk_faktorleri": "Jet yakıtı (Brent petrol) fiyatları, jeopolitik gerilimler, küresel turizm dalgalanmaları.",
            "grafik_ve_fiyat_karakteri": "BIST'in ana lokomotifidir. 320-335 TL bandında güçlü kurumsal destek ve devasa günlük hacim (40M+ lot) üretir. Varantları en likit olanıdır."
        },
        "ASTOR": {
            "name": "Astor Enerji A.Ş.",
            "sektor": "Elektrik Teçhizatı ve Enerji İletimi",
            "yonetim": {
                "yonetim_kurulu_baskani": "Feridun Geçgel",
                "genel_mudur": "Hakan Ünsal"
            },
            "faaliyet_alani": "Transformatör (güç ve dağıtım trafoları), orta ve yüksek gerilim anahtarlama ürünleri imalatı ve ihracatı.",
            "gelir_kaynaklari": "90+ ülkeye trafo ihracatı, TEİAŞ ve yenilenebilir enerji santralleri projeleri.",
            "risk_faktorleri": "Bakır ve silisli sac hammadde maliyetleri, küresel şebeke yatırımlarının hızı.",
            "grafik_ve_fiyat_karakteri": "145-160 TL bandında güçlü sipariş defteriyle hareket eder. İhale haberleriyle sert yukarı tepkiler verir."
        },
        "EREGL": {
            "name": "Ereğli Demir ve Çelik Fabrikaları T.A.Ş. (OYAK Grubu)",
            "sektor": "Temel Metal ve Ağır Sanayi",
            "yonetim": {
                "yonetim_kurulu_baskani": "Süleyman Savaş Erdem (OYAK Genel Müdürü)",
                "genel_mudur": "Niyazi Aşkın Uzun"
            },
            "faaliyet_alani": "Yassı çelik, levha, sıcak ve soğuk haddelenmiş rulo üretimi; Türkiye'nin en büyük entegre çelik devi.",
            "gelir_kaynaklari": "Otomotiv, beyaz eşya, boru ve inşaat sektörlerine endüstriyel çelik satışı.",
            "risk_faktorleri": "Küresel çelik fiyatları (HRC), demir cevheri ve koklaşabilir kömür maliyetleri, Çin dampingi.",
            "grafik_ve_fiyat_karakteri": "Ağır ve oturaklı tahta yapısı. 30-33 TL bandında güçlü temettü ve defansif liman karakteristiği taşır."
        },
        "AKBNK": {
            "name": "Akbank T.A.Ş. (Sabancı Holding)",
            "sektor": "Bankacılık ve Finans",
            "yonetim": {
                "yonetim_kurulu_baskani": "Suzan Sabancı",
                "genel_mudur": "Kaan Gür"
            },
            "faaliyet_alani": "Bireysel, ticari ve kurumsal bankacılık, dijital finans ve hazine işlemleri.",
            "gelir_kaynaklari": "Net faiz marjı (NIM), kredi komisyonları, hazine tahvil getirileri.",
            "risk_faktorleri": "TCMB faiz kararları, regülasyonlar, kredi takip oranları (NPL).",
            "grafik_ve_fiyat_karakteri": "Yabancı fonların giriş-çıkış kapısıdır. Endeks rallilerinde en önden gider, yüksek likiditeye sahiptir."
        },
        "TUPRS": {
            "name": "Tüpraş - Türkiye Petrol Rafinerileri A.Ş. (Koç Holding)",
            "sektor": "Enerji ve Rafineri",
            "yonetim": {
                "yonetim_kurulu_baskani": "Mehmet Ömer Koç",
                "genel_mudur": "İbrahim Yelmenoğlu"
            },
            "faaliyet_alani": "Ham petrol işleme, benzin, dizel, jet yakıtı ve asfalt üretimi.",
            "gelir_kaynaklari": "Akaryakıt satışları, uluslararası ürün marjları (Crack margin).",
            "risk_faktorleri": "Brent petrol fiyat dalgalanmaları, rafineri bakım duruşları, döviz kuru.",
            "grafik_ve_fiyat_karakteri": "Yüksek nakit akışı ve güçlü bilanço. 160-180 TL bandında defansif ve güçlü temettü şampiyonudur."
        }
    }
}

def build_knowledge_base():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(CORPORATE_INTELLIGENCE, f, indent=2, ensure_ascii=False)
    print("✅ Kurumsal İstihbarat ve Derin Risk Yönetimi Bilgi Bankası başarıyla hafızaya alındı!")

if __name__ == "__main__":
    build_knowledge_base()
