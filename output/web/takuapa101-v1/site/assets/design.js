/* Progressive enhancement: all records and the original map remain usable without JS. */
for (const explorer of document.querySelectorAll('[data-explorer]')) {
  const buttons = [...explorer.querySelectorAll('[data-filter]')];
  const cards = [...explorer.querySelectorAll('[data-place-card]')];
  const input = explorer.querySelector('[data-place-search]');
  let category = 'all';
  const filter = () => {
    const query = (input?.value || '').trim().normalize('NFC').toLocaleLowerCase('th');
    let count = 0;
    for (const card of cards) {
      card.hidden = !((category === 'all' || card.dataset.category === category) && card.dataset.name.normalize('NFC').toLocaleLowerCase('th').includes(query));
      if (!card.hidden) count++;
    }
    for (const button of buttons) button.setAttribute('aria-pressed', String(button.dataset.filter === category));
    explorer.querySelector('[data-place-count]').textContent = `${count} สถานที่ให้ค่อย ๆ รู้จัก`;
    explorer.querySelector('[data-place-empty]').hidden = count !== 0;
  };
  for (const button of buttons) button.addEventListener('click', () => { category = button.dataset.filter; filter(); });
  input?.addEventListener('input', filter);
  if (input && new URLSearchParams(location.search).has('q')) { input.value = new URLSearchParams(location.search).get('q'); filter(); }
  explorer.querySelector('[data-clear-places]').addEventListener('click', () => {category='all';if(input) input.value='';filter();buttons[0].focus();});
}

const search = document.querySelector('#shop-search');
if (search) {
  const category = document.querySelector('#shop-category');
  const groups = [...document.querySelectorAll('.shop-group')];
  const filter = () => {
    let total=0;
    const query=search.value.trim().normalize('NFC').toLocaleLowerCase('th');
    for(const group of groups){let count=0;for(const row of group.querySelectorAll('[data-shop]')){
      row.hidden=!((category.value==='all'||category.value===group.dataset.category)&&row.dataset.shop.normalize('NFC').toLocaleLowerCase('th').includes(query));
      if(!row.hidden)count++;
    }group.hidden=count===0;total+=count;}
    document.querySelector('#results').textContent=`แสดง ${total} ร้าน`;
    document.querySelector('#empty').hidden=total!==0;
  };
  search.addEventListener('input',filter);category.addEventListener('change',filter);
  document.querySelector('#clear-shops').addEventListener('click',()=>{search.value='';category.value='all';filter();search.focus();});
}

const viewer = document.querySelector('[data-map-viewer]');
if (viewer) {
  const stage=viewer.querySelector('.map-stage');
  const image=stage.querySelector('img');
  const level=viewer.querySelector('[data-map-level]');
  const zones=[...viewer.querySelectorAll('[data-map-zone]')];
  let width=0,height=0,fit=1,scale=1,x=0,y=0,activeZone='full';
  const pointers=new Map();
  let gesture=null;
  const maxScale=()=>fit*7;
  const clamp=(v,min,max)=>Math.min(max,Math.max(min,v));
  function render(){
    const iw=image.naturalWidth*scale,ih=image.naturalHeight*scale;
    x=iw<=width?(width-iw)/2:clamp(x,width-iw,0);
    y=ih<=height?(height-ih)/2:clamp(y,height-ih,0);
    image.style.transform=`translate(${x}px, ${y}px) scale(${scale})`;
    level.textContent=`${Math.round(scale/fit*100)}%`;
    viewer.querySelector('[data-map-action="out"]').disabled=scale<=fit*1.001;
    viewer.querySelector('[data-map-action="in"]').disabled=scale>=maxScale()*.999;
    for(const button of zones)button.setAttribute('aria-pressed',String(button.dataset.mapZone===activeZone));
  }
  function zoom(factor,cx=width/2,cy=height/2){
    const next=clamp(scale*factor,fit,maxScale());
    x=cx-(cx-x)*next/scale;y=cy-(cy-y)*next/scale;scale=next;activeZone='';render();
  }
  function zone(name){
    activeZone=name;
    const W=image.naturalWidth,H=image.naturalHeight;
    // Framing regions refer to the two labeled panels in the supplied source artwork.
    const bounds=name==='north'?[0,0,W,H*.345]:name==='old'?[0,H*.34,W,H*.48]:[0,0,W,H];
    const regionFit=Math.min(width/bounds[2],height/bounds[3]);
    scale=clamp(name==='full'?regionFit:Math.max(regionFit,fit*2),fit,maxScale());
    x=width/2-(bounds[0]+bounds[2]/2)*scale;y=height/2-(bounds[1]+bounds[3]/2)*scale;render();
  }
  for(const button of zones)button.addEventListener('click',()=>zone(button.dataset.mapZone));
  for(const button of viewer.querySelectorAll('[data-map-action]'))button.addEventListener('click',()=>{
    if(button.dataset.mapAction==='reset')zone('full');else zoom(button.dataset.mapAction==='in'?1.4:1/1.4);
  });
  stage.addEventListener('keydown',event=>{
    if(['+','=','-','ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home'].includes(event.key)){
      event.preventDefault();
      if(event.key==='+'||event.key==='=')zoom(1.4);
      else if(event.key==='-')zoom(1/1.4);
      else if(event.key==='Home')zone('full');
      else {x+=event.key==='ArrowLeft'?60:event.key==='ArrowRight'?-60:0;y+=event.key==='ArrowUp'?60:event.key==='ArrowDown'?-60:0;activeZone='';render();}
    }
  });
  function local(event){const rect=stage.getBoundingClientRect();return{x:event.clientX-rect.left,y:event.clientY-rect.top};}
  function beginGesture(){
    const pts=[...pointers.values()];
    if(pts.length>=2){const a=pts[0],b=pts[1];gesture={kind:'pinch',distance:Math.hypot(b.x-a.x,b.y-a.y),cx:(a.x+b.x)/2,cy:(a.y+b.y)/2,x,y,scale};}
    else if(pts.length)gesture={kind:'pan',px:pts[0].x,py:pts[0].y,x,y};else gesture=null;
  }
  stage.addEventListener('pointerdown',event=>{
    if(event.pointerType==='mouse'&&event.button!==0)return;
    stage.setPointerCapture(event.pointerId);pointers.set(event.pointerId,local(event));stage.classList.add('dragging');beginGesture();
  });
  stage.addEventListener('pointermove',event=>{
    if(!pointers.has(event.pointerId)||!gesture)return;
    pointers.set(event.pointerId,local(event));const pts=[...pointers.values()];activeZone='';
    if(gesture.kind==='pinch'&&pts.length>=2){const a=pts[0],b=pts[1];const next=clamp(gesture.scale*Math.hypot(b.x-a.x,b.y-a.y)/Math.max(1,gesture.distance),fit,maxScale());x=(a.x+b.x)/2-(gesture.cx-gesture.x)*next/gesture.scale;y=(a.y+b.y)/2-(gesture.cy-gesture.y)*next/gesture.scale;scale=next;}
    else{x=gesture.x+pts[0].x-gesture.px;y=gesture.y+pts[0].y-gesture.py;}
    render();
  });
  const end=event=>{pointers.delete(event.pointerId);if(!pointers.size)stage.classList.remove('dragging');beginGesture();};
  stage.addEventListener('pointerup',end);stage.addEventListener('pointercancel',end);stage.addEventListener('lostpointercapture',end);
  function initialize(){
    if(!image.naturalWidth)return;
    image.style.width=`${image.naturalWidth}px`;
    image.style.height=`${image.naturalHeight}px`;
    stage.classList.add('ready');
    const resize=()=>{width=stage.clientWidth;height=stage.clientHeight;fit=Math.min(width/image.naturalWidth,height/image.naturalHeight);zone(activeZone||'full');};
    new ResizeObserver(resize).observe(stage);resize();
  }
  if(image.complete)initialize();else image.addEventListener('load',initialize,{once:true});
}

