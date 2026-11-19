# 🏛️ Ertuğrul YZ — İleri Düzey Finansal Piyasalar ve Ticaret Akademisi
**6 Temel İleri Düzey Borsa Silahı Kılavuzu ve Algoritmik Modelleri**

---

## 1. ⚔️ VİOP (Vadeli İşlem ve Opsiyon Piyasası)
* **Temel Mantık:** Gelecekteki bir tarihte, bugünden belirlenen fiyattan bir dayanak varlığı (Endeks 30, Dolar, Altın, THYAO, EREGL) alma veya satma taahhüdüdür.
* **Kaldıraç Oranı:** Genellikle **5x ile 10x** arasındadır. 10.000 TL teminatla 100.000 TL'lik BIST 30 kontratı açılabilir.
* **İki Yönlü İşlem:**
  - **Uzun (Long):** Fiyatın yükseleceğine oynama.
  - **Kısa (Short):** Fiyatın düşeceğine oynama.
* **Algoritmik Kural:** Teminat tamamlama çağrısı (Margin Call) yememek için pozisyon büyüklüğü toplam kasanın asla %30'unu geçemez; sert stop-loss zorunludur.

---

## 2. 🎯 Varant İşlemleri (Securitized Derivatives)
* **Temel Mantık:** Bir hisse veya endeksi belirli bir fiyattan alma (Call) veya satma (Put) **hakkını** kuruşlarla satın almaktır (Yükümlülük değil haktır).
* **Avantaj:** Zarar sadece yatırılan varant parasıyla sınırlıdır (eksiye düşmez, margin call yoktur).
* **Büyük Risk (Teta / Zaman Erimesi):** Vade yaklaştıkça varantın değeri her gün erir.
* **Algoritmik Kural:** Vadesine 25 günden az kalmış varantlar çöpe dönebilir; sistem sadece **30-60 gün vadeli** ve **Deltası 0.40 - 0.70** arası sağlıklı varantları seçer.

---

## 3. ⚡ Scalping (Saniyelik / Dakikalık Al-Sat)
* **Temel Mantık:** Büyük kârlar peşinde saatlerce beklemek yerine; saniyeler içinde 1-2 kademelik kuruş farklarını toplayıp yüzlerce işlemde bileşik getiri üretmektir.
* **Kritik Eşik:** Sıfır veya ultra düşük komisyon (Midas'ta 0 TL olması scalping için dünyadaki en büyük avantajdır).
* **Algoritmik Kural:** Tahta derinliği (Level 2) ve Bank of America / Kurumsal akışın yönünde girilir; ters kademe görüldüğü anda 1 kademede acımadan stop olunur.

---

## 4. 📰 Haber / KAP Akışı Trade Etme (Event-Driven Trading)
* **Temel Mantık:** Şirketlerin Kamuyu Aydınlatma Platformu'na (KAP) düşen haberlerini insanlar okuyup anlayana kadar, algoritmaların milisaniyeler içinde analiz edip emri göndermesidir.
* **Haber Tipleri:**
  - **Kuvvetli Pozitif (+):** Beklenti üstü net kâr / bilanço, devasa yeni iş sözleşmesi (ciroya oranı %20+), yüksek oranlı bedelsiz sermaye artırımı, şirket hisse geri alımı (Share Buyback).
  - **Negatif (-):** Sermaye azaltımı, konkordato / dava riski, üretim durdurma, patron hisse satışı.
* **Algoritmik Kural:** Haber düşer düşmez ilk 3-5 saniyedeki tavana giden ivme yakalanır; haber piyasada soğuduğunda kâr realizasyonu yapılır.

---

## 5. 📉 Açığa Satış (Short Selling)
* **Temel Mantık:** Elinizde olmayan bir hisseyi aracı kurumdan ödünç alıp yüksek fiyattan satmak, hisse düştüğünde aşağıdan geri alıp aracı kuruma iade ederek aradaki farkı kâr olarak cebe indirmektir.
* **Motto:** "Ayılar da para kazanır!" Borsa çökerken kenarda ağlamak yerine, düşüş dalgasını nakde çevirmektir.
* **BIST Kuralı:** Türkiye'de açığa satış dönemsel olarak sadece BIST 50 hisselerinde veya yukarı adım kuralı (uptick rule) ile uygulanır. VİOP ve Satım Varantları açığa satışın en risksiz modern alternatifidir.

---

## 6. 🚀 Halka Arz (IPO) Katılımı
* **Temel Mantık:** Borsaya ilk kez açılan şirketlerin hisselerini tabandan, indirimli fiyattan ve eşit dağıtımla satın almaktır.
* **Karakteristik Getiri:** Yeni halka arz olan şirketler genellikle ilk 4-8 tavan serisi (+%10 günlük bileşik) yakalar.
* **Algoritmik Kural:** 
  - Tavan serisi bozulduğu gün (kademede milyonlarca lotluk tavan kilidi çözüldüğünde ve işlem hacmi patladığında) sistem tüm lotları satar, kârı ana kasaya kilitler.
  - Asla tavan bozulduktan sonra açgözlülükle elde tutulmaz.
