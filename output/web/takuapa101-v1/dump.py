import json

def dump():
    with open('dump.txt', 'w', encoding='utf-8') as out:
        data = json.load(open('data/places-enriched.json', encoding='utf-8'))
        for x in data:
            out.write(f"{x.get('id')}: {x.get('name_th')}\n")

        out.write("\n--- PHOTOS ---\n")
        try:
            p1 = json.load(open('data/photos-cc-manifest.json', encoding='utf-8'))
            if isinstance(p1, list):
                for p in p1: out.write(f"CC: {p.get('id', p.get('file'))} - {p.get('caption_th')}\n")
            else:
                for k, v in p1.items(): out.write(f"CC: {k} - {v.get('caption_th')}\n")
        except: pass

        try:
            p2 = json.load(open('data/photos-local.json', encoding='utf-8'))
            if isinstance(p2, list):
                for p in p2: out.write(f"LOCAL: {p.get('id', p.get('file'))} - {p.get('caption_th')}\n")
            else:
                for k, v in p2.items(): out.write(f"LOCAL: {k} - {v.get('caption_th')}\n")
        except: pass

if __name__ == '__main__':
    dump()