// Phase 3: keep both photo groups visible until enhanced controls are ready.
for (const gallery of document.querySelectorAll('[data-gallery]')) {
  const bar=gallery.querySelector('.gallery-tabs'), tabs=[...bar.querySelectorAll('[data-tab]')];
  const panels=[...gallery.querySelectorAll('[data-panel]')];
  bar.hidden=false;bar.setAttribute('role','tablist');bar.setAttribute('aria-label','ช่วงเวลาของภาพ');
  const select=(index)=>{tabs.forEach((tab,i)=>{tab.setAttribute('aria-selected',String(i===index));tab.tabIndex=i===index?0:-1;panels[i].hidden=i!==index;});};
  tabs.forEach((tab,i)=>{tab.id=`tab-${tab.dataset.tab}`;tab.setAttribute('role','tab');tab.setAttribute('aria-controls',panels[i].id);panels[i].setAttribute('role','tabpanel');panels[i].setAttribute('aria-labelledby',tab.id);tab.addEventListener('click',()=>select(i));tab.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();const n=e.key==='Home'?0:e.key==='End'?tabs.length-1:(i+(e.key==='ArrowRight'?1:tabs.length-1))%tabs.length;select(n);tabs[n].focus();}});});
  select(0);
}
if(document.querySelector('[data-lightbox]') && typeof HTMLDialogElement!=='undefined'){
  const dialog=document.createElement('dialog');dialog.className='photo-dialog';dialog.setAttribute('aria-label','ภาพขยาย');
  const close=document.createElement('button');close.type='button';close.textContent='ปิดภาพ ×';dialog.append(close);document.body.append(dialog);
  let trigger=null;
  close.addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});dialog.addEventListener('close',()=>trigger?.focus());
  document.querySelectorAll('[data-lightbox]').forEach(a=>a.addEventListener('click',e=>{if(e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;e.preventDefault();trigger=a;dialog.querySelector('figure')?.remove();const figure=a.closest('figure').cloneNode(true);const anchor=figure.querySelector('a[data-lightbox]');anchor.replaceWith(anchor.querySelector('img'));figure.querySelector('img').loading='eager';dialog.append(figure);dialog.showModal();close.focus();}));
}
const readingLinks=[...document.querySelectorAll('.research-rail a')];
if(readingLinks.length){
  let queued=false;
  const mark=()=>{queued=false;let active=readingLinks[0];for(const a of readingLinks){const section=document.querySelector(a.getAttribute('href'));if(section && section.getBoundingClientRect().top<=180)active=a;}readingLinks.forEach(a=>{if(a===active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});};
  window.addEventListener('scroll',()=>{if(!queued){queued=true;requestAnimationFrame(mark);}},{passive:true});mark();
}
