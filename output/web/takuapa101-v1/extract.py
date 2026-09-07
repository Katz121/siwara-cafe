import json

def main():
    with open('data/places-enriched.json', encoding='utf-8') as f:
        d = json.load(f)
    
    places = [p for p in d if p['id'] in ['riverwalk', 'thung-phra', 'wat-pathum', 'iron-bridge']]
    with open('extract_output2.txt', 'w', encoding='utf-8') as out:
        for p in places:
            out.write(f"--- {p['id']} ---\n")
            out.write("ERAS:\n")
            out.write(json.dumps(p.get('eras', {}), ensure_ascii=False, indent=2) + "\n")
            out.write("HISTORY:\n")
            out.write(json.dumps(p.get('history', []), ensure_ascii=False, indent=2) + "\n\n")

if __name__ == '__main__':
    main()
