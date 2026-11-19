"""
Ertuğrul YZ — Büyük Para & Türev Piyasalar Karargahı (Big Money Derivatives Core)
6 Dev Silah: VİOP, Varant, Scalping, KAP Haber, Short Selling, Halka Arz
"""

import sys
import datetime

class BigMoneyTradingEmpire:
    def __init__(self):
        self.arsenal = {
            "1_VARANT": {
                "slogan": "Küçük Parayla Milyonluk Dalga Yakalama (8x - 12x Kaldıraç)",
                "mekanizma": "Kuruşlarla (0.50 TL - 2.00 TL) Alım (Call) veya Satım (Put) hakkı alma.",
                "midas_entegrasyonu": "Midas Atlas 'Varant Zinciri' ve 'Varant Trendleri' modülleri aktif.",
                "asıl_para_sırrı": "Hisse %3 yükseldiğinde varant %30 prim yapar! Düşerken de Satım Varantı ile çöküşten kâr edilir."
            },
            "2_VIOP": {
                "slogan": "Büyük Balinaların Kaldıraçlı ve Çift Yönlü Arenası (10x Kaldıraç)",
                "mekanizma": "BIST 30 Endeksi, Dolar, Altın ve Dev hisselerde teminatla vadeli kontrat.",
                "asıl_para_sırrı": "Spot piyasada 100.000 TL kazandıran hareket, VİOP'ta 10.000 TL teminatla kazanılır."
            },
            "3_SCALPING": {
                "slogan": "Saniyeler İçinde Kuruşları Toplayıp Bileşik Servet Üretme",
                "mekanizma": "ISCTR, YKBNK ve THYAO tahtalarında 1-2 kademede alıp çıkmak.",
                "midas_entegrasyonu": "Midas'ın 0 TL Sıfır Komisyonu sayesinde her kuruş net kâr kalır."
            },
            "4_KAP_HABER": {
                "slogan": "Milisaniyelik Otonom Bilgi Arbitrajı",
                "mekanizma": "KAP'a düşen devasa iş anlaşması veya bedelsiz sermaye haberinde ilk 3 saniyede tavan kilitlemek."
            },
            "5_ACIGA_SATIS": {
                "slogan": "Ayı Piyasasında Çöküşten Servet Kazanma (Short Selling)",
                "mekanizma": "Yüksekten satıp dipten yerine koyarak düşüş trendini nakde çevirme."
            },
            "6_HALKA_ARZ": {
                "slogan": "Risksiz Tavan Serisi ve Ücretsiz Para Dağıtımı",
                "mekanizma": "İndirimli fiyattan eşit dağıtımla girip 5-7 gün boyunca her gün +%10 bileşik getiriyle çıkmak."
            }
        }

    def print_master_plan(self):
        print("="*75)
        print("🦅 ERTUĞRUL YZ • 'ASIL PARA BURADA' BÜYÜK SERMAYE STRATEJİSİ")
        print("Saat:", datetime.datetime.now().strftime("%H:%M:%S"))
        print("="*75)
        for key, item in self.arsenal.items():
            print(f"\n🔥 {key}: {item['slogan']}")
            print(f"   • Mantık : {item['mekanizma']}")
            print(f"   • Asıl Sır: {item.get('asıl_para_sırrı', 'Sıfır komisyon ve hızlı icra')}")
        print("="*75)

if __name__ == "__main__":
    empire = BigMoneyTradingEmpire()
    empire.print_master_plan()
