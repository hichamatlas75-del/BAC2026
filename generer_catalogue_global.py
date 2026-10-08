import os
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_DIR = os.path.join(BASE_DIR, "pdf")

# Load existing metadata from both catalogues to preserve clean human titles if available
meta_titles = {}

if os.path.exists(os.path.join(PDF_DIR, "catalogue_moutamadris.json")):
    try:
        with open(os.path.join(PDF_DIR, "catalogue_moutamadris.json"), 'r', encoding='utf-8') as f:
            for item in json.load(f):
                fkey = item["fichier"].replace("\\", "/")
                meta_titles[fkey] = item["titre"]
    except Exception:
        pass

if os.path.exists(os.path.join(PDF_DIR, "catalogue_annales.json")):
    try:
        with open(os.path.join(PDF_DIR, "catalogue_annales.json"), 'r', encoding='utf-8') as f:
            for item in json.load(f):
                fkey = item["fichier"].replace("\\", "/")
                meta_titles[fkey] = item["titre"]
    except Exception:
        pass

def generate_title_from_filename(filename, matiere, categorie):
    name_no_ext = os.path.splitext(filename)[0]
    
    # Check if it's an annale / national exam
    if categorie == "national":
        # Format like PC_National_2024_Normale_Sujet.pdf
        m = re.match(r'([A-Za-z]+)_National_(\d{4})_(Normale|Rattrapage)_(Sujet|Corrige)(_AR)?', name_no_ext, re.I)
        if m:
            prefix, year, session, doc_type, is_ar = m.groups()
            badge = "🏛️" if doc_type.lower() == "sujet" else "✅"
            type_fr = "Corrigé Officiel" if doc_type.lower() == "corrige" else "Sujet"
            lang = " (AR)" if is_ar else ""
            return f"{badge} {prefix} National {year} – Session {session} ({type_fr}){lang}"
        
        # Check prep series
        m_prep = re.match(r'([A-Za-z]+)_National_(\d{4})_Prep_Serie_(\d+)_(Sujet|Corrige)', name_no_ext, re.I)
        if m_prep:
            prefix, year, snum, doc_type = m_prep.groups()
            badge = "📝" if doc_type.lower() == "sujet" else "✅"
            type_fr = "Corrigé" if doc_type.lower() == "corrige" else "Sujet"
            return f"{badge} {prefix} National {year} – Préparation Série {snum} ({type_fr})"

        # Check reading methods
        if "Methodes_Reading" in name_no_ext:
            part = re.search(r'Part_(\d+)', name_no_ext)
            p_num = part.group(1) if part else "1"
            return f"🇬🇧 Anglais – Méthodes Reading Comprehension (Partie {p_num})"

    # Moutamadris clean title
    clean = name_no_ext.replace('-', ' ').replace('_', ' ')
    clean = re.sub(r'^(cours|resume|exercise|quiz|lesson)\s+', '', clean, flags=re.I)
    clean = re.sub(r'\s+2bac.*$', '', clean, flags=re.I)
    
    icon = "📖" if categorie == "cours" else ("📝" if categorie == "resumes" else "✍️")
    return f"{icon} {clean.strip().capitalize()}"

all_records = []

for root, dirs, files in os.walk(PDF_DIR):
    for f in sorted(files):
        if not f.lower().endswith(".pdf"):
            continue
        full_path = os.path.join(root, f)
        sz = os.path.getsize(full_path)
        if sz < 1000:
            continue
        
        rel_path = os.path.relpath(full_path, BASE_DIR).replace("\\", "/")
        parts = rel_path.split("/")
        # format: pdf / {matiere} / {categorie} / filename
        if len(parts) >= 4:
            mat = parts[1]
            cat = parts[2]
        elif len(parts) == 3:
            mat = parts[1]
            cat = "cours"
        else:
            mat = "autre"
            cat = "cours"

        titre = meta_titles.get(rel_path)
        if not titre:
            titre = generate_title_from_filename(f, mat, cat)
        else:
            # Add emoji badge if missing
            if cat == "national" and not any(titre.startswith(x) for x in ["🏛️", "✅", "📝"]):
                badge = "✅" if "corrig" in titre.lower() or "corrige" in f.lower() else "🏛️"
                titre = f"{badge} {titre}"
            elif cat == "cours" and not titre.startswith("📖"):
                titre = f"📖 {titre}"
            elif cat == "resumes" and not titre.startswith("📝"):
                titre = f"📝 {titre}"
            elif cat in ("exercices", "devoirs") and not titre.startswith("✍️"):
                titre = f"✍️ {titre}"

        year_m = re.search(r'\b(20[0-2][0-9])\b', f)
        year = year_m.group(1) if year_m else ""

        all_records.append({
            "matiere": mat,
            "categorie": cat,
            "titre": titre,
            "fichier": rel_path,
            "taille_ko": sz // 1024,
            "year": year
        })

print(f"Total fichiers PDF valides répertoriés : {len(all_records)}")

# Write to js/pdf_catalogue.js
js_path = os.path.join(BASE_DIR, "js", "pdf_catalogue.js")
js_content = "// Catalogue complet 100% Hors-Ligne des 620+ PDF (Moutamadris & AlloSchool Annales 2008-2024)\n"
js_content += "window.MOUTAMADRIS_CATALOG = " + json.dumps(all_records, ensure_ascii=False) + ";\n"
js_content += "window.FULL_PDF_CATALOG = window.MOUTAMADRIS_CATALOG;\n"

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Catalogue JavaScript sauvegardé avec succès dans : {js_path} ({len(js_content)} octets)")

# Also write full json catalog for easy reading/tools
with open(os.path.join(PDF_DIR, "catalogue_global_complet.json"), "w", encoding="utf-8") as f:
    json.dump(all_records, f, ensure_ascii=False, indent=2)

print("Catalogue JSON global sauvegardé dans pdf/catalogue_global_complet.json")
