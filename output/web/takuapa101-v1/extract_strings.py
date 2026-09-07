import re
import json

files = [
    "design.py",
    "build_site.py",
    "stories.py",
    "site/assets/design.js",
    "site/assets/trip-page.js",
    "site/assets/search.js",
    "site/assets/live-news.js"
]

thai_regex = re.compile(r'[\u0E00-\u0E7F]')
strings = set()

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as fp:
            content = fp.read()
            # Find strings in double or single quotes
            matches = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"|\'([^\'\\]*(?:\\.[^\'\\]*)*)\'|`([^`\\]*(?:\\.[^`\\]*)*)`', content)
            for m in matches:
                s = m[0] or m[1] or m[2]
                if thai_regex.search(s):
                    strings.add(s)
    except Exception as e:
        print(f"Error reading {f}: {e}")

res = {s: "" for s in sorted(strings)}
with open('extracted_th.json', 'w', encoding='utf-8') as fp:
    json.dump(res, fp, ensure_ascii=False, indent=2)

print("Extracted", len(res), "strings")
