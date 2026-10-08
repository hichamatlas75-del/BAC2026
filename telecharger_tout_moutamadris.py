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
INVENTORY_FILE = os.path.join(BASE_DIR, "moutamadris_inventory.json")
CATALOGUE_FILE = os.path.join(PDF_DIR, "catalogue_moutamadris.json")

def sanitize_filename(name):
    # Unquote URL encoding first
    unquoted = urllib.parse.unquote(name)
    # Remove filesystem prohibited chars
    clean = re.sub(r'[\\/*?:"<>|]', '', unquoted)
    clean = clean.strip()
    if not clean.lower().endswith('.pdf'):
        clean += '.pdf'
    return clean

def humanize_title(filename):
    name = urllib.parse.unquote(filename)
    name = re.sub(r'\.pdf$', '', name, flags=re.I)
    name = name.replace('-', ' ').replace('_', ' ')
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def download_one(item):
    url = item['url']
    matiere = item['matiere']
    cat = item['categorie']
    raw_fn = item['filename']
    clean_fn = sanitize_filename(raw_fn)

    target_dir = os.path.join(PDF_DIR, matiere, cat)
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, clean_fn)
    rel_path = os.path.join("pdf", matiere, cat, clean_fn).replace('\\', '/')

    title = humanize_title(clean_fn)

    # Check if already downloaded and valid
    if os.path.exists(target_path) and os.path.getsize(target_path) > 1000:
        return {
            "status": "exists",
            "matiere": matiere,
            "categorie": cat,
            "titre": title,
            "fichier": rel_path,
            "taille_ko": os.path.getsize(target_path) // 1024,
            "url": url
        }

    # Download with retries
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = resp.read()
                if len(data) > 500 and data.startswith(b'%PDF'):
                    with open(target_path, 'wb') as f:
                        f.write(data)
                    return {
                        "status": "downloaded",
                        "matiere": matiere,
                        "categorie": cat,
                        "titre": title,
                        "fichier": rel_path,
                        "taille_ko": len(data) // 1024,
                        "url": url
                    }
                elif len(data) > 500:
                    # Sometimes PDF header has leading bytes
                    pdf_idx = data.find(b'%PDF')
                    if pdf_idx != -1:
                        with open(target_path, 'wb') as f:
                            f.write(data[pdf_idx:])
                        return {
                            "status": "downloaded",
                            "matiere": matiere,
                            "categorie": cat,
                            "titre": title,
                            "fichier": rel_path,
                            "taille_ko": len(data[pdf_idx:]) // 1024,
                            "url": url
                        }
        except Exception as e:
            time.sleep(1)

    return {
        "status": "error",
        "matiere": matiere,
        "categorie": cat,
        "titre": title,
        "fichier": rel_path,
        "taille_ko": 0,
        "url": url
    }

def main():
    print("=" * 75)
    print("TÉLÉCHARGEMENT & CLASSEMENT INTÉGRAL DES COURS ET RESSOURCES MOUTAMADRIS.MA")
    print("Matières : Mathématiques, Physique-Chimie, SVT, Anglais, Philosophie")
    print(f"Destination : {PDF_DIR}")
    print("=" * 75)

    if not os.path.exists(INVENTORY_FILE):
        print(f"Erreur: Inventaire introuvable: {INVENTORY_FILE}")
        return

    with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
        items = json.load(f)

    print(f"Total fichiers à traiter : {len(items)}")

    results = []
    downloaded_cnt = 0
    exists_cnt = 0
    error_cnt = 0
    total_size_ko = 0

    # 10 workers for fast and safe concurrent download
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(download_one, item): item for item in items}
        done_count = 0
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            done_count += 1
            st = res["status"]
            if st == "downloaded":
                downloaded_cnt += 1
                total_size_ko += res["taille_ko"]
            elif st == "exists":
                exists_cnt += 1
                total_size_ko += res["taille_ko"]
            else:
                error_cnt += 1

            if done_count % 25 == 0 or done_count == len(items):
                print(f"Progression: {done_count}/{len(items)} (Nouveaux: {downloaded_cnt}, Déjà là: {exists_cnt}, Erreurs: {error_cnt})")

    # Filter successful downloads for the final catalog
    valid_catalog = [r for r in results if r["status"] in ("downloaded", "exists")]

    # Sort catalogue by matiere, categorie, titre
    valid_catalog.sort(key=lambda x: (x["matiere"], x["categorie"], x["titre"]))

    with open(CATALOGUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(valid_catalog, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 75)
    print(f"SUCCÈS : {len(valid_catalog)} fichiers PDF classés et vérifiés !")
    print(f"Volume total : {total_size_ko // 1024} Mo ({total_size_ko} Ko)")
    print(f"Catalogue JSON généré : {CATALOGUE_FILE}")
    print("=" * 75)

if __name__ == '__main__':
    main()
