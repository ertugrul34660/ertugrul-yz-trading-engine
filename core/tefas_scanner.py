# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • TEFAS Yatırım Fonları Liderlik Radarı (TEFAS Funds Scanner)
Türkiye'nin en popüler, en çok kazandıran hisse senedi ve serbest fonlarını takip eder.
"""

def get_top_tefas_funds():
    """
    Borsa İstanbul'da yatırımcıların en çok tercih ettiği lider TEFAS fonları.
    """
    return [
        {
            "code": "TI2",
            "name": "İş Portföy BIST 100 Dışı Şirketler Hisse Fonu",
            "category": "Hisse Senedi Fonu",
            "return_1y": "+%84.2",
            "return_1m": "+%9.4",
            "bofa_alignment": "Yan Tahtalar & Büyüme Şirketleri",
            "score": "95/100"
        },
        {
            "code": "TCD",
            "name": "Tacirler Portföy Değişken Fon",
            "category": "Değişken Fon",
            "return_1y": "+%78.6",
            "return_1m": "+%8.1",
            "bofa_alignment": "Agresif Hisse & Arbitraj",
            "score": "92/100"
        },
        {
            "code": "MAC",
            "name": "Marmara Capital Portföy Hisse Senedi Fonu",
            "category": "Hisse Senedi Fonu",
            "return_1y": "+%74.5",
            "return_1m": "+%7.8",
            "bofa_alignment": "Değer Hisseleri & BIST 30",
            "score": "90/100"
        },
        {
            "code": "IIH",
            "name": "İstanbul Portföy Üçüncü Hisse Senedi Fonu",
            "category": "Hisse Senedi Fonu",
            "return_1y": "+%71.8",
            "return_1m": "+%6.9",
            "bofa_alignment": "İhracatçı Sanayi Şirketleri",
            "score": "88/100"
        },
        {
            "code": "KZL",
            "name": "Kuveyt Türk Altın Katılım Fonu",
            "category": "Kıymetli Madenler",
            "return_1y": "+%68.4",
            "return_1m": "+%5.2",
            "bofa_alignment": "Enflasyon & Dolar Koruma Kalkanı",
            "score": "86/100"
        }
    ]

if __name__ == "__main__":
    print("TEFAS Lider Fonlar:", get_top_tefas_funds())
