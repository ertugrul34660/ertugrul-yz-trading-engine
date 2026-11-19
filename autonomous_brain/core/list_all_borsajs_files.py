import os
base = r"C:\Users\ertug\.gemini\antigravity\scratch\04-Finans-Borsa-ve-Ticaret\ertugrul-yz-alsat-botu\autonomous_brain\research\borsajs"
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(('.ts', '.js', '.json')):
            print(os.path.join(root, f))
