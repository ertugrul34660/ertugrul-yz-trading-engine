# 🦅 Ertuğrul YZ - Autonomous Algorithmic Trading & Scalping Engine

Türkiye finansal piyasaları (**Borsa İstanbul - BIST, VİOP ve Varantlar**) için geliştirilmiş, 7/24 kesintisiz çalışan, dayanıklı ve pekiştirmeli öğrenme (Q-Learning) ile kendi kendini eğiten açık kaynaklı algoritmik ticaret motoru.

---

## 🌟 Öne Çıkan Özellikler

- **🛡️ 7/24 Kesintisiz Otonom Nöbetçi (Resilient Engine):** Bağlantı kopmalarına ve API gecikmelerine karşı *exponential backoff* algoritmasıyla kendi kendini onaran mimari.
- **⚡ Kuruş Kuruş Scalping (Penny Harvester):** Tahtadaki 1 kademelik mikro kârları (+%1.5 - +%2) mekanik olarak toplayıp sermayeyi nakde çeviren yüksek frekanslı emir motoru.
- **🎯 Sert Devre Kesici (Circuit Breaker):** Günlük portföy kaybı %3.0'a ulaştığı an tüm işlemleri kilitleyen kurumsal sermaye koruma mekanizması.
- **📊 BIST 550+ Likidite ve Derinlik Filtresi:** Sığ, donuk ve manipülatif hisseleri kara listeye alarak sadece BIST 30 lokomotiflerinde işlem izni veren koruma katmanı.
- **📈 İndikatör Paketi:** Wilder's Smoothing RSI, MACD (12, 26, 9) ve Çift EMA (20 & 50) trend onay mekanizması.
- **🧠 Kendini Eğiten Yapay Zeka (Q-Learning):** Geçmiş seansların kâr/zarar sonuçlarından ders çıkararak ağırlıklarını güncelleyen otonom beyin.

---

## 📂 Proje Yapısı

```
ertugrul-yz-alsat-botu/
├── autonomous_brain/
│   ├── core/
│   │   ├── resilient_algo_trader.py       # 7/24 Otonom Trading Motoru & Devre Kesici
│   │   ├── bist_technical_analyzer.py    # RSI, MACD, EMA İndikatör Motoru
│   │   ├── bist_data_fetcher.py           # Likidite Filtresi & Sığ Tahta Denetleyicisi
│   │   ├── self_evolving_brain.py         # Q-Learning Strateji Geliştirici
│   │   └── pre_market_scout_agent.py      # Seans Öncesi İstihbarat ve Tarama Ajanı
│   ├── memory/                            # SQLite İşlem Kütükleri & Telemetri
│   ├── reports/                           # BIST 550 Hisse Taramaları & Analiz Raporları
│   └── research/                          # Finansal Veri Kütüphaneleri & Modeller
└── README.md
```

---

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler
- Python 3.10+
- `pip install pandas numpy yfinance`

### 2. Likidite ve Teknik Taramayı Çalıştırma
```bash
python autonomous_brain/core/bist_data_fetcher.py
```

### 3. Dayanıklı Algoritmik Motoru Başlatma
```bash
python autonomous_brain/core/resilient_algo_trader.py
```

---

## 🤝 Katkıda Bulunma (Contributing)

Bu proje açık kaynaklıdır ve topluluk geliştirmesine açıktır!
1. Bu depoyu Fork edin.
2. Yeni bir özellik dalı oluşturun (`git checkout -b ozellik/yeni-indikator`).
3. Değişikliklerinizi commit edin (`git commit -m 'Yeni likidite filtresi eklendi'`).
4. Dalınıza push yapın (`git push origin ozellik/yeni-indikator`).
5. Bir **Pull Request (Geliştirme İsteği)** açın.

---

## ⚖️ Lisans ve Sorumluluk Reddi
Bu yazılım eğitim ve araştırma amaçlı geliştirilmiştir. Kesinlikle yatırım tavsiyesi içermez. Gerçek piyasalardaki finansal risk kullanıcıya aittir.

**Geliştirici:** Ertuğrul YZ Ekosistemi
