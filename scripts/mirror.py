
import os, re, sys, json, time, hashlib
from urllib.parse import urljoin, urlparse, urldefrag
import httpx
from bs4 import BeautifulSoup

BASE = "https://www.weinbauneumayer.at/"
OUT  = "/data/.hermes/cache/scratch/neumayer-mirror"
HDRS = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"}
os.makedirs(OUT, exist_ok=True)
client = httpx.Client(headers=HDRS, follow_redirects=True, timeout=30)
seen=set(); queue=[BASE]; pages={}; assets=set()
SKIP_EXT = (".zip",".rar",".mp4",".avi",".mov",".webm",".mp3",".pdf",".doc",".docx",".xls",".xlsx",".ppt",".pptx")

def local_path(url):
    p = urlparse(url)
    path = p.path
    if path.endswith("/") or not path:
        path += "index.html"
    if "." not in os.path.basename(path):
        path += "/index.html"
    return os.path.join(OUT, p.netloc, path.lstrip("/"))

def save(url, content):
    fp = local_path(url)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp,"wb") as f: f.write(content)
    return fp

n=0
while queue and n < 120:
    url = queue.pop(0)
    url,_ = urldefrag(url)
    if url in seen: continue
    seen.add(url); n+=1
    try:
        r = client.get(url)
    except Exception as e:
        continue
    ct = r.headers.get("content-type","")
    if "text/html" not in ct:
        assets.add((url, ct))
        save(url, r.content); continue
    html = r.text
    pages[url] = {"status":r.status_code,"len":len(html),"title":""}
    soup = BeautifulSoup(html,"html.parser")
    if soup.title: pages[url]["title"] = soup.title.get_text(strip=True)
    save(url, r.content)
    for tag,attr in (("a","href"),("img","src"),("link","href"),("script","src"),("source","src")):
        for el in soup.find_all(tag):
            v = el.get(attr)
            if not v: continue
            if v.startswith(("mailto:","tel:","javascript:","data:","#")): continue
            full = urljoin(url, v)
            p = urlparse(full)
            if p.netloc not in ("www.weinbauneumayer.at","weinbauneumayer.at"): continue
            if p.path.lower().endswith(SKIP_EXT): continue
            full = full.split("#")[0]
            if full not in seen and full not in queue:
                if any(full.lower().endswith(e) for e in (".png",".jpg",".jpeg",".gif",".webp",".svg",".css",".js",".ico",".woff",".woff2",".ttf",".eot")) or "/wp-content/" in full or "/wp-includes/" in full:
                    assets.add((full,""))
                    try:
                        rr=client.get(full); save(full, rr.content)
                    except Exception: pass
                else:
                    queue.append(full)
    time.sleep(0.15)

json.dump(pages, open(os.path.join(OUT,"_pages.json"),"w"), indent=1, ensure_ascii=False)
print("pages:", len(pages))
for u,v in sorted(pages.items()):
    print(v["status"], v["len"], u, "|", v["title"][:60])
