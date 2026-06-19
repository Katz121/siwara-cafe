// สร้าง gmaps-config.js จาก environment variable ตอน build (Vercel)
// key จะไม่อยู่ใน git · ตั้งค่า SS_GMAPS_KEY ใน Vercel → Settings → Environment Variables
const fs = require('fs');
const key = process.env.SS_GMAPS_KEY || '';
fs.writeFileSync('gmaps-config.js', 'window.SS_GMAPS_KEY=' + JSON.stringify(key) + ';\n');
console.log('gmaps-config.js generated · key ' + (key ? 'set ('+key.length+' chars)' : 'EMPTY → fallback local images'));
