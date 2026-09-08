import os
from bs4 import BeautifulSoup

paths = [
    r"D:\Siwaracafeweb\output\web\takuapa101-v1\site\en\index.html",
    r"D:\Siwaracafeweb\output\web\takuapa101-v1\site\en\places\tao-ming\index.html",
    r"D:\Siwaracafeweb\output\web\takuapa101-v1\site\en\stories\city\index.html",
    r"D:\Siwaracafeweb\output\web\takuapa101-v1\site\en\rest\index.html",
    r"D:\Siwaracafeweb\output\web\takuapa101-v1\site\en\eat\index.html",
    r"D:\Siwaracafeweb\output\web\takuapa101-v1\site\en\map\index.html",
]

out = ""
for p in paths:
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            # Extract text from main or body
            main = soup.find('main') or soup.find('body')
            text = main.get_text(separator='\n', strip=True) if main else ""
            out += f"--- {p} ---\n{text}\n\n"

with open(r"D:\Siwaracafeweb\output\web\takuapa101-v1\audit\english_pages.txt", 'w', encoding='utf-8') as f:
    f.write(out)

print("Dumped english pages")
