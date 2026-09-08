"""Shared rendering guard for sources confirmed offline."""
import json
from html import escape
from pathlib import Path

_ROOT = Path(__file__).parent
_DEAD = json.loads((_ROOT / 'data' / 'dead-sources.json').read_text(encoding='utf-8'))

def _norm(url):
    """ถอดรหัส %xx ก่อนเทียบ · URL เดียวกันเขียนได้ทั้งแบบเข้ารหัสและไม่เข้ารหัส"""
    from urllib.parse import unquote
    return unquote(str(url)).rstrip('/')


def is_dead(url):
    if not url:
        return False
    u = _norm(url)
    return any(u.startswith(_norm(item['url_prefix'])) for item in _DEAD)

def source_link(url, label, lang='th'):
    """Render a source as a link, or preserve it as text when confirmed dead."""
    if not url:
        return ''
    label = escape(str(label))
    if is_dead(url):
        note = 'Original source offline · checked 8 Sep 2026' if lang == 'en' else 'แหล่งเดิมออฟไลน์ · ตรวจเมื่อ 8 ก.ย. 2569'
        return f'<span class="source-offline">{label} <small>{escape(note)}</small></span>'
    return f'<a href="{escape(str(url), quote=True)}" target="_blank" rel="noopener">{label}</a>'
