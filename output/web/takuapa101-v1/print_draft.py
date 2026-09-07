import json
d = json.load(open('ui_draft.json', encoding='utf-8'))
for i, k in enumerate(list(d.keys())[:50]):
    print(k.encode('utf-8').decode('utf-8'))  # this will fail to print on cp1252 console.
