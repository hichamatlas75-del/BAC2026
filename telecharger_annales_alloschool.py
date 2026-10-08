import os
import sys
import re
import urllib.request
import urllib.parse
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

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

SECTIONS = [
    {
        "matiere": "physique_chimie",
        "prefix": "PC",
        "nom": "Physique-Chimie (SPC)",
        "url": "https://www.alloschool.com/section/4586"
    },
    {
        "matiere": "mathematiques",
        "prefix": "Maths",
        "nom": "Mathématiques (Sciences)",
        "url": "https://www.alloschool.com/section/5321"
    },
    {
        "matiere": "svt",
        "prefix": "SVT",
        "nom": "SVT (Sciences Physiques)",
        "url": "https://www.alloschool.com/section/5192"
    },
    {
        "matiere": "anglais",
        "prefix": "Anglais",
        "nom": "Anglais (Sciences)",
        "url": "https://www.alloschool.com/section/2229"
    },
    {
        "matiere": "philosophie",
        "prefix": "Philo",
        "nom": "Philosophie (Sciences)",
        "url": "https://www.alloschool.com/section/1089"
    }
]

def parse_metadata(raw_title, matiere, prefix):
    # Reading comprehension methods in English
    if "reading comprehension" in raw_title.lower() or "methods for answering" in raw_title.lower():
        part_m = re.search(r'part\s*(\d+)', raw_title, re.I)
        part = part_m.group(1) if part_m else "1"
        filename = f"{prefix}_Methodes_Reading_Part_{part}.pdf"
        human_title = f"{prefix} – Méthodes Reading Comprehension (Partie {part})"
        return "2020", "Normale", "Methode", filename, human_title

    # Preparation series in Maths
    if "série" in raw_title.lower() or "serie" in raw_title.lower():
        s_m = re.search(r's[ée]rie\s*(?:d\'exercices\s*)?(\d+)', raw_title, re.I)
        num = s_m.group(1) if s_m else "1"
        is_corr = any(k in raw_title.lower() for k in ['corrigé', 'corrige', 'correction', 'تصحيح', 'عناصر'])
        t_type = "Corrige" if is_corr else "Sujet"
        year_m = re.search(r'\b(20[0-2][0-9])\b', raw_title)
        year = year_m.group(1) if year_m else "2020"
        filename = f"{prefix}_National_{year}_Prep_Serie_{num}_{t_type}.pdf"
        human_title = f"{prefix} National {year} – Préparation Série {num} ({'Corrigé' if is_corr else 'Sujet'})"
        return year, "Normale", t_type, filename, human_title

    # Year
    year_m = re.search(r'\b(20[0-2][0-9])\b', raw_title)
    year = year_m.group(1) if year_m else ""

    # Session
    if any(k in raw_title.lower() for k in ['rattrapage', 'rattrap', 'إستدراكية', 'استدراكية']):
        session = "Rattrapage"
    else:
        session = "Normale"

    # Type
    if any(k in raw_title.lower() for k in ['corrigé', 'corrige', 'correction', 'تصحيح', 'عناصر الإجابة', 'عناصر الاجابة', 'answers', 'answer']):
        doc_type = "Corrige"
    else:
        doc_type = "Sujet"

    suffix = "_AR" if matiere == "philosophie" else ""
    if year:
        filename = f"{prefix}_National_{year}_{session}_{doc_type}{suffix}.pdf"
        human_title = f"{prefix} National {year} – Session {session} ({'Corrigé Officiel' if doc_type == 'Corrige' else 'Sujet'})"
    else:
        clean = re.sub(r'[^\w\s-]', '', raw_title).strip().replace(' ', '_')
        filename = f"{prefix}_{clean[:40]}.pdf"
        human_title = raw_title

    return year, session, doc_type, filename, human_title

def fetch_section_elements(sec_cfg):
    url = sec_cfg["url"]
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        html = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', 'ignore')
    except Exception as e:
        print(f"   [!] Erreur chargement section {url}: {e}")
        return []

    elements = []
    seen_ids = set()
    for m in re.finditer(r'<a\s+[^>]*href=[\'"](?:https?://www\.alloschool\.com)?/element/(\d+)[^\'"]*[\'"][^>]*>(.*?)</a>', html, re.DOTALL | re.I):
        eid = m.group(1)
        raw_text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if not raw_text or len(raw_text) < 3 or eid in seen_ids:
            continue
        seen_ids.add(eid)

        year, session, doc_type, filename, human_title = parse_metadata(raw_text, sec_cfg["matiere"], sec_cfg["prefix"])

        elements.append({
            "id": eid,
            "raw_title": raw_text,
            "matiere": sec_cfg["matiere"],
            "prefix": sec_cfg["prefix"],
            "year": year,
            "session": session,
            "doc_type": doc_type,
            "filename": filename,
            "human_title": human_title
        })
    return elements

