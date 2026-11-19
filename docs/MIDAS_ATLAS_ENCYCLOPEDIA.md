# 📘 Midas Atlas (atlas.getmidas.com) Eksiksiz Platform Kılavuzu & Mimari Haritası
**Ertuğrul YZ Finansal Zeka ve Karargah Dokümantasyonu**

---

## 1. Midas Atlas Nedir? (Genel Bakış)
Midas Atlas, profesyonel web tabanlı bir borsa terminalidir (Bloomberg / TradingView karması).
Next.js App Router, Radix UI ve DXCharts çok katmanlı Canvas motoruyla çalışır.
Kullanıcıya modüler (drag-and-drop / resize) bir çalışma alanı sunar.

---

## 2. Platformdaki 12 Temel Modül ve Görevleri

### 1. Varant Zinciri (`warrant-chain`)
* **İşlev:** Borsa İstanbul'da işlem gören tüm Alım (Call) ve Satım (Put) varantlarını tek tabloda listeler.
* **Filtreler:**
  - Dayanak Varlık (THYAO, ASELS, AKBNK, EREGL, XU030 vb.)
  - İhraççı Kurum (İş Yatırım, Ak Yatırım vb.)
  - Vade Tarihi (Kalan gün sayısı)
  - Kullanım Fiyatı (Strike Price)
* **Kritik Metrikler:** Kaldıraç (Gearing), Delta (Hassasiyet), Başa Baş Noktası, Teta (Günlük zaman erimesi maliyeti).

### 2. Varant Trendleri (`options-trends` / Varant Trendleri)
* **İşlev:** Günün en çok işlem gören, hacim patlaması yaşayan ve en çok kazandıran varantlarını ısı haritası ve sıralı liste olarak gösterir.
* **Algoritma Kullanımı:** Hacim patlaması yapan alım/satım varantlarını tespit ederek büyük kurumsal paranın hangi yöne bahis aldığını anlamamızı sağlar.

### 3. Opsiyon Zinciri (`options-chain`)
* **İşlev:** Özellikle ABD hisse senetleri (Apple, Tesla, Microsoft, Nvidia) ve VİOP için Call/Put opsiyon sözleşmelerini gösterir.
* **Kullanım:** Prim toplama, riskten korunma (hedge) ve kaldıraçlı yönlü işlemler.

### 4. Hisse Tarayıcı (`screener`)
* **İşlev:** BIST ve ABD pazarlarındaki binlerce hisseyi rasyolara göre süzer.
* **Filtre Kriterleri:**
  - F/K (Fiyat/Kazanç) Oranı
  - PD/DD (Piyasa Değeri / Defter Değeri)
  - Günlük Hacim ve Piyasa Değeri
  - Temettü Verimi (%)
  - Sektör Seçimi (Bankacılık, Havacılık, Teknoloji, Sanayi)

### 5. Derinlik / Midas Pro (`depth`)
* **İşlev:** Borsa İstanbul hisselerinde tahtadaki 10 kademe alış ve satış emirlerini gösterir.
* **Aracı Kurum Dağılımı (AKD):** Hangi kurumun (Bank of America, Yapı Kredi, İş Yatırım vb.) tahtada net alıcı veya net satıcı olduğunu canlı akıtır.

### 6. Gelişmiş Grafik (`advanced-chart` - DXCharts)
* **Katmanlar:** OHLCV, Mum, Heikin Ashi, Hacim çubukları.
* **İndikatörler:** EMA, SMA, RSI, MACD, Bollinger Bantları, VWAP, Supertrend.
* **Çizim Araçları:** Trend çizgileri, Fibonacci düzeltmeleri, yatay destek/direnç bantları.

### 7. Varlık Detayı (`asset`)
* **Genel Bakış:** Açılış, gün içi tavan/taban, 52 haftalık zirve/dip.
* **Finansal Rasyolar:** FAVÖK marjı, cari oran, net borç, özkaynak kârlılığı.
* **Analist Konsensüsü:** Kurum analistlerinin AL/TUT/SAT yüzdeleri ve hedef fiyat ortalamaları.
* **AI Özeti:** Hissedeki Boğa (olumlu) ve Ayı (olumsuz) tezleri.

### 8. Takip Listesi (`watchlist`)
* **Listeler:** "Takip Ettiklerim", "Yapay Zeka Top 5", özel listeler.
* **Sütunlar:** Sembol, son fiyat, günlük %, haftalık %, aylık %, yıllık %.

### 9. Pozisyonlar (`positions`)
* **İşlev:** Sahip olunan hisse/varant adedi, ortalama maliyet, anlık piyasa değeri, günlük K/Z ve toplam kâr/zarar yüzdesi.

### 10. Emir Geçmişi (`recent-orders`)
* **İşlev:** Bekleyen, gerçekleşen, iptal edilen ve süresi dolan son 200 emrin dökümü.

### 11. Portföy Özeti (`portfolio`)
* **İşlev:** TRY ve USD toplam varlıklar, nakit bakiye, takastaki bakiye ve Nema durumu.

### 12. Haberler & KAP Akışı (`news`)
* **İşlev:** Şirketlerin Kamuyu Aydınlatma Platformu (KAP) bildirimleri, bilanço tarihleri, temettü duyuruları ve finans haberleri.

---

## 3. Renk Grupları ile Akıllı Senkronizasyon (Widget Linking)
Midas Atlas'taki en güçlü ergonomik özellik:
* Widget'lar sol üstlerindeki bağlantı rengiyle (`Turuncu`, `Mavi`, `Mor`, `Yeşil`) gruplanır.
* Takip listesinde bir hisseye tıkladığınızda; aynı renge bağlı Grafik, Varlık Detayı ve Haberler paneli saniyesinde o hisseye geçer.
