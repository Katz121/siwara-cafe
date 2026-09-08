import os
import json
import re

SITE_DIR = r"D:\Siwaracafeweb\output\web\takuapa101-v1\site"
DATA_DIR = r"D:\Siwaracafeweb\output\web\takuapa101-v1\data"

exaggerated_words = ["ดีที่สุด", "ห้ามพลาด", "สวยที่สุด", "ที่เดียวในโลก"]
dash_pattern = re.compile(r'[—–]')
takua_pa_pattern = re.compile(r'(?i)\bTakua\s*Pa\b|\bTakuapa\b')

results = {
    "exaggerated": [],
    "dashes": [],
    "takuapa": {"Takua Pa": 0, "Takuapa": 0, "locations": []}
}

def scan_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return

    # Check for exaggerated words
    for word in exaggerated_words:
        if word in content:
            # find line number
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if word in line:
                    results["exaggerated"].append((filepath, i+1, word, line.strip()[:100]))

    # Check for dashes
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if dash_pattern.search(line):
            results["dashes"].append((filepath, i+1, line.strip()[:100]))

    # Check Takuapa vs Takua Pa
    for i, line in enumerate(lines):
        matches = takua_pa_pattern.findall(line)
        if matches:
            for m in matches:
                if ' ' in m:
                    results["takuapa"]["Takua Pa"] += 1
                else:
                    results["takuapa"]["Takuapa"] += 1
                results["takuapa"]["locations"].append((filepath, i+1, m))


for root, dirs, files in os.walk(SITE_DIR):
    for f in files:
        if f.endswith('.html'):
            scan_file(os.path.join(root, f))

for root, dirs, files in os.walk(DATA_DIR):
    for f in files:
        if f.endswith('.json') or f.endswith('.md'):
            scan_file(os.path.join(root, f))

with open(r"D:\Siwaracafeweb\output\web\takuapa101-v1\audit\check_lang_results.json", 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Scan complete")
