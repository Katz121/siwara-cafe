import codecs

css = """
/* --- V2 Story & News styles --- */

/* Base story v2 layout */
.story-layout-v2 {
  display: grid;
  grid-template-columns: 1fr;
  gap: 2rem;
  padding: 0 1rem;
  max-width: 1200px;
  margin: 0 auto;
}
@media (min-width: 900px) {
  .story-layout-v2 { grid-template-columns: 2fr 1fr; gap: 4rem; }
}
.story-hero-v2 {
  padding: 2rem 1rem;
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}
.story-hero-v2 h1 { font-family: 'Noto Serif Thai', serif; font-size: 2.2rem; color: #203f39; margin-bottom: 0.5rem; }
.story-hero-v2 .lead { font-size: 1.1rem; color: #3a5c53; }
.story-meta { font-size: 0.9rem; color: #6b7a70; }

.hero-photo-v2 { margin: 0 auto 2rem; max-width: 1000px; }
.hero-photo-v2 img, .section-photo-v2 img, .card-art-v2 img { width: 100%; height: auto; border-radius: 8px; }
.hero-photo-v2 figcaption, .section-photo-v2 figcaption { font-size: 0.8rem; color: #6b7a70; text-align: center; margin-top: 0.5rem; }
.credit { display: block; font-size: 0.75rem; opacity: 0.8; }

.story-lede-v2 p {
  font-size: 1.15rem;
  line-height: 1.7;
  color: #203f39;
  font-family: 'Noto Serif Thai', serif;
}

.story-section-v2 h2 { font-family: 'Noto Serif Thai', serif; color: #203f39; margin-top: 2rem; }
.story-section-v2 p { line-height: 1.6; margin-bottom: 1rem; }

.story-flags-v2 { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 1rem; }
.story-flag-v2 { font-size: 0.8rem; padding: 4px 8px; border-radius: 4px; display: inline-block; }
.flag-unverified { background-color: #fff9c4; color: #7f6000; }
.flag-disputed { background-color: #ffe0b2; color: #e65100; }

.pull-quote-v2 {
  margin: 2rem 0;
  padding: 1.5rem;
  border-left: 4px solid #a3492f;
  background: #f6f1e6;
  font-family: 'Noto Serif Thai', serif;
  font-size: 1.3rem;
  color: #203f39;
  font-style: italic;
}

.evidence-box-v2 {
  background: #fff;
  border: 1px solid #dcd7ce;
  padding: 1.5rem;
  border-radius: 8px;
  position: sticky;
  top: 2rem;
  margin-bottom: 2rem;
}
.evidence-box-v2 h3 { margin-top: 0; color: #a3492f; }
.ev-items-v2 { list-style: none; padding: 0; margin: 0; }
.ev-items-v2 li { margin-bottom: 1.5rem; padding-bottom: 1.5rem; border-bottom: 1px solid #eee; }
.ev-items-v2 li:last-child { border: none; padding-bottom: 0; margin-bottom: 0; }
.ev-claim { font-weight: bold; margin-bottom: 0.5rem; }
.ev-status { display: inline-block; font-size: 0.75rem; padding: 2px 6px; border-radius: 4px; font-weight: bold; margin-bottom: 0.5rem; }
.ev-status.unverified { background: #fff9c4; color: #7f6000; }
.ev-status.disputed { background: #ffe0b2; color: #e65100; }
.ev-explain { font-size: 0.9rem; }

.story-places-v2, .story-sources-v2 { margin-top: 3rem; }
.mini-cards-v2 { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); }
.place-card-mini { background: #fff; border: 1px solid #eee; border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; }
.place-card-mini img { height: 120px; object-fit: cover; }
.place-card-mini div { padding: 1rem; display: flex; flex-direction: column; flex-grow: 1; }
.place-card-mini h4 { margin: 0 0 1rem 0; font-size: 1rem; }
.place-card-mini button { margin-top: auto; min-height: 44px; }

.unknowns-box-v2 { margin-top: 2rem; background: #faf8f5; border: 1px dashed #ccc; padding: 1rem; border-radius: 8px; }
.unknowns-box-v2 summary { font-weight: bold; cursor: pointer; min-height: 44px; display: flex; align-items: center; }
.unknowns-box-v2 ul { padding-left: 1.5rem; margin-top: 0.5rem; }

.story-sidebar-v2 { display: flex; flex-direction: column; gap: 2rem; }
.story-toc-v2 { position: sticky; top: 2rem; background: #f6f1e6; padding: 1rem; border-radius: 8px; }
.story-toc-v2 h2 { margin-top: 0; font-size: 1.1rem; }
.story-toc-v2 ul { list-style: none; padding: 0; margin: 0; }
.story-toc-v2 li { margin-bottom: 0.5rem; }
.story-toc-v2 a { text-decoration: none; color: #3a5c53; display: block; min-height: 32px; display: flex; align-items: center; }
.story-toc-v2 a:hover, .story-toc-v2 a.active { color: #a3492f; font-weight: bold; }

.story-grid-v2 { display: grid; gap: 1.5rem; grid-template-columns: 1fr; max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
@media (min-width: 768px) {
  .story-grid-v2 { grid-template-columns: 1fr 1fr; }
  .story-card-v2-lead { grid-column: span 2; display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; align-items: center; }
}
.story-card-v2 { background: #fff; border-radius: 8px; overflow: hidden; display: flex; flex-direction: column; text-decoration: none; color: inherit; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: transform 0.2s; }
.story-card-v2:hover { transform: translateY(-4px); }
.card-art-v2 img { height: 200px; object-fit: cover; }
.card-content-v2 { padding: 1.5rem; display: flex; flex-direction: column; flex-grow: 1; }
.card-meta-v2 { margin-top: auto; padding-top: 1rem; display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; }

.news-page { max-width: 800px; margin: 0 auto; padding: 2rem 1rem; }
.news-filters { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 2rem; }
.news-filters button { padding: 0.5rem 1rem; min-height: 44px; border: 1px solid #203f39; border-radius: 20px; background: transparent; color: #203f39; cursor: pointer; transition: 0.2s; }
.news-filters button[aria-pressed="true"] { background: #203f39; color: #f6f1e6; }
.news-list-full { display: flex; flex-direction: column; gap: 1.5rem; }
.news-item { padding-bottom: 1.5rem; border-bottom: 1px solid #dcd7ce; display: grid; gap: 1rem; }
@media (min-width: 600px) {
  .news-item { grid-template-columns: 100px 1fr; }
}
.news-item time { font-weight: bold; color: #6b7a70; }
.news-item h2 { margin: 0 0 0.5rem 0; font-size: 1.2rem; }
.news-item p { margin: 0 0 0.5rem 0; }

@media (prefers-reduced-motion: reduce) {
  .story-card-v2 { transition: none; }
  .story-card-v2:hover { transform: none; }
}
"""
with codecs.open('site/assets/design.css', 'a', 'utf-8') as f:
    f.write(css)
