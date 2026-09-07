import json

try:
    with open('data/stories/city.json', encoding='utf-8') as f:
        story = json.load(f)
    
    total_chars = len(story['title']) + len(story['dek'])
    for p in story['lede']:
        total_chars += len(p)
    for s in story['sections']:
        total_chars += len(s['heading_th'])
        for p in s['paragraphs']:
            total_chars += len(p)
            
    print("Successfully parsed city.json.")
    print("Total sections:", len(story['sections']))
    print("Total characters:", total_chars)
    # Check Thai text sample
    print("Sample Title:", story['title'])
except Exception as e:
    print("Error:", e)
