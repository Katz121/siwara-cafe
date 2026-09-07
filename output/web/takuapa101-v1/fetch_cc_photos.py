"""
fetch_cc_photos.py
Fetch Creative Commons photos from places-enriched.json, optimize to WebP,
and record metadata in data/photos-cc-manifest.json.
"""
import io
import json
from pathlib import Path
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from PIL import Image

# Ensure stdout uses UTF-8 encoding
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

USER_AGENT = "takuapa101-site/1.0 (contact: siwaracafe.com)"
MAX_RETRIES_429 = 3
RETRY_DELAY_429 = 5.0  # seconds
FULL_MAX_WIDTH = 1600
THUMB_MAX_WIDTH = 640
WEBP_QUALITY = 85


def download_photo(
    url: str,
    user_agent: str = USER_AGENT,
    max_retries: int = MAX_RETRIES_429,
    retry_delay: float = RETRY_DELAY_429,
) -> bytes:
    """
    Downloads image data from url sequentially using urllib.
    Retries on HTTP 429 up to max_retries times with retry_delay seconds wait.
    """
    headers = {"User-Agent": user_agent}
    req = urllib.request.Request(url, headers=headers)

    attempts = 0
    while True:
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read()
        except urllib.error.HTTPError as err:
            if err.code == 429 and attempts < max_retries:
                attempts += 1
                print(
                    f"    [HTTP 429] ติด Rate Limit: รอ {retry_delay} วินาทีก่อนลองใหม่ "
                    f"(ครั้งที่ {attempts}/{max_retries})..."
                )
                time.sleep(retry_delay)
                continue
            raise


def resize_and_save_webp(
    image_bytes: bytes, full_path: Path, thumb_path: Path
) -> tuple[int, int]:
    """
    Converts image to WebP format:
    - Full image: max width 1600px, aspect ratio preserved
    - Thumb image: max width 640px, aspect ratio preserved
    Returns (full_width, full_height).
    """
    with Image.open(io.BytesIO(image_bytes)) as img:
        # Convert color mode for WebP compatibility
        if img.mode in ("RGBA", "LA") or (
            img.mode == "P" and "transparency" in img.info
        ):
            img = img.convert("RGBA")
        else:
            img = img.convert("RGB")

        orig_w, orig_h = img.size

        # 1. Full size (max width 1600px, maintain aspect ratio)
        if orig_w > FULL_MAX_WIDTH:
            ratio = FULL_MAX_WIDTH / orig_w
            full_w = FULL_MAX_WIDTH
            full_h = max(1, round(orig_h * ratio))
            full_img = img.resize((full_w, full_h), Image.Resampling.LANCZOS)
        else:
            full_w, full_h = orig_w, orig_h
            full_img = img.copy()

        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_img.save(full_path, format="WEBP", quality=WEBP_QUALITY)

        # 2. Thumbnail (max width 640px, maintain aspect ratio)
        if orig_w > THUMB_MAX_WIDTH:
            ratio_thumb = THUMB_MAX_WIDTH / orig_w
            thumb_w = THUMB_MAX_WIDTH
            thumb_h = max(1, round(orig_h * ratio_thumb))
            thumb_img = img.resize(
                (thumb_w, thumb_h), Image.Resampling.LANCZOS
            )
        else:
            thumb_img = img.copy()

        thumb_path.parent.mkdir(parents=True, exist_ok=True)
        thumb_img.save(thumb_path, format="WEBP", quality=WEBP_QUALITY)

        return full_w, full_h


def main():
    base_dir = Path(__file__).resolve().parent
    data_file = base_dir / "data" / "places-enriched.json"
    assets_cc_dir = base_dir / "site" / "assets" / "photos" / "cc"
    manifest_file = base_dir / "data" / "photos-cc-manifest.json"

    if not data_file.exists():
        print(f"Error: ไม่พบไฟล์ {data_file}")
        sys.exit(1)

    print(f"กำลังอ่านข้อมูลจาก {data_file}...")
    with open(data_file, "r", encoding="utf-8") as f:
        places = json.load(f)

    # Extract CC photos that start with http
    # Numbering n per place_id starting from 1
    tasks = []
    for place in places:
        place_id = place.get("id") or place.get("place_id")
        usable_photos = place.get("photos", {}).get("usable", [])
        place_http_count = 0
        for photo in usable_photos:
            url = photo.get("url", "")
            if url.startswith("http"):
                place_http_count += 1
                tasks.append(
                    {
                        "place_id": place_id,
                        "n": place_http_count,
                        "photo": photo,
                    }
                )

    print(
        f"พบภาพ CC ที่ต้องดาวน์โหลดทั้งหมด {len(tasks)} ใบ จาก {len(places)} สถานที่\n"
    )

    manifest = []
    success_count = 0
    failed_count = 0

    for i, task in enumerate(tasks, 1):
        place_id = task["place_id"]
        n = task["n"]
        photo = task["photo"]
        url = photo.get("url")

        local_rel_file = f"/assets/photos/cc/{place_id}-{n}.webp"
        thumb_rel_file = f"/assets/photos/cc/{place_id}-{n}-640.webp"
        local_full_path = assets_cc_dir / f"{place_id}-{n}.webp"
        local_thumb_path = assets_cc_dir / f"{place_id}-{n}-640.webp"

        manifest_entry = {
            "place_id": place_id,
            "original_url": url,
            "page_url": photo.get("page_url", ""),
            "local_file": local_rel_file,
            "thumb_file": thumb_rel_file,
            "license": photo.get("license", ""),
            "attribution_th": photo.get("attribution_th", ""),
            "caption_th": photo.get("caption_th", ""),
            "era": photo.get("era", ""),
            "width": None,
            "height": None,
            "status": "pending",
        }

        print(f"[{i}/{len(tasks)}] ดาวน์โหลด: {place_id} (รูปที่ {n}) -> {url}")

        try:
            img_bytes = download_photo(url)
            full_w, full_h = resize_and_save_webp(
                img_bytes, local_full_path, local_thumb_path
            )

            manifest_entry["width"] = full_w
            manifest_entry["height"] = full_h
            manifest_entry["status"] = "ok"
            success_count += 1
            print(
                f"    [สำเร็จ] บันทึก: {local_full_path.name} ({full_w}x{full_h}) และ {local_thumb_path.name}"
            )
        except Exception as e:
            err_msg = str(e)
            manifest_entry["status"] = "failed"
            manifest_entry["reason"] = err_msg
            manifest_entry["error"] = err_msg
            failed_count += 1
            print(f"    [ล้มเหลว] {err_msg}")

        manifest.append(manifest_entry)
        time.sleep(1.0)

    print("\n" + "=" * 60)
    print(f"บันทึก manifest ไปยัง {manifest_file}...")
    manifest_file.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(
        f"ผลการทำงาน: สำเร็จ {success_count} ใบ, ล้มเหลว {failed_count} ใบ (รวมทั้งหมด {len(manifest)} ใบ)"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()
