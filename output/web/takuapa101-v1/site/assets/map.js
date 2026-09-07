const mapApp = document.getElementById('interactive-map-app');
if (mapApp) {
  const data = JSON.parse(mapApp.getAttribute('data-map-data'));
  
  const catLabels = {
      'temple': '????????????',
      'shrine': '???????????????',
      'heritage': '??????????????????????',
      'museum': '??????????',
      'park': '????????????????????',
      'market': '?????????????',
      'street': '??????????????',
      'food_center': '??????????',
      'tradition': '???????'
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
         <button data-cat="all" class="active">???????</button>
         ${Array.from(new Set(hasCoords.map(d=>d.category))).map(cat => 
            `<button data-cat="${cat}">${catLabels[cat] || cat}</button>`
         ).join('')}
      </div>
      <div class="map-count" id="map-count">???? ${hasCoords.length} ????</div>
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
        <h3 class="missing-coords-heading">????????????? ?????????</h3>
        <ul class="map-list map-list-missing">
          ${noCoords.map(d => `
            <li>
              <strong>${d.name}</strong><br>
              <small>${d.address || '???????????????'}</small>
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
             <input type="checkbox" id="overlay-toggle"> ???????????????????
           </label>
           <input type="range" id="overlay-opacity" min="0" max="1" step="0.05" value="0.6">
           <span class="map-note">?????????????????????????????? ?????????????????????????????</span>
           <a class="full-map-link" href="/assets/municipal-map.png" target="_blank" rel="noopener">?????????????????????????????? ? ?</a>
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
                      <a href="${d.url}" class="button" style="min-height:36px;padding:6px 12px;font-size:0.8rem;gap:6px;">????????????</a>
                      <a href="https://www.google.com/maps/search/?api=1&query=${d.coords[1]},${d.coords[0]}" target="_blank" rel="noopener" class="button button-outline" style="min-height:36px;padding:6px 12px;font-size:0.8rem;border:1px solid currentColor;">????? ?</a>
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
          url: '/assets/municipal-map.png',
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
  
  toggle.addEventListener('change', (e) => {
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
          
          countEl.textContent = `???? ${count} ????`;
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
