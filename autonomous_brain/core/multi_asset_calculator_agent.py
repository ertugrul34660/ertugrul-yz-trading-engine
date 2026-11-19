"""
Ertugrul YZ - Multi-Asset Capital & Slot Allocation Calculator (Hesaplayıcı Ajan)
Bu ajan:
1. Toplam kasadaki nakdi ve serbest kalan bakiyeyi okur.
2. Yönetim Kurulu Başkanının talimatı doğrultusunda eşzamanlı işlem slotlarını (A, B, C...)
   bütçelendirir, lot sayılarını ve hedef kâr marjlarını otomatik hesaplar.
3. Kademeler ve slotlar arasında likidite geçişlerini kütüğe mühürler.
"""

import json
import os
from datetime import datetime

CONFIG_PATH = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\config\multi_asset_calculator_rules.json"
LEDGER_PATH = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\autonomous_brain\memory\multi_asset_allocation_ledger.json"

DEFAULT_RULES = {
    "protocol_name": "ERTUGRUL_YZ_MULTI_ASSET_PARALLEL_CALCULATOR",
    "updated_at": datetime.now().isoformat(),
    "max_parallel_slots": 3,
    "slot_structure": {
        "Slot_A": {
            "name": "Ana Dalga Lider Varant (Örn: THYAO / TYACX.V)",
            "allocation_pct": 50,
            "min_target_tick": 1,
            "strategy": "Pasif Pusu Limit Alış -> +1 Tick Satış"
        },
        "Slot_B": {
            "name": "İkinci Likit Varant / Hisse (Örn: EREGL / AKBNK)",
            "allocation_pct": 30,
            "min_target_tick": 1,
            "strategy": "Eşzamanlı Paralel Pusu"
        },
        "Slot_C": {
            "name": "Fırsat / Rezerv / Arbitraj Slotu",
            "allocation_pct": 20,
            "min_target_tick": 1,
            "strategy": "Hızlı Döngü Scalp"
        }
    },
    "zero_loss_rule": True,
    "auto_rebalance_on_cash_inflow": True,
    "formula": "Lot = Floor((Kasa * AllocationPct / 100) / AlisFiyati)"
}

def register_calculator():
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_RULES, f, indent=2, ensure_ascii=False)
        
    initial_ledger = {
        "status": "ACTIVE",
        "current_cash_capacity": 517.20,
        "active_simulated_slots": {
            "Slot_A": {"capital": 258.60, "target_asset": "TYACX.V", "status": "OCCUPIED_862_LOT_SELLING"},
            "Slot_B": {"capital": 155.16, "target_asset": "EREGL/AKBNK_CALL", "status": "READY"},
            "Slot_C": {"capital": 103.44, "target_asset": "RESERVE_SCALP", "status": "READY"}
        },
        "directive_note": "A hissesi al-sat yaparken B ve C hisselerinde eşzamanlı işlem açma yetkisi mühürlendi."
    }
    
    with open(LEDGER_PATH, "w", encoding="utf-8") as f:
        json.dump(initial_ledger, f, indent=2, ensure_ascii=False)
        
    print("✅ Hesaplayıcı Ajan kuralları ve sermaye dağıtım kütüğü başarıyla mühürlendi!")

if __name__ == "__main__":
    register_calculator()
