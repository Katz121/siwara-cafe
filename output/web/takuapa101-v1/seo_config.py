from pathlib import Path
import os
from urllib.parse import urlsplit
SITE_BASE_URL = os.getenv('SITE_BASE_URL', 'https://takuapa101.com').rstrip('/')
BASE_PATH = urlsplit(SITE_BASE_URL).path.rstrip('/')
ROOT = Path(__file__).resolve().parent

# Cloudflare Worker that harvests and re-checks city news. Empty disables live top-up.
NEWS_API = os.environ.get('TAKUAPA_NEWS_API', '')
