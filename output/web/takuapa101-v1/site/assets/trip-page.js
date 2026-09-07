(function() {
    const app = document.getElementById('trip-app');
    if (!app) return;

    const BASE_PATH = document.documentElement.dataset.base || '';
    let placesMap = new Map();
    let tripList = [];

    async function init() {
        try {
            const res = await fetch(`${BASE_PATH}/assets/map-points.json`);
            const data = await res.json();
            
            (data.points || []).forEach(p => placesMap.set(p.id, p));
            (data.unlocated || []).forEach(p => placesMap.set(p.id, p));

            const urlParams = new URLSearchParams(window.location.search);
            const tripQuery = urlParams.get('trip');
            if (tripQuery) {
                const ids = tripQuery.split(',').filter(id => id.trim() !== '');
                if (window.TakuaTrip) {
                    window.TakuaTrip.clear();
                    ids.forEach(id => window.TakuaTrip.add(id));
                }
                const newUrl = window.location.pathname;
                window.history.replaceState({}, document.title, newUrl);
            }

            if (window.TakuaTrip) {
                tripList = [...window.TakuaTrip.list()];
                window.TakuaTrip.on((newList) => {
                    tripList = [...newList];
                    render();
                });
            }

            // Event delegation
            app.addEventListener('click', (e) => {
                const moveBtn = e.target.closest('button[data-move]');
                if (moveBtn) {
                    const idx = parseInt(moveBtn.dataset.idx, 10);
                    const dir = parseInt(moveBtn.dataset.dir, 10);
                    moveItem(idx, dir);
                }
                const removeBtn = e.target.closest('button[data-remove]');
                if (removeBtn) {
                    const id = removeBtn.dataset.remove;
                    if (window.TakuaTrip) window.TakuaTrip.remove(id);
                }
                
                if (e.target.closest('#btn-sort')) sortByDistance();
                if (e.target.closest('#btn-clear')) {
                    if (window.TakuaTrip) window.TakuaTrip.clear();
                }
                if (e.target.closest('#btn-print')) window.print();
                if (e.target.closest('#btn-copy')) copyLink();
            });

            render();
        } catch (e) {
            console.error('Failed to load map data', e);
            app.innerHTML = '<p>ไม่สามารถโหลดข้อมูลสถานที่ได้</p>';
        }
    }

    function haversine(lat1, lon1, lat2, lon2) {
        const R = 6371;
        const dLat = (lat2 - lat1) * Math.PI / 180;
        const dLon = (lon2 - lon1) * Math.PI / 180;
        const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
                  Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
                  Math.sin(dLon/2) * Math.sin(dLon/2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
        return R * c;
    }

    function sortByDistance() {
        if (tripList.length < 2) return;
        
        let sorted = [tripList[0]];
        let remaining = tripList.slice(1);
        
        while (remaining.length > 0) {
            const currentId = sorted[sorted.length - 1];
            const currentPlace = placesMap.get(currentId);
            
            if (!currentPlace || currentPlace.lat == null) {
                sorted = sorted.concat(remaining);
                break;
            }
            
            let nearestId = remaining[0];
            let minDest = Infinity;
            
            remaining.forEach(id => {
                const p = placesMap.get(id);
                if (p && p.lat != null) {
                    const d = haversine(currentPlace.lat, currentPlace.lng, p.lat, p.lng);
                    if (d < minDest) {
                        minDest = d;
                        nearestId = id;
                    }
                }
            });
            
            sorted.push(nearestId);
            remaining = remaining.filter(id => id !== nearestId);
        }
        
        if (window.TakuaTrip) {
            window.TakuaTrip.clear();
            sorted.forEach(id => window.TakuaTrip.add(id));
        } else {
            tripList = sorted;
            render();
        }
    }

    function moveItem(index, dir) {
        if (index + dir < 0 || index + dir >= tripList.length) return;
        const arr = [...tripList];
        const temp = arr[index];
        arr[index] = arr[index + dir];
        arr[index + dir] = temp;
        
        if (window.TakuaTrip) {
            window.TakuaTrip.clear();
            arr.forEach(id => window.TakuaTrip.add(id));
        } else {
            tripList = arr;
            render();
        }
    }

    function copyLink() {
        const url = new URL(window.location.href);
        url.searchParams.set('trip', tripList.join(','));
        const urlStr = url.toString();
        if (navigator.clipboard) {
            navigator.clipboard.writeText(urlStr).then(() => alert('คัดลอกลิงก์แล้ว')).catch(() => prompt('คัดลอกลิงก์นี้:', urlStr));
        } else {
            prompt('คัดลอกลิงก์นี้:', urlStr);
        }
    }

    function render() {
        if (tripList.length === 0) {
            app.innerHTML = `
                <div class="empty-state">
                    <h3>ทริปของคุณยังว่างอยู่</h3>
                    <p>ลองเลือกสถานที่จาก <a href="${BASE_PATH}/places/">สถานที่ทั้งหมด</a> หรือ <a href="${BASE_PATH}/map/">แผนที่</a></p>
                </div>
            `;
            return;
        }

        let totalDist = 0;
        let lastCoords = null;
        let waypoints = [];
        let missingCount = 0;

        const listHtml = tripList.map((id, index) => {
            const place = placesMap.get(id);
            if (!place) return '';

            if (place.lat != null) {
                if (lastCoords) {
                    totalDist += haversine(lastCoords.lat, lastCoords.lng, place.lat, place.lng);
                }
                lastCoords = { lat: place.lat, lng: place.lng };
                waypoints.push(`${place.lat},${place.lng}`);
            } else {
                missingCount++;
            }

            const imgStr = place.image ? `<img src="${place.image}" alt="${place.name_th}" width="120" height="120" loading="lazy">` : '';
            const coordStr = place.lat != null ? `<div class="print-coords" hidden>${place.lat.toFixed(5)}, ${place.lng.toFixed(5)}</div>` : '';

            return `
                <article class="trip-item">
                    <div class="trip-item-art">${imgStr}</div>
                    <div class="trip-item-info">
                        <h3><a href="${place.url || BASE_PATH + '/places/' + id + '/'}">${place.name_th}</a></h3>
                        <p class="small">${place.kicker || place.address || 'ไม่มีข้อมูลตำแหน่ง'}</p>
                        ${coordStr}
                    </div>
                    <div class="trip-item-actions">
                        <button type="button" class="button-outline" aria-label="เลื่อนขึ้น" data-move data-idx="${index}" data-dir="-1" ${index === 0 ? 'disabled' : ''}>ขึ้น</button>
                        <button type="button" class="button-outline" aria-label="เลื่อนลง" data-move data-idx="${index}" data-dir="1" ${index === tripList.length - 1 ? 'disabled' : ''}>ลง</button>
                        <button type="button" class="button-outline button-remove" aria-label="ลบ" data-remove="${id}">ลบ</button>
                    </div>
                </article>
            `;
        }).join('');

        let mapUrl = '';
        if (waypoints.length > 0) {
            const origin = waypoints[0];
            const dest = waypoints[waypoints.length - 1];
            const wpStr = waypoints.slice(1, -1).join('|');
            mapUrl = `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${dest}&travelmode=walking`;
            if (wpStr) mapUrl += `&waypoints=${wpStr}`;
        }

        app.innerHTML = `
            <div class="trip-controls no-print">
                <button type="button" class="button button-outline" id="btn-sort">เรียงตามระยะทาง</button>
                <button type="button" class="button button-outline" id="btn-clear">ล้างทั้งหมด</button>
                <button type="button" class="button button-outline" id="btn-print">พิมพ์</button>
                <button type="button" class="button button-outline" id="btn-copy">คัดลอกลิงก์ทริป</button>
                ${mapUrl ? `<a href="${mapUrl}" target="_blank" rel="noopener" class="button">เปิดใน Google Maps <span>↗</span></a>` : ''}
            </div>
            
            <div class="trip-summary">
                <p>ระยะรวมโดยประมาณ: <strong>${totalDist.toFixed(1)} กิโลเมตร</strong> <span class="small">(ระยะเส้นตรงโดยประมาณ ไม่ใช่ระยะเดินจริง)</span></p>
                ${missingCount > 0 ? `<p class="small">มี ${missingCount} สถานที่ที่ไม่มีพิกัด</p>` : ''}
            </div>

            <div class="trip-list">
                ${listHtml}
            </div>

            <div class="trip-rest-stop">
                <span class="eyebrow">แวะพักระหว่างเดิน</span>
                <h3>ศิวรา คาเฟ่</h3>
                <p>พักดื่มเครื่องดื่มเย็น ๆ ในบรรยากาศสบาย ๆ</p>
                <a href="https://siwaracafe.com/" target="_blank" rel="noopener" class="text-link">ดูรายละเอียดร้าน ↗</a>
            </div>
        `;
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
