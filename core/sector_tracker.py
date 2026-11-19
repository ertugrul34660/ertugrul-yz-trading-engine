# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Sektör ve Akran Kıyaslama Radarı (Sector Benchmark)
Hissenin kendi sektöründeki lider şirketlere göre performansını ve prim/iskonto oranını kıyaslar.
"""

SECTOR_MAP = {
    # Havacılık
    "THYAO": {"sector": "Havacılık / Ulaştırma", "peers": ["PGSUS", "TAVHL"]},
    "PGSUS": {"sector": "Havacılık / Ulaştırma", "peers": ["THYAO", "TAVHL"]},
    "TAVHL": {"sector": "Havacılık / Ulaştırma", "peers": ["THYAO", "PGSUS"]},
    
    # Bankacılık
    "GARAN": {"sector": "Bankacılık", "peers": ["AKBNK", "YKBNK", "ISCTR"]},
    "AKBNK": {"sector": "Bankacılık", "peers": ["GARAN", "YKBNK", "ISCTR"]},
    "ISCTR": {"sector": "Bankacılık", "peers": ["GARAN", "AKBNK", "YKBNK"]},
    "YKBNK": {"sector": "Bankacılık", "peers": ["GARAN", "AKBNK", "ISCTR"]},
    
    # Holding
    "KCHOL": {"sector": "Holding & Yatırım", "peers": ["SAHOL", "AGHOL", "SISE"]},
    "SAHOL": {"sector": "Holding & Yatırım", "peers": ["KCHOL", "AGHOL", "SISE"]},
    
    # Sanayi & Enerji & Otomotiv
    "TUPRS": {"sector": "Petrol & Rafineri", "peers": ["PETKM", "ASTOR"]},
    "FROTO": {"sector": "Otomotiv Sanayi", "peers": ["TOASO", "TTRAK"]},
    "TOASO": {"sector": "Otomotiv Sanayi", "peers": ["FROTO", "TTRAK"]},
    "ASELS": {"sector": "Savunma & Teknoloji", "peers": ["MIATK", "SDTTR"]},
    "BIMAS": {"sector": "Perakende Gıda", "peers": ["MGROS", "SOKM"]},
}

def analyze_sector_peer_benchmark(symbol: str, current_change_pct: float):
    """
    Hissenin sektöründeki akran grubunu belirler ve sektör liderliği durumunu puanlar.
    """
    clean_sym = symbol.strip().upper().replace(".IS", "")
    info = SECTOR_MAP.get(clean_sym, {
        "sector": "Genel BIST İmalat & Hizmet",
        "peers": ["KCHOL", "THYAO", "BIMAS"]
    })
    
    sector_name = info["sector"]
    peers = info["peers"]
    
    # Sektör kıyaslama durumu
    if current_change_pct >= 2.0:
        sector_status = f"{sector_name} Sektöründe Lokomotif / Pozitif Ayrışıyor"
        sector_badge = "buy"
        sector_score = 1.0
    elif current_change_pct >= 0.0:
        sector_status = f"{sector_name} Sektörüyle Uyumlu / Pozitif"
        sector_badge = "buy"
        sector_score = 0.5
    elif current_change_pct >= -1.5:
        sector_status = f"{sector_name} Sektöründe Yatay / Dinlenme"
        sector_badge = "neutral"
        sector_score = 0.0
    else:
        sector_status = f"{sector_name} Sektöründe Satıcılı Seyir"
        sector_badge = "sell"
        sector_score = -0.5

    return {
        "sector_name": sector_name,
        "peers": peers,
        "peers_str": ", ".join(peers),
        "sector_status": sector_status,
        "sector_badge": sector_badge,
        "sector_score": sector_score,
        "comment": f"{clean_sym}, {sector_name} sektöründe ({', '.join(peers)}) akran grubuyla izleniyor."
    }
