import re
import json
from pathlib import Path

files = [
    "design.py",
    "build_site.py",
    "stories.py",
    "site/assets/design.js",
    "site/assets/trip-page.js",
    "site/assets/search.js",
    "site/assets/live-news.js"
]

thai_regex = re.compile(r'[\u0E00-\u0E7F]+')

results = []
for f in files:
    path = Path(f)
    if not path.exists():
        print(f"Not found: {f}")
        continue
    content = path.read_text(encoding='utf-8')
    
    # We want strings. Usually in quotes.
    # Simple heuristic: find anything in quotes or HTML text that contains Thai.
    # For UI.json, we want exact strings.
    # Let's just extract all unique matches of Thai text or lines with Thai text.
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if thai_regex.search(line):
            results.append(f"{f}:{i+1}: {line.strip()}")

Path('thai_lines.txt').write_text('\n'.join(results), encoding='utf-8')
print(f"Extracted {len(results)} lines to thai_lines.txt")
