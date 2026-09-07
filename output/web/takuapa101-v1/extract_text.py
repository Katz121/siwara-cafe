import json

with open('data/places-enriched.json', encoding='utf-8') as f:
    data = json.load(f)

places_of_interest = ['riverwalk', 'wat-kongkha', 'governor-wall', 'yan-yao', 'thung-tuk', 'thung-phra', 'city']

places = [p for p in data if p.get('id') in places_of_interest]

with open('extract_text.txt', 'w', encoding='utf-8') as f:
    for p in places:
        f.write(f"\n--- {p.get('id')} ---\n")
        eras = p.get('eras', {})
        for era in ['then', 'before', 'now']:
            if era in eras:
                f.write(f"[{era}] {eras[era].get('headline_th')}\n")
                f.write(eras[era].get('body_th') + "\n")
        
        f.write("[history claims]\n")
        for h in p.get('history', []):
            f.write(f"- {h.get('claim_th')}\n")
