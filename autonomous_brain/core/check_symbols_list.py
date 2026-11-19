import os
import json
import glob

base = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\autonomous_brain\research\borsajs"
files = glob.glob(os.path.join(base, "**", "*symbol*"), recursive=True)
print("Bulunan sembol dosyalari:")
for f in files:
    print(f, "Boyut:", os.path.getsize(f))