def resolve_and_download(item):
    eid = item["id"]
    matiere = item["matiere"]
    filename = item["filename"]

    dest_dir = os.path.join(PDF_DIR, matiere, "national")
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, filename)
    rel_path = f"pdf/{matiere}/national/{filename}"

    # Check if file already exists with good size
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 2000:
        return {
            "status": "exists",
            "matiere": matiere,
            "categorie": "national",
            "titre": item["human_title"],
            "fichier": rel_path,
            "taille_ko": os.path.getsize(dest_path) // 1024,
            "year": item["year"],
            "session": item["session"],
            "doc_type": item["doc_type"]
        }

    # Resolve direct PDF URL
    elem_url = f"https://www.alloschool.com/element/{eid}"
    direct_url = None
    try:
        req = urllib.request.Request(elem_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', 'ignore')
            pdfs = re.findall(r'href=[\'"](https?://www\.alloschool\.com(?:/index\.ph%70)?/assets/documents/[^\'"]+\.pdf[^\'"]*)[\'"]', html, re.I)
            if pdfs:
                direct_url = pdfs[0].replace("/index.ph%70/", "/").replace("/index.php/", "/")
    except Exception:
        pass

    if not direct_url:
        direct_url = f"https://www.alloschool.com/element/{eid}/pdf"

    # Download
    for attempt in range(3):
        try:
            pdf_req = urllib.request.Request(direct_url, headers=HEADERS)
            with urllib.request.urlopen(pdf_req, timeout=25) as resp:
                data = resp.read()
                if len(data) > 1000 and (data.startswith(b'%PDF') or b'%PDF' in data[:1024]):
                    pdf_start = data.find(b'%PDF')
                    final_data = data[pdf_start:] if pdf_start > 0 else data
                    with open(dest_path, 'wb') as f:
                        f.write(final_data)
                    return {
                        "status": "downloaded",
                        "matiere": matiere,
                        "categorie": "national",
                        "titre": item["human_title"],
                        "fichier": rel_path,
                        "taille_ko": len(final_data) // 1024,
                        "year": item["year"],
                        "session": item["session"],
                        "doc_type": item["doc_type"]
                    }
        except Exception:
            time.sleep(1)

    return {
        "status": "error",
        "matiere": matiere,
        "categorie": "national",
        "titre": item["human_title"],
        "fichier": rel_path,
        "taille_ko": 0,
        "year": item["year"],
        "session": item["session"],
        "doc_type": item["doc_type"]
    }

def main():
    print("=" * 75)
    print("TÉLÉCHARGEMENT OFFICIEL DES ANNALES DU BACCALAURÉAT (2008 À 2024)")
    print("AlloSchool : Physique-Chimie, Maths, SVT, Anglais, Philosophie")
    print(f"Destination : {PDF_DIR}")
    print("=" * 75)

    all_elements = []
    for sec in SECTIONS:
        items = fetch_section_elements(sec)
        print(f"[{sec['nom']}] -> {len(items)} sujets et corrigés identifiés")
        all_elements.extend(items)

    print(f"\nTotal épreuves identifiées : {len(all_elements)}")

    results = []
    downloaded_cnt = 0
    exists_cnt = 0
    error_cnt = 0
    total_size_ko = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(resolve_and_download, it): it for it in all_elements}
        done = 0
        for fut in as_completed(futures):
            res = fut.result()
            results.append(res)
            done += 1
            if res["status"] == "downloaded":
                downloaded_cnt += 1
                total_size_ko += res["taille_ko"]
            elif res["status"] == "exists":
                exists_cnt += 1
                total_size_ko += res["taille_ko"]
            else:
                error_cnt += 1

            if done % 25 == 0 or done == len(all_elements):
                print(f"Progression: {done}/{len(all_elements)} (Nouveaux: {downloaded_cnt}, Déjà présents: {exists_cnt}, Erreurs: {error_cnt})")

    # Deduplicate by unique relative file path
    unique_map = {}
    for r in results:
        if r["status"] in ("downloaded", "exists"):
            fpath = r["fichier"]
            if fpath not in unique_map or unique_map[fpath]["taille_ko"] < r["taille_ko"]:
                unique_map[fpath] = r

    valid_annales = list(unique_map.values())
    valid_annales.sort(key=lambda x: (x["matiere"], -int(x.get("year", 0) if x.get("year", "").isdigit() else 0), x["titre"]))

    annales_json = os.path.join(PDF_DIR, "catalogue_annales.json")
    with open(annales_json, "w", encoding="utf-8") as f:
        json.dump(valid_annales, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 75)
    print(f"SUCCÈS ANNALES : {len(valid_annales)} examens nationaux uniques vérifiés et classés !")
    print(f"Volume téléchargé/vérifié : {total_size_ko // 1024} Mo")
    print(f"Catalogue des annales généré : {annales_json}")
    print("=" * 75)

if __name__ == '__main__':
    main()
