import os
import sys
import re
import urllib.request
import urllib.parse
import time
import json

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE_DIR, "pdf")

PAGES = [
    {
        "matiere": "physique_chimie",
        "nom": "Physique-Chimie (BIOF)",
        "url": "https://moutamadris.ma/%D8%A7%D9%84%D9%81%D9%8A%D8%B2%D9%8A%D8%A7%D8%A1-%D9%88%D8%A7%D9%84%D9%83%D9%8A%D9%85%D9%8A%D8%A7%D8%A1-%D8%A7%D9%84%D8%AB%D8%A7%D9%86%D9%8A%D8%A9-%D8%A8%D8%A7%D9%83-%D8%B9%D9%84%D9%88%D9%85-%D8%AE/",
        "crawl_subs": False
    },
    {
        "matiere": "svt",
        "nom": "SVT (BIOF)",
        "url": "https://moutamadris.ma/%D8%B9%D9%84%D9%88%D9%85-%D8%A7%D9%84%D8%AD%D9%8A%D8%A7%D8%A9-%D9%88%D8%A7%D9%84%D8%A7%D8%B1%D8%B6-%D8%A7%D9%84%D8%AB%D8%A7%D9%86%D9%8A%D8%A9-%D8%A8%D8%A7%D9%83-%D8%B9%D9%84%D9%88%D9%85-%D9%81%D9%8A/",
        "crawl_subs": False
    },
    {
        "matiere": "mathematiques",
        "nom": "Mathématiques (BIOF)",
        "url": "https://moutamadris.ma/%D8%A7%D9%84%D8%B1%D9%8A%D8%A7%D8%B6%D9%8A%D8%A7%D8%AA-%D8%A7%D9%84%D8%AB%D8%A7%D9%86%D9%8A%D8%A9-%D8%A8%D8%A7%D9%83-%D8%B9%D9%84%D9%88%D9%85-%D8%AE%D9%8A%D8%A7%D8%B1-%D9%81%D8%B1%D9%86%D8%B3%D9%8A/",
        "crawl_subs": False
    },
    {
        "matiere": "anglais",
        "nom": "Anglais (National)",
        "url": "https://moutamadris.ma/%d8%a7%d9%84%d9%84%d8%ba%d8%a9-%d8%a7%d9%84%d8%a7%d9%86%d8%ac%d9%84%d9%8a%d8%b2%d9%8a%d8%a9-%d8%a7%d9%84%d8%ab%d8%a7%d9%86%d9%8a%d8%a9-%d8%a8%d8%a7%d9%83/",
        "crawl_subs": False
    },
    {
        "matiere": "philosophie",
        "nom": "Philosophie (Arabe)",
        "url": "https://moutamadris.ma/%d8%a7%d9%84%d9%81%d9%84%d8%b3%d9%81%d8%a9-%d8%a7%d9%84%d8%ab%d8%a7%d9%86%d9%8a%d8%a9-%d8%a8%d8%a7%d9%83/",
        "crawl_subs": True
    }
]

def fetch_html(url):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode('utf-8', 'ignore')
    except Exception as e:
        print(f"   [!] Erreur fetch {url}: {e}")
        return ""

def sanitize_filename(name):
    clean = re.sub(r'[\\/*?:"<>|]', '', name)
    clean = clean.replace(' ', '_').replace('-', '_')
    clean = re.sub(r'_+', '_', clean).strip('_')
    return clean

def extract_pdfs_from_html(html, page_url):
    found = []
    # Match anchor tags
    for m in re.finditer(r'<a\s+[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>', html, re.DOTALL | re.I):
        href = m.group(1).strip()
        text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        
        # Absolute URL
        full_url = urllib.parse.urljoin(page_url, href)
        
        if full_url.lower().endswith('.pdf'):
            found.append({
                "url": full_url,
                "text": text,
                "filename": os.path.basename(urllib.parse.urlparse(full_url).path)
            })
    return found

def classify_pdf(filename, text, matiere):
    fn = filename.lower()
    tx = text.lower()
    combined = fn + " " + tx

    # Classification par type
    if any(k in combined for k in ['cours', 'lesson', 'درس', 'دروس']):
        cat = "cours"
    elif any(k in combined for k in ['resume', 'résumé', 'summary', 'ملخص']):
        cat = "resumes"
    elif any(k in combined for k in ['exercice', 'exercices', 'exercise', 'تمرین', 'تمارين', 'quiz', 'practice']):
        cat = "exercices"
    elif any(k in combined for k in ['devoir', 'controle', 'contrôle', 'فرض', 'فروض']):
        cat = "devoirs"
    elif any(k in combined for k in ['examen', 'national', 'امتحان']):
        cat = "examens"
    else:
        cat = "cours"

    return cat

print("Phase 1: Exploration des pages et détection de tous les PDFs...")
all_items = []

for cfg in PAGES:
    mat = cfg["matiere"]
    nom = cfg["nom"]
    url = cfg["url"]
    print(f"\nScanning {nom} : {url}")
    html = fetch_html(url)
    
    pdfs = extract_pdfs_from_html(html, url)
    print(f" -> {len(pdfs)} PDFs directs trouvés")

    sub_urls = []
    if cfg["crawl_subs"]:
        # Find subpages
        sub_links = re.findall(r'<a\s+[^>]*href=[\'"]([^\'"]+)[\'"][^>]*>(.*?)</a>', html, re.DOTALL | re.I)
        for href, link_text in sub_links:
            clean_text = re.sub(r'<[^>]+>', '', link_text).strip()
            if 'moutamadris.ma/' in href and not href.endswith('.pdf') and not any(x in href for x in ['notes', 'prof', 'support', 'students', 'category', 'tag']):
                if href != url and href not in sub_urls:
                    sub_urls.append(href)
        print(f" -> {len(sub_urls)} sous-pages détectées pour {mat}")

        for s_url in sub_urls[:15]:
            print(f"    Sub-crawl: {urllib.parse.unquote(s_url).split('/')[-2] if '/' in s_url else s_url}")
            sub_html = fetch_html(s_url)
            sub_pdfs = extract_pdfs_from_html(sub_html, s_url)
            for sp in sub_pdfs:
                if not any(x["url"] == sp["url"] for x in pdfs):
                    pdfs.append(sp)

    print(f" ==> Total pour {nom}: {len(pdfs)} fichiers PDF")
    
    for p in pdfs:
        p["matiere"] = mat
        p["categorie"] = classify_pdf(p["filename"], p["text"], mat)
        all_items.append(p)

print(f"\n==========================================")
print(f"TOTAL GLOBAL: {len(all_items)} PDFs uniques inventoriés !")
print(f"==========================================")

with open(os.path.join(BASE_DIR, "moutamadris_inventory.json"), "w", encoding="utf-8") as f:
    json.dump(all_items, f, ensure_ascii=False, indent=2)

print("Inventaire sauvegardé dans moutamadris_inventory.json")
