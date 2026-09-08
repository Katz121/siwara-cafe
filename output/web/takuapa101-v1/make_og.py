"""สร้างภาพแบ่งปันจากภาพประกอบเดิม"""
import json, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps
from seo_config import ROOT
sys.stdout.reconfigure(encoding='utf-8')

FONT = ROOT/'fonts-src/IBMPlexSansThaiLooped-Regular.ttf'


def wrap_thai(draw, text, font, width):
    """ขึ้นบรรทัดใหม่ที่ขอบคำ · ไทยไม่เว้นวรรคระหว่างคำ การตัดตามตัวอักษรจะได้ 'เมือ/งเก่า'"""
    from pythainlp.tokenize import word_tokenize
    words = word_tokenize(text, engine='newmm', keep_whitespace=True)
    lines = ['']
    for w in words:
        if lines[-1] and draw.textlength(lines[-1] + w, font=font) > width:
            lines.append(w.lstrip())
        else:
            lines[-1] += w
    return [ln for ln in lines if ln.strip()] or ['']


def main():
    assets=ROOT/'site/assets';out=assets/'og';out.mkdir(exist_ok=True)
    records=json.loads((ROOT/'data/places-enriched.json').read_text(encoding='utf-8'))
    links=json.loads((ROOT/'data/links.json').read_text(encoding='utf-8'))
    for r in records+[{'id':'default','name_th':'คู่มือเมืองเก่าตะกั่วป่า'}]:
        image=Image.new('RGB',(1200,630),'#f6f1e7')
        art_id=r['id'] if (assets/(r['id']+'.webp')).exists() else next(iter(links.get(r['id'],[])), 'tao-ming')
        with Image.open(assets/(art_id+'.webp')) as source:
            art=ImageOps.contain(source.convert('RGB'),(570,510))
            image.paste(art,(615+(570-art.width)//2,(530-art.height)//2))
        draw=ImageDraw.Draw(image)
        name=r['name_th'].replace('—','·').replace('–','·')
        size=52
        while True:
            font=ImageFont.truetype(str(FONT),size)
            lines=wrap_thai(draw,name,font,530)
            if len(lines)<=4 or size<=30:break
            size-=2
        for i,line in enumerate(lines):draw.text((48,210-len(lines)*size//2+i*(size+22)),line,font=font,fill='#203f39')
        draw.rectangle((0,530,1200,630),fill='#203f39')
        draw.text((48,550),'ตะกั่วป่า 101',font=ImageFont.truetype(str(FONT),40),fill='#f6f1e7')
        image.save(out/(r['id']+'.png'))
    print(f'สร้างภาพ OG {len(records)+1} ภาพ · 1200×630')
if __name__=='__main__':main()
