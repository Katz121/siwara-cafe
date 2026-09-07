import re, json
import codecs

def patch():
    fp = 'build_site.py'
    content = codecs.open(fp, 'r', 'utf-8').read()
    
    # 1. Add /news/ to nav
    if "('news', 'ความเคลื่อนไหว')" not in content:
        content = content.replace(
            "nav=[('places','สถานที่'),('map','แผนที่'),('traditions','ประเพณี'),('eat','กินและของฝาก'),('routes','เส้นทางเดิน'),('trip','ทริปของคุณ'),('about','เกี่ยวกับ')]",
            "nav=[('places','สถานที่'),('map','แผนที่'),('traditions','ประเพณี'),('eat','กินและของฝาก'),('routes','เส้นทางเดิน'),('trip','ทริปของคุณ'),('about','เกี่ยวกับ')]\nnav.insert(1, ('news', 'ความเคลื่อนไหว'))"
        )
        
    # 2. Render news page before sitemap writing
    
    news_render = """
def render_news():
    news_data = json.loads((DATA/'news-feed.json').read_text(encoding='utf-8'))
    places = sorted(list(set(n['place_name'] for n in news_data if n.get('place_name'))))
    years = sorted(list(set(n.get('date','2026')[:4] for n in news_data)), reverse=True)
    
    tabs = '<button type="button" data-news-filter="all" aria-pressed="true">ทั้งหมด</button>'
    for p in places: tabs += f'<button type="button" data-news-filter="{esc(p)}" aria-pressed="false">{esc(p)}</button>'
    for y in years: tabs += f'<button type="button" data-news-filter="{y}" aria-pressed="false">ปี {int(y)+543}</button>'
    
    items_html = ''
    jsonld_items = []
    
    for i, n in enumerate(news_data):
        d = n.get('date', '')
        d_th = ''
        y = d[:4] if d else ''
        if d:
            try:
                yx, m, dd = d.split('-')
                months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
                d_th = f'{int(dd)} {months[int(m)-1]} {int(yx)+543}'
            except:
                pass
                
        place_link = f'<a href="{esc(n["place_url"])}">{esc(n["place_name"])}</a>' if n.get("place_url") else ''
        title = esc(n.get("title_th", ""))
        summary = esc(n.get("summary_th", ""))
        outlet = esc(n.get("outlet", ""))
        url_link = esc(n.get("url", ""))
        link = f'<a class="news-out" href="{url_link}" target="_blank" rel="noopener">อ่านข่าวต้นทาง ↗</a>' if url_link else ''
        
        items_html += f'<article class="news-item" data-place="{esc(n.get("place_name",""))}" data-year="{y}"><time datetime="{d}">{d_th}</time><div class="news-content"><h2>{title}</h2><p>{summary}</p><div class="news-meta">{place_link}{" · " if place_link and outlet else ""}{outlet}</div>{link}</div></article>'
        
        jsonld_items.append({
            "@type": "ListItem",
            "position": i + 1,
            "item": {
                "@type": "NewsArticle",
                "headline": title,
                "datePublished": d,
                "url": url_link
            }
        })
        
    jsonld = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": jsonld_items
    }
    
    html = f'<div class="news-page"><div class="intro"><a class="eyebrow" href="/">ตะกั่วป่า 101 / คู่มือเมืองเก่า</a><h1>ความเคลื่อนไหวของเมือง</h1><p class="lead">ข่าวสารและกิจกรรมที่เกิดขึ้นในเมืองเก่าตะกั่วป่า</p></div><div class="news-filters" role="group" aria-label="กรองข่าวสาร">{tabs}</div><div class="news-list-full">{items_html}</div></div><script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False).replace("</", "<\\/")}</script>'
    return html

page('/news/','ความเคลื่อนไหวของเมือง','ข่าวสารและกิจกรรมในเมืองเก่าตะกั่วป่า',render_news())
"""
    
    if 'render_news()' not in content:
        content = content.replace('stories.write_audit()', news_render + '\nstories.write_audit()')
        
    # 3. Update stories iteration
    new_loop = """for story in stories.get_all_stories():
 page(story.get('route', f'/stories/{story["id"]}/'), story['title'], story['dek'], stories.article(story, {'byid': byid, 'pic': pic}))
"""
    content = re.sub(
        r"for story in stories\.STORIES:.*?\n page\(stories\.KUAPAPOH\['route'\].*?\n",
        new_loop,
        content,
        flags=re.DOTALL
    )

    codecs.open(fp, 'w', 'utf-8').write(content)

patch()
print('Patch applied')
