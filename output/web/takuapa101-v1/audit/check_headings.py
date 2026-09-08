import glob,io,re,os,sys
sys.stdout.reconfigure(encoding='utf-8')
bad=0
for f in sorted(glob.glob('site/**/index.html',recursive=True)):
    html=io.open(f,encoding='utf-8').read()
    body=html.split('<main',1)[-1].split('</main>',1)[0]
    lv=[int(m) for m in re.findall(r'<h([1-6])[\s>]',body)]
    route='/'+os.path.relpath(os.path.dirname(f),'site').replace(os.sep,'/').strip('.')+'/'
    route=route.replace('//','/')
    issues=[]
    if lv.count(1)!=1: issues.append('h1 %d ตัว'%lv.count(1))
    for a,b in zip(lv,lv[1:]):
        if b>a+1: issues.append('h%d -> h%d'%(a,b))
    if issues: bad+=1; print('%-34s %s'%(route,' · '.join(dict.fromkeys(issues))))
print('หน้าที่มีปัญหา heading:',bad)
