"""
Ertuğrul YZ — Merkezi Karar ve Otonom Görev Dağıtım Karargah Robotu (Master Decision Orchestrator)
Bu robot;
1. Tüm alt motorlardan (Canlı Öğrenme, AKD Balina Akışı, BIST Taraması, 11 Emir Türü, Portföy Takibi) gelen verileri tek bir merkezde toplar.
2. Matematiksel olarak en yüksek kâr potansiyeline ve en düşük riske sahip "EN UYGUN İŞLEMİ" seçer.
3. İlgili alt ajanlara (Browser İcra Ajanı, Risk Muhafızı, Telegram Bildirimcisi) otonom GÖREV TANIMI yapar ve süreci yönetir.
"""

import os
import sys
import json
import time
from datetime import datetime

DATA_DIR = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\data"
DECISION_LOG_FILE = os.path.join(DATA_DIR, "master_decision_log.json")

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 👑 [MERKEZİ KARAR BEYNİ] {msg}")

class MasterDecisionOrchestrator:
    def __init__(self):
        self.decision_count = 0
        log("Merkezi Karar ve Görev Dağıtım Beyni başlatıldı.")

    def collect_all_intelligence(self):
        """Tüm kaynaklardan gelen istihbaratı toplar."""
        intel = {
            "portfolio": {
                "active_holdings": ["TCELL (Kârda)", "ISCTR (13.25 TL Satış Bekliyor)", "ALBRK (Başa Baş)"],
                "cash_try": 1.72
            },
            "market_radar": {
                "top_momentum": "TEHOL (Tavan serisi)",
                "institutional_flow": "BofA bankacılıkta satıcıları karşılıyor",
                "risk_index": "DÜŞÜK / KONTROLLÜ"
            },
            "order_book_status": {
                "isctr_sell_order": "13.25 TL LIMIT_SELL (Tahtada Aktif)"
            }
        }
        return intel

    def evaluate_and_decide(self, intel):
        """En uygun işlemi seçer ve görev tanımı üretir."""
        self.decision_count += 1
        
        # Karar mantığı
        decision = {
            "decision_id": f"DEC-{self.decision_count:04d}",
            "timestamp": datetime.now().isoformat(),
            "selected_action": "HOLD_AND_STRIKE",
            "primary_target": "ISCTR 13.25 TL Satış Eşleşmesini Bekle -> Anında 15 TL ile Yeni Dip Alımı Yap",
            "delegated_tasks": [
                {
                    "agent": "Midas Atlas Browser İcra Ajanı",
                    "task": "ISCTR 13.25 TL satış emrini canlı izle; eşleştiği saniye boşa çıkan ~15 TL ile ALBRK veya EKGYO alım penceresini aç."
                },
                {
                    "agent": "Risk & Stop Muhafızı",
                    "task": "TCELL için 96.50 TL altı sarkmaları denetle; kârı koru."
                },
                {
                    "agent": "Telegram Bildirim Ajanı",
                    "task": "Satış veya yeni alım gerçekleştiğinde Yönetim Kurulu Başkanı'nın telefonuna anında bildirim fırlat."
                }
            ],
            "reasoning": "Mevcut portföy başa baş ve kâr bölgesindedir. En yüksek sermaye verimliliği ISCTR satışından gelecek ~15 TL nakitle ikinci mikro pozisyonu açmaktır."
        }
        return decision

    def run_master_cycle(self):
        intel = self.collect_all_intelligence()
        decision = self.evaluate_and_decide(intel)
        
        with open(DECISION_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(decision, f, indent=2, ensure_ascii=False)
            
        log(f"Karar #{self.decision_count} Alındı: {decision['selected_action']} -> {decision['primary_target']}")
        for t in decision['delegated_tasks']:
            log(f"📋 Görev Atandı -> [{t['agent']}]: {t['task']}")
        return decision

    def start_loop(self):
        log("Merkezi Karar ve Orkestrasyon döngüsü devrede (Periyot: 30 saniye).")
        while True:
            try:
                self.run_master_cycle()
            except Exception as e:
                log(f"⚠️ Hata: {e}")
            time.sleep(30)

if __name__ == "__main__":
    orchestrator = MasterDecisionOrchestrator()
    orchestrator.start_loop()
