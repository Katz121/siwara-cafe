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


// Load map.js code

const mapApp = document.getElementById('interactive-map-app');
if (mapApp) {
  const BASE = (document.documentElement.dataset.base || '');
  const data = JSON.parse(mapApp.getAttribute('data-map-data'));
  
  const catLabels = {
      'temple': 'วัด',
      'shrine': 'ศาลเจ้าและโรงเจ',
      'heritage': 'อาคารและมรดกเมือง',
      'museum': 'พิพิธภัณฑ์',
      'park': 'สวนสาธารณะ',
      'market': 'ตลาด',
      'street': 'ถนนสายวัฒนธรรม',
      'food_center': 'ศูนย์อาหาร',
      'tradition': 'ประเพณี'
  };

  const catColors = {
      'temple': '#e8a931',
      'shrine': '#d54d3f',
      'heritage': '#6a8473',
      'park': '#4d8359',
      'market': '#a86749',
      'museum': '#556885',
      'street': '#885053',
      'food_center': '#d49635',
      'tradition': '#896499'
  };

  const hasCoords = data.filter(d => d.coords);
  const noCoords = data.filter(d => !d.coords);
  
  // Calculate center
  let sumLng = 0, sumLat = 0;
  hasCoords.forEach(d => { sumLng += d.coords[0]; sumLat += d.coords[1]; });
  const center = [sumLng / hasCoords.length, sumLat / hasCoords.length];

  // Build UI
  mapApp.innerHTML = `
    <div class="map-filter-bar">
      <div class="map-filter-buttons" id="map-filters">
         <button data-cat="all" class="active">ทั้งหมด</button>
         ${Array.from(new Set(hasCoords.map(d=>d.category))).map(cat => 
            `<button data-cat="${cat}">${catLabels[cat] || cat}</button>`
         ).join('')}
      </div>
      <div class="map-count" id="map-count">เห็นอยู่ ${hasCoords.length} จุด</div>
    </div>
    
    <div class="map-layout">
      <div class="map-sidebar">
        <ul id="map-list" class="map-list">
          ${hasCoords.map(d => `
            <li data-id="${d.id}" data-cat="${d.category}" tabindex="0">
              <strong>${d.name}</strong><br>
              <small>${catLabels[d.category] || d.category}</small>
            </li>
          `).join('')}
        </ul>
        <h3 class="missing-coords-heading">ยังไม่มีพิกัด · รอปักหมุด</h3>
        <ul class="map-list map-list-missing">
          ${noCoords.map(d => `
            <li>
              <strong>${d.name}</strong><br>
              <small>${d.address || 'ยังไม่ทราบที่อยู่'}</small>
            </li>
          `).join('')}
        </ul>
      </div>
      
      <div class="map-main">
        <div id="map-container" style="height: 600px; width: 100%;"></div>
        <div class="map-legend">
          ${Array.from(new Set(hasCoords.map(d=>d.category))).map(cat => `
            <span class="legend-item"><i style="background:${catColors[cat] || '#333'}"></i> ${catLabels[cat] || cat}</span>
          `).join('')}
        </div>
        <div class="map-controls">
           <label>
             <input type="checkbox" id="overlay-toggle"> ซ้อนภาพแผนที่เทศบาล
           </label>
           <input type="range" id="overlay-opacity" min="0" max="1" step="0.05" value="0.6">
           <span class="map-note">ภาพแผนที่เทศบาลวางทับแบบประมาณ · ไม่ใช่การอ้างอิงตำแหน่งแม่นยำ</span>
           <a class="full-map-link" href="${BASE}/assets/municipal-map.png" target="_blank" rel="noopener">เปิดภาพแผนที่เทศบาลฉบับเต็ม ↗</a>
        </div>
      </div>
    </div>
  `;

  // Init MapLibre
  const map = new maplibregl.Map({
      container: 'map-container',
      style: 'https://tiles.openfreemap.org/styles/liberty',
      center: center,
      zoom: 15,
      pitchWithRotate: false,
      dragRotate: false
  });
  
  map.addControl(new maplibregl.NavigationControl({showCompass: false}));

  const markers = {};
  
  hasCoords.forEach(d => {
      // Create a marker using default maplibre marker but colored
      const marker = new maplibregl.Marker({ color: catColors[d.category] || '#333' })
          .setLngLat(d.coords)
          .addTo(map);
          
      const popupHtml = `
          <div class="map-popup">
              ${d.photo ? `<img src="${d.photo}" alt="${d.name}" style="width:100%;height:140px;object-fit:cover;">` : ''}
              <div style="padding: 10px;">
                  <h3 style="margin:0 0 5px;font-size:1.1rem;">${d.name}</h3>
                  <span class="eyebrow" style="display:block;margin-bottom:8px;">${catLabels[d.category] || d.category}</span>
                  <p style="font-size:0.875rem;margin:0 0 15px;line-height:1.5;">${d.kicker}</p>
                  <div class="popup-actions" style="display:flex;gap:10px;">
                      <a href="${d.url}" class="button" style="min-height:36px;padding:6px 12px;font-size:0.8rem;gap:6px;">เปิดหน้าเต็ม</a>
                      <a href="https://www.google.com/maps/search/?api=1&query=${d.coords[1]},${d.coords[0]}" target="_blank" rel="noopener" class="button button-outline" style="min-height:36px;padding:6px 12px;font-size:0.8rem;border:1px solid currentColor;">นำทาง ↗</a>
                  </div>
              </div>
          </div>
      `;
      
      const popup = new maplibregl.Popup({ offset: 25, maxWidth: '280px' }).setHTML(popupHtml);
      marker.setPopup(popup);
      markers[d.id] = { marker, data: d };
  });

  // Layer overlay
  map.on('load', () => {
      map.addSource('municipal-map', {
          type: 'image',
          url: BASE + '/assets/municipal-map.png',
          coordinates: [
              [98.349, 8.840],
              [98.368, 8.840],
              [98.368, 8.825],
              [98.349, 8.825]
          ]
      });
      map.addLayer({
          id: 'municipal-overlay',
          type: 'raster',
          source: 'municipal-map',
          paint: {
              'raster-opacity': 0
          }
      });
  });

  const toggle = document.getElementById('overlay-toggle');
  const opacity = document.getElementById('overlay-opacity');
  
  if (toggle && opacity) toggle.addEventListener('change', (e) => {
      if (map.getLayer('municipal-overlay')) {
          map.setPaintProperty('municipal-overlay', 'raster-opacity', e.target.checked ? parseFloat(opacity.value) : 0);
      }
  });
  
  opacity.addEventListener('input', (e) => {
      if (toggle.checked && map.getLayer('municipal-overlay')) {
          map.setPaintProperty('municipal-overlay', 'raster-opacity', parseFloat(e.target.value));
      }
  });

  // Filtering
  const filterBtns = document.querySelectorAll('#map-filters button');
  const countEl = document.getElementById('map-count');
  
  filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
          filterBtns.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          const cat = btn.dataset.cat;
          let count = 0;
          
          Object.values(markers).forEach(m => {
              if (cat === 'all' || m.data.category === cat) {
                  m.marker.addTo(map);
                  count++;
              } else {
                  m.marker.remove();
              }
          });
          
          document.querySelectorAll('#map-list li').forEach(li => {
              li.style.display = (cat === 'all' || li.dataset.cat === cat) ? '' : 'none';
          });
          
          countEl.textContent = `เห็นอยู่ ${count} จุด`;
      });
  });

  // List hover/click
  document.querySelectorAll('#map-list li').forEach(li => {
      li.addEventListener('click', () => {
          const id = li.dataset.id;
          const m = markers[id];
          if (m) {
              map.flyTo({ center: m.data.coords, zoom: 17 });
              m.marker.togglePopup();
          }
      });
  });
}
