import urllib.request
import re
import sys

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def inspect_course(slug, label):
    url = f"https://www.alloschool.com/course/{slug}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    html = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
    sections = re.findall(r'<li id="sections-(\d+)"[^>]*>[\s\S]*?<h2>([\s\S]*?)</h2>', html)
    print(f"\n=== {label} ({slug}) : {len(sections)} sections ===")
    res = []
    for sec_id, sec_title in sections:
        clean_title = re.sub(r'\s+', ' ', sec_title).strip()
        print(f"  [{sec_id}] {clean_title}")
        res.append((int(sec_id), clean_title))
    return res

pc_secs = inspect_course("physique-et-chimie-2eme-bac-sciences-physiques-biof", "PHYSIQUE-CHIMIE BIOF")
m_secs = inspect_course("mathematiques-2eme-bac-sciences-physiques-biof", "MATHEMATIQUES BIOF")
svt_secs = inspect_course("sciences-de-la-vie-et-de-la-terre-svt-2eme-bac-sciences-physiques-biof", "SVT BIOF")
