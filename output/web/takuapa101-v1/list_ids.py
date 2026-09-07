import json

with open('data/places-enriched.json', encoding='utf-8') as f:
    data = json.load(f)

with open('ids.txt', 'w', encoding='utf-8') as out:
    for p in data:
        out.write(f"{p.get('id')} {p.get('name_th')}\n")
