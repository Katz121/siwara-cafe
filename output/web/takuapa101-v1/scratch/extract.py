import json

data = json.load(open('scratch/places_4.json', encoding='utf-8'))

with open('scratch/extracted_text.txt', 'w', encoding='utf-8') as out:
    for p in data:
        out.write(f"=== {p.get('id')} ===\n")
        out.write(f"name: {p.get('name_th')} / {p.get('name_en')}\n")
        out.write(f"lead: {p.get('editorial_angle')}\n")
        
        eras = p.get("eras", {})
        for era_key in ["then", "before", "now"]:
            era = eras.get(era_key, {})
            out.write(f"eras {era_key} headline: {era.get('headline_th')}\n")
            out.write(f"eras {era_key} body: {era.get('body_th')}\n")
            
        for h in p.get('highlights', []):
            out.write(f"highlight: {h.get('title_th')} - {h.get('detail_th')}\n")
            
        for g in p.get('getting_there', []):
            out.write(f"getting_there: {g.get('from')} - {g.get('text_th')}\n")
            
        for d in p.get('did_you_know', []):
            out.write(f"did_you_know: {d.get('fact_th')}\n")
            
        fest = p.get('festival', {})
        if fest:
            out.write(f"festival months: {fest.get('months_th')}\n")
            out.write(f"festival venue: {fest.get('venue_th')}\n")
            out.write(f"festival activities: {fest.get('activities_th')}\n")
            
        out.write(f"unknowns: {p.get('unknowns')}\n")
        out.write("-" * 40 + "\n")
