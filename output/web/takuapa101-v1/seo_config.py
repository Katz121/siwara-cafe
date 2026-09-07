from pathlib import Path
import os
from urllib.parse import urlsplit
SITE_BASE_URL = os.getenv('SITE_BASE_URL', 'https://siwaracafe.com/takuapa').rstrip('/')
BASE_PATH = urlsplit(SITE_BASE_URL).path.rstrip('/')
ROOT = Path(__file__).resolve().parent
