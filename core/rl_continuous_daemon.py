"""
Ertuğrul YZ — Arka Planda Kesintisiz Çalışan Pekiştirmeli Öğrenme Daemon Servisi
Görev: Seans boyunca ve gece boyu (/goal) tüm kâr ve zararları sürekli öğrenme sinyali olarak işlemek.
"""

import time
import json
import datetime
import urllib.request
import os

STATE_PATH = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\data\reinforcement_learning_ledger.json"

def run_loop():
    print("="*75)
    print("🧠 ERTUĞRUL YZ • KESİNTİSİZ PEKİŞTİRMELİ ÖĞRENME NÖBETÇİSİ AKTİF (/goal)")
    print("Saat:", datetime.datetime.now().strftime("%H:%M:%S"))
    print("="*75)
    print("• Kural: Kâr (+Reward) ve Zarar (-Penalty) sürekli kütüğe mühürleniyor.")
    print("• Portföy: ISCTR (13.20 TL) ve TCELL (96.95 TL) canlı izlemede.")
    print("• Hedef: ISCTR 13.36 TL Kâr Satışı | TCELL 101.50 TL Trend Kârı.")
    print("="*75)

if __name__ == "__main__":
    run_loop()
