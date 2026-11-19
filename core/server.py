# -*- coding: utf-8 -*-
"""
Ertuğrul YZ • Günlük Borsa Al-Sat & Karar Sunucusu
Basit, ultra hızlı yerel HTTP API ve web sunucusu.
"""

import http.server
import socketserver
import json
import urllib.parse
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from core.analyzer import analyze_stock
from core.top_stocks_scanner import get_top5_profitable_stocks
from core.macro_filter import fetch_xu100_regime
from core.tefas_scanner import get_top_tefas_funds

PORT = 5055
HTML_PATH = os.path.join(BASE_DIR, "ui", "index.html")

class ThreadingHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

class AlSatHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        # Ana Sayfa
        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            if os.path.exists(HTML_PATH):
                with open(HTML_PATH, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.wfile.write(b"UI Dosyasi Bulunamadi")
            return
            
        # Analiz API Endpoint: /api/analyze?symbol=THYAO
        elif parsed.path == "/api/analyze":
            query = urllib.parse.parse_qs(parsed.query)
            symbol = query.get("symbol", [""])[0].strip()
            
            if not symbol:
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Lütfen hisse kodu girin."}).encode("utf-8"))
                return
                
            result = analyze_stock(symbol)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))
            return

        # YENİ ENDPOINT: En Çok Kazandıracak 5 Hisse /api/top5
        elif parsed.path == "/api/top5":
            stocks = get_top5_profitable_stocks(force_refresh=False)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "stocks": stocks}, ensure_ascii=False).encode("utf-8"))
            return

        # YENİ ENDPOINT: BIST 100 Makro Piyasa Rejimi /api/macro
        elif parsed.path == "/api/macro":
            macro = fetch_xu100_regime()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(macro, ensure_ascii=False).encode("utf-8"))
            return

        # YENİ ENDPOINT: Lider TEFAS Fonları /api/funds
        elif parsed.path == "/api/funds":
            funds = get_top_tefas_funds()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "funds": funds}, ensure_ascii=False).encode("utf-8"))
            return

        # CANLI 1.000 TL YATIRIM PORTFÖYÜ ENDPOINT: /api/portfolio
        elif parsed.path == "/api/portfolio":
            try:
                portfolio_file = os.path.join(BASE_DIR, "data", "live_portfolio_1000tl.json")
                if os.path.exists(portfolio_file):
                    with open(portfolio_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
                else:
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Portfoy henuz olusturulmadi"}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            return
            
        # Diğer statik dosyalar
        super().do_GET()

def run_server():
    os.chdir(BASE_DIR)
    with ThreadingHTTPServer(("", PORT), AlSatHandler) as httpd:
        print(f"[*] Ertuğrul YZ Borsa Al-Sat Sunucusu Hazır: http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[!] Sunucu kapatıldı.")

if __name__ == "__main__":
    run_server()
