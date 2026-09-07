import re
import json
from pathlib import Path

files = ['design.py', 'build_site.py', 'stories.py', 'site/assets/design.js', 'site/assets/trip-page.js', 'site/assets/search.js', 'site/assets/live-news.js']

thai_regex = re.compile(r'[\u0E00-\u0E7F]+')
strings = set()

for f in files:
    path = Path(f)
    if not path.exists(): continue
    content = path.read_text(encoding='utf-8')
    
    # We want exactly the strings the user sees. 
    # Let's extract everything between > and <
    html_texts = re.findall(r'>([^<]+)<', content)
    for s in html_texts:
        s = s.strip()
        if s and thai_regex.search(s):
            strings.add(s)

    # And strings in quotes (single, double, or backticks)
    literals = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"|\'([^\'\\]*(?:\\.[^\'\\]*)*)\'|`([^`\\]*(?:\\.[^`\\]*)*)`', content)
    for m in literals:
        s = m[0] or m[1] or m[2]
        s = s.strip()
        if s and thai_regex.search(s):
            # Exclude some large HTML chunks that might have been matched as a whole
            if '<' not in s and '>' not in s:
                strings.add(s)

d = {s: '' for s in sorted(strings)}
Path('ui_draft.json').write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Found {len(d)} strings')
