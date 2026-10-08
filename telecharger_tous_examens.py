import os
import sys
import urllib.request
import re
import time

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

EXAMS = [
    # PHYSIQUE-CHIMIE (FRANCAIS / BIOF)
    ("physique_chimie", "PC_National_2024_Normale_Sujet_BIOF.pdf", 147672),
    ("physique_chimie", "PC_National_2024_Normale_Corrige_BIOF.pdf", 147675),
    ("physique_chimie", "PC_National_2024_Rattrapage_Sujet_BIOF.pdf", 147678),
    ("physique_chimie", "PC_National_2024_Rattrapage_Corrige_BIOF.pdf", 147681),
    ("physique_chimie", "PC_National_2023_Normale_Sujet_BIOF.pdf", 142388),
    ("physique_chimie", "PC_National_2023_Normale_Corrige_BIOF.pdf", 142393),

    # MATHEMATIQUES (FRANCAIS / BIOF)
    ("mathematiques", "Maths_National_2024_Normale_Sujet_BIOF.pdf", 147782),
    ("mathematiques", "Maths_National_2024_Normale_Corrige_BIOF.pdf", 147787),
    ("mathematiques", "Maths_National_2024_Rattrapage_Sujet_BIOF.pdf", 147792),
    ("mathematiques", "Maths_National_2024_Rattrapage_Corrige_BIOF.pdf", 147797),
    ("mathematiques", "Maths_National_2023_Normale_Sujet_BIOF.pdf", 147757),
    ("mathematiques", "Maths_National_2023_Normale_Corrige_BIOF.pdf", 147762),

    # SVT (FRANCAIS / BIOF)
    ("svt", "SVT_National_2024_Normale_Sujet_BIOF.pdf", 147821),
    ("svt", "SVT_National_2024_Normale_Corrige_BIOF.pdf", 147822),
    ("svt", "SVT_National_2024_Rattrapage_Sujet_BIOF.pdf", 147823),
    ("svt", "SVT_National_2024_Rattrapage_Corrige_BIOF.pdf", 147824),
    ("svt", "SVT_National_2023_Normale_Sujet_BIOF.pdf", 147816),
    ("svt", "SVT_National_2023_Normale_Corrige_BIOF.pdf", 147817),

    # ANGLAIS
    ("anglais", "Anglais_National_2024_Normale_Sujet.pdf", 145934),
    ("anglais", "Anglais_National_2024_Normale_Corrige.pdf", 145945),
    ("anglais", "Anglais_National_2023_Normale_Sujet.pdf", 142510),
    ("anglais", "Anglais_National_2023_Normale_Corrige.pdf", 142521),

    # PHILOSOPHIE (ARABE)
    ("philosophie", "Philo_National_2024_Normale_Sujet_AR.pdf", 146018),
    ("philosophie", "Philo_National_2024_Normale_Corrige_AR.pdf", 146027),
    ("philosophie", "Philo_National_2023_Normale_Sujet_AR.pdf", 142698),
    ("philosophie", "Philo_National_2023_Normale_Corrige_AR.pdf", 142707),
]

def resolve_pdf_url(elem_id):
    url = f"https://www.alloschool.com/element/{elem_id}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        html = urllib.request.urlopen(req, timeout=12).read().decode('utf-8', 'ignore')
        pdfs = re.findall(r'href=[\'"](https?://www\.alloschool\.com/assets/documents/[^\'"]+\.pdf[^\'"]*)[\'"]', html, re.I)
        if pdfs:
            return pdfs[0]
    except Exception as e:
        print(f"   [!] Erreur résolution ID {elem_id}: {e}")
    return None

def download_pdf(direct_url, dest_path, filename):
    req = urllib.request.Request(direct_url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
            if len(data) > 1000:
                with open(dest_path, 'wb') as f:
                    f.write(data)
                print(f"   [+] OK: {filename} ({len(data) // 1024} Ko)")
                return True
    except Exception as e:
        print(f"   [!] Erreur téléchargement {filename}: {e}")
    return False

if __name__ == "__main__":
    print("=" * 70)
    print("TÉLÉCHARGEMENT OFFICIEL DU PACK D'ANNALES (2BAC SCIENCES PHYSIQUES)")
    print("Matières scientifiques en français (BIOF) & Philosophie en arabe")
    print(f"Dossier de stockage : {PDF_DIR}")
    print("=" * 70)

    success = 0
    total = len(EXAMS)

    for subfolder, filename, elem_id in EXAMS:
        dest_dir = os.path.join(PDF_DIR, subfolder, "national")
        os.makedirs(dest_dir, exist_ok=True)
        dest_file = os.path.join(dest_dir, filename)

        if os.path.exists(dest_file) and os.path.getsize(dest_file) > 1000:
            print(f"[Déjà présent] {filename}")
            success += 1
            continue

        print(f"[*] Traitement de {filename} (ID AlloSchool: {elem_id})...")
        pdf_url = resolve_pdf_url(elem_id)
        if pdf_url:
            if download_pdf(pdf_url, dest_file, filename):
                success += 1
        time.sleep(0.4)

    print("=" * 70)
    print(f"RÉSULTAT : {success}/{total} fichiers PDF d'examens nationaux enregistrés !")
    print("=" * 70)
