from pathlib import Path
from PIL import Image
import json,shutil
R=Path(__file__).parent
L=R.parents[1]/'library/2026-09-06_takuapa-siwara-v1'
O=R/'site/assets';O.mkdir(parents=True,exist_ok=True)
s=json.loads((L/'data/production.json').read_text(encoding='utf-8'))
for k,v in s['records'].items():
 im=Image.open(L/v['approved_image']).convert('RGB');im.thumbnail((1000,1000));im.save(O/f'{k}.webp',quality=87,method=6)
for f in ['NotoSerifThai.ttf','IBMPlexSansThaiLooped-Regular.ttf','CormorantGaramond.ttf']:shutil.copy2(L/'assets'/f,O/f)
shutil.copy2(L/'source/maps.png',O/'municipal-map.png')
shutil.copy2(L/'data/library.json',R/'briefs/library-source.json')
(R/'data').mkdir(exist_ok=True)
shutil.copy2(L/'data/library.json',R/'data/library.json')
shutil.copy2(L/'data/card-copy.json',R/'data/card-copy.json')
print('Prepared 20 optimized images, 3 fonts and source map.')
