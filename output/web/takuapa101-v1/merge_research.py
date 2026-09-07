import json
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RESEARCH = ROOT / "research" / "2026-09-07-places"


def load(path, default):
    if not path.exists():
        return default
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def by_id(folder):
    return {p.stem: load(p, {}) for p in sorted(folder.glob("*.json"))} if folder.exists() else {}


def unique(values):
    result, seen = [], set()
    for value in values:
        marker = json.dumps(value, ensure_ascii=False, sort_keys=True) if isinstance(value, (dict, list)) else value
        if marker not in seen:
            seen.add(marker)
            result.append(value)
    return result


def photo_url(photo):
    return photo.get("url") or photo.get("file")


def photo_record(photo, local=False):
    if local:
        return dict(photo, url=photo.get("file"), license_verdict="USABLE", http_status=200)
    return dict(photo)


def year_key(item):
    year = item.get("year_ce")
    return (0, year) if isinstance(year, (int, float)) else (1, 0)


def date_key(item):
    try:
        return datetime.fromisoformat(str(item.get("date"))).date()
    except (TypeError, ValueError):
        return datetime.min.date()


def main():
    library = load(DATA / "library.json", {}).get("records", [])
    targets = [x for x in library if x.get("type") == "place" or x.get("category") == "tradition"]
    out1, out2, out3 = by_id(RESEARCH / "out"), by_id(RESEARCH / "out2"), by_id(RESEARCH / "out3")
    local = load(DATA / "photos-local.json", [])
    local_by_id = {}
    for photo in local:
        local_by_id.setdefault(photo.get("place_id"), []).append(photo_record(photo, True))

    records, queue_rows, geo_missing = [], [], []
    for lib in targets:
        ident = lib.get("id")
        r1, r2, r3 = out1.get(ident, {}), out2.get(ident, {}), out3.get(ident, {})
        geo = r1.get("geo")
        if not isinstance(geo, dict) or geo.get("lat") is None:
            geo = None
            address = r1.get("address") or {}
            geo_missing.append((lib.get("name_th", ident), address.get("line_th") or "ไม่ทราบที่อยู่"))

        history = r1.get("history") or []
        timeline = sorted(r2.get("timeline") or [], key=year_key)
        news = sorted(r2.get("news") or [], key=date_key, reverse=True)
        photos = {"usable": [], "needs_permission": [], "broken": []}
        seen_photo_urls = set()

        def add_photo(photo, bucket):
            url = photo_url(photo)
            if not url or url in seen_photo_urls:
                return
            seen_photo_urls.add(url)
            status = photo.get("http_status")
            if status is not None and status != 200:
                photos["broken"].append(photo)
            else:
                photos[bucket].append(photo)

        for photo in local_by_id.get(ident, []):
            add_photo(photo, "usable")
        for photo in (r2.get("photos_archive") or []) + (r2.get("photos_current") or []):
            add_photo(photo, "needs_permission")
            if url := photo_url(photo):
                queue_rows.append((lib.get("name_th", ident), photo, "รอบ 2 · ต้องขออนุญาตก่อนใช้"))
        for photo in r3.get("photos") or []:
            verdict = str(photo.get("license_verdict", "")).upper()
            bucket = "usable" if verdict == "USABLE" else "needs_permission"
            add_photo(photo, bucket)
            if bucket == "needs_permission":
                queue_rows.append((lib.get("name_th", ident), photo, "รอบ 3 · ยังไม่อนุญาตให้ใช้"))

        statuses = [x.get("status") for x in history + timeline]
        counts = {s.lower(): statuses.count(s) for s in ("CONFIRMED", "UNVERIFIED", "DISPUTED")}
        sources = unique((r1.get("sources") or []) + (r2.get("sources") or []) + (r3.get("sources") or []))
        record = {
            "id": ident, "type": lib.get("type"), "category": lib.get("category"),
            "name_th": lib.get("name_th"), "name_en": lib.get("name_en"),
            "editorial_angle": lib.get("editorial_angle"),
            "illustration": f"/assets/{ident}.webp",
            "brochure_facts": lib.get("facts_paraphrased") or [], "geo": geo,
            "address": r1.get("address"), "contact": r1.get("contact"), "visit": r1.get("visit"),
            "getting_there": r1.get("getting_there") or [], "highlights": r1.get("highlights") or [],
            "nearby": r1.get("nearby") or [], "festival": r1.get("festival"), "history": history,
            "eras": {"then": r2.get("era_then"), "before": r2.get("era_before"), "now": r2.get("era_now")},
            "timeline": timeline, "news": news, "did_you_know": r2.get("did_you_know") or [],
            "photos": photos,
            "seo": {"keywords_th": r1.get("seo_keywords_th") or [], "keywords_en": r1.get("seo_keywords_en") or []},
            "unknowns": unique((r1.get("unknowns") or []) + (r2.get("unknowns") or [])),
            "sources": sources, "counts": counts,
        }
        records.append(record)

    (DATA / "places-enriched.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    queue_lines = ["# คิวขออนุญาตใช้ภาพ", "", "| สถานที่ | หน้าที่พบภาพ | เจ้าของ/เครดิต | สัญญาอนุญาตที่ระบุ | หมายเหตุ |", "|---|---|---|---|---|"]
    for name, photo, note in sorted(queue_rows, key=lambda x: (x[0], photo_url(x[1]) or "")):
        queue_lines.append("| {} | [{}]({}) | {} | {} | {} |".format(name, photo.get("page_url") or photo_url(photo), photo.get("page_url") or photo_url(photo), photo.get("credit") or "ไม่ระบุ", photo.get("license_note_th") or photo.get("license_verdict") or "ไม่ระบุ", note))
    (DATA / "photo-permission-queue.md").write_text("\n".join(queue_lines) + "\n", encoding="utf-8")

    geo_lines = ["# สถานที่ที่ยังไม่มีพิกัด", "", "| สถานที่ | ที่อยู่เท่าที่รู้ |", "|---|---|"]
    geo_lines += [f"| {name} | {address} |" for name, address in sorted(geo_missing)]
    (DATA / "geo-missing.md").write_text("\n".join(geo_lines) + "\n", encoding="utf-8")

    qa = ["# รายงาน QA การรวมข้อมูล", "", "| สถานที่ | พิกัด | เวลาเปิด | ประวัติ | CONFIRMED | ไทม์ไลน์ | ข่าว | ภาพ usable/ask | unknowns |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for x in records:
        qa.append(f"| {x['name_th']} | {'Y' if x['geo'] else '-'} | {'Y' if (x['visit'] or {}).get('opening_hours_th') else '-'} | {len(x['history'])} | {x['counts']['confirmed']} | {len(x['timeline'])} | {len(x['news'])} | {len(x['photos']['usable'])}/{len(x['photos']['needs_permission'])} | {len(x['unknowns'])} |")
    qa += ["", f"สรุปรวม: {len(records)} สถานที่ · พิกัด {sum(bool(x['geo']) for x in records)} · usable {sum(len(x['photos']['usable']) for x in records)} · timeline {sum(len(x['timeline']) for x in records)}"]
    qa += ["", "ผลตรวจคำสั่ง:", "```", "รันหลังสร้างไฟล์จริงด้านล่าง", "```"]
    qa_dir = ROOT / "qa" / "2026-09-07-merge"
    qa_dir.mkdir(parents=True, exist_ok=True)
    (qa_dir / "report.md").write_text("\n".join(qa) + "\n", encoding="utf-8")
    print(f"merged {len(records)} records")


if __name__ == "__main__":
    main()
