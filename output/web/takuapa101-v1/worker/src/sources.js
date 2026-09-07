/* Where city news comes from. Google News RSS needs no key; the .go.th feeds are
   read directly. Facebook pages need a page token, so they stay disabled until
   one is configured (see FB_PAGES in the README). */

export const GOOGLE_NEWS_QUERIES = [
  'ตะกั่วป่า',
  'เมืองเก่าตะกั่วป่า',
  '"ตะกั่วป่า" เทศกาล',
  '"ตะกั่วป่า" ประเพณี',
  'ถนนสายวัฒนธรรม ตะกั่วป่า',
  'ตะกั่วป่า พังงา ท่องเที่ยว',
  'ตะโกลา พังงา',
  'กั่วป่าโพ้',
];

/* Direct feeds. Each entry: {id, name, url, kind: 'rss' | 'html', authority} */
export const DIRECT_SOURCES = [
  { id: 'takuapacity', name: 'เทศบาลเมืองตะกั่วป่า', url: 'https://www.takuapacity.go.th/news', kind: 'html', authority: 'official' },
  { id: 'tat-phangnga', name: 'ททท. สำนักงานพังงา', url: 'https://thai.tourismthailand.org/Search-result?keyword=%E0%B8%95%E0%B8%B0%E0%B8%81%E0%B8%B1%E0%B9%88%E0%B8%A7%E0%B8%9B%E0%B9%88%E0%B8%B2', kind: 'html', authority: 'official' },
  { id: 'finearts', name: 'กรมศิลปากร', url: 'https://www.finearts.go.th/main/categories/news', kind: 'html', authority: 'official' },
];

/* Set FB_PAGES as a Worker secret: JSON [{id, name, page_id}] plus FB_TOKEN. */
export const FB_ENABLED_HINT = 'ตั้งค่า secret FB_TOKEN และ FB_PAGES เพื่อเปิดการดึงจากเพจ';

/* Siwara's own events feed, published by the shop itself. */
export const FIRST_PARTY = [
  { id: 'siwara', name: 'ศิวรา คาเฟ่', url: 'https://siwaracafe.com/api/events.json', kind: 'json', authority: 'first-party' },
];

/* An item must mention the town. Without this, national tourism stories and
   province-wide weather bulletins flood the feed. */
export const REQUIRE_ANY = ['ตะกั่วป่า', 'ตะโกลา', 'กั่วป่าโพ้', 'Takua Pa', 'Takuapa'];

/* Categories that mention the town but are not city news. */
export const BLOCK_PATTERNS = [
  /ดัชนีคุณภาพอากาศ|คุณภาพอากาศ|AQI|IQAir/i,
  /พยากรณ์อากาศประจำวัน|อุณหภูมิวันนี้/i,
  /ขายที่ดิน|ขายบ้าน|ให้เช่า|คอนโด|ประกาศขาย|นายหน้า/i,
  /หวย|เลขเด็ด|สลากกินแบ่ง/i,
  /ราคาน้ำมันวันนี้|ราคาทองวันนี้/i,
  /โปรโมชั่น|ส่วนลด|ดีลเด็ด|ราคาถูกที่สุด/i,
  /อุบัติเหตุ|ฆ่า|ยิง|ข่มขืน|จับกุมยาเสพติด|ศพ/i,
];

/* Outlets we will publish without a human reading them first. */
export const OUTLET_ALLOWLIST = [
  'thairath', 'matichon', 'khaosod', 'dailynews', 'bangkokbiznews', 'prachachat',
  'thansettakij', 'posttoday', 'siamrath', 'naewna', 'mgronline', 'ผู้จัดการออนไลน์',
  'topnews', 'nationtv', 'pptvhd36', 'thaipbs', 'ch7', 'ch3plus', 'amarintv',
  'springnews', 'komchadluek', 'sanook', 'kapook', 'thaipost', 'innnews',
  'nbt', 'prd.go.th', 'thainews', 'สวพ', 'มติชน', 'ไทยรัฐ', 'แนวหน้า', 'สยามรัฐ',
  'tourismthailand', 'finearts.go.th', 'takuapacity.go.th', 'phangnga',
  'youphuket', 'phuketnews', 'andamannews', 'line.me',
];

/* Which place a story belongs to. First match wins. */
export const PLACE_KEYWORDS = {
  'wat-boromthat': ['บรมธาตุคีรีเขต', 'วัดลุ่ม', 'พระธาตุคีรีเขต', 'เขาพระบาท'],
  'wat-khuha': ['คุหาภิมุข', 'วัดควนถ้ำ'],
  'wat-pathum': ['ปทุมธารา', 'วัดหน้าเมือง'],
  'wat-kongkha': ['คงคาภิมุข', 'วัดคงคา'],
  'wat-nikorn': ['นิกรวราราม', 'วัดย่านยาว'],
  'wat-sena': ['เสนานุชรังสรรค์', 'วัดใหม่'],
  'museum': ['พิพิธภัณฑ์'],
  'guan-yu': ['กวนอู', 'ซิ่นไช่ตึ๋ง'],
  'pun-thao': ['ปุนเถ่ากง'],
  'kue-chai': ['กู่ใช่ตึ๋ง'],
  'rong-jae': ['โรงเจ'],
  'phra-narai': ['พระนารายณ์'],
  'thung-phra': ['ทุ่งพระโพธิ์'],
  'riverwalk': ['ตลาดริมน้ำ', 'ริมน้ำตะกั่วป่า'],
  'culture-street': ['ถนนสายวัฒนธรรม', 'ถนนคนเดิน', 'เมืองเก่าตะกั่วป่า', 'ชิโน'],
  'iron-bridge': ['สะพานเหล็ก', 'บุญสูง'],
  'governor-wall': ['จวนเจ้าเมือง', 'กำแพงเมือง'],
  'khun-in': ['ขุนอินทร์', 'บ้านขุนอิน'],
  'tao-ming': ['เต้าหมิง', 'เต๋าหมิง'],
  'food-center': ['ศูนย์อาหาร', 'ลานโล่ง'],
  'vegetarian': ['กินเจ', 'กินผัก', 'ถือศีลกินผัก', 'อ๋องฉ่าย'],
  'loy-krathong': ['ลอยกระทง'],
  'chak-phra': ['ชักพระ', 'เรือพระ'],
  'new-year-alms': ['ตักบาตร', 'สงกรานต์', 'ปีใหม่'],
  'narai-ceremony': ['บวงสรวง' , 'เทวรูปพระนารายณ์'],
  'ruler-ceremony': ['บวงสรวงเจ้าเมือง'],
  'relic-procession': ['พระบรมสารีริกธาตุ', 'แห่พระธาตุ'],
};
