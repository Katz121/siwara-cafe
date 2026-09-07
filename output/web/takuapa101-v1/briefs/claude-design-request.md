# Takuapa101 architecture and visual direction

Act as a senior Thai tourism editorial website designer and technical SEO architect. User explicitly requests Claude's help. Return your proposal in Thai Markdown only. Read-only task; do not edit files or invoke other agents. Do not browse or read secrets.

Project: Takuapa101, an independent useful tourism guide to Takua Pa, Phang Nga, with contextual links to the owner's Siwara cafe at https://siwaracafe.com/. Goal is to promote the town, not a link farm. Need credible SEO and a premium editorial design combining traced street lines from the attached municipal map with already generated heritage illustrations. No cheap tourism template, no generic oversized card dashboard.

Read:
- D:/Siwaracafeweb/output/library/2026-09-06_takuapa-siwara-v1/data/library.json (86 extracted records: 20 places, 7 events, 59 businesses)
- D:/Siwaracafeweb/output/library/2026-09-06_takuapa-siwara-v1/data/production.json (20 current approved images)
- D:/Siwaracafeweb/output/library/2026-09-06_takuapa-siwara-v1/source/maps.png (image: municipal schematic town map; not surveyed coordinates)
- D:/Siwaracafeweb/output/library/2026-09-06_takuapa-siwara-v1/data/card-copy.json
- Optional current corrected card image: collections/2026-09-06_individual-places-v6/2026-09-06_pun-thao.png under the library directory.

Critical constraints:
- Corrected identities: Pun Thao Kong A = white-column pavilion; Rong Jae/The Shrine in the Garden = red Chinese gateway. Never undo this correction.
- Preserve source provenance, distinguish reviewed brochure facts from current visiting details not verified. Do not invent opening times, distance, GPS, prices, ratings, interview quotes, dates of events, live status of businesses, or cafe location on a map.
- Source brochure map pins represent schematic placement only. Derive street topology from the supplied map, keep trace and illustrations separate layers, provide accessible list fallback. Explain coverage gaps rather than invent positions for all 20.
- No audience captions containing the words the user previously deleted: ภาพวาดประกอบ / ภาพวาดจากภาพถ่ายบ้านศิวรา / ไม่ใช่แผนที่นำทาง / ภาพวาดประกอบจากภาพอ้างอิง.
- Avoid claiming schema guarantees rich results or ranking. Use relevant WebSite, BreadcrumbList, Article/Place vocabularies with accurate visible data; no fabricated rating or Event dates. Only publish indexable substantive pages. Names-only businesses should remain directory entries, not 59 thin SEO pages.
- Domain is not yet confirmed. Prototype stays local; no deployment. Canonical and sitemap production base must be configurable, not an invented owned domain.
- Relationship to Siwara should be transparent on About. Use selective useful contextual links with descriptive anchors, not repeated exact-match SEO links across all pages. Paid/sponsored links need proper rel qualification.

Deliver:
1. A clear homepage composition with exact Thai headings and navigation.
2. Information architecture, URL plan, content page template, category grouping and internal links for all data.
3. A design system: typography, restrained palette, spacing, map/linework treatment and mobile behavior.
4. Practical map layer plan, known limitations, interactions, and fallback.
5. Prioritized technical/content SEO implementation and a concrete Siwara link strategy.
6. Focused first prototype scope that can be built now from existing data; distinguish launch requirements and later enrichment.

Be specific, opinionated, compact (about 1200-1800 Thai words). Do not merely restate constraints. Your answer will be saved as the design brief and implemented by Codex.
