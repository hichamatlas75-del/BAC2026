import os
import sys
import urllib.request
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

# Liste d'exemples d'annales et devoirs surveillés (Option BIOF) à télécharger automatiquement
DEVOIRS_TO_DOWNLOAD = [
    {
        "url": "https://moutamadris.ma/wp-content/uploads/2022/05/devoir-1-Physique-et-Chimie-2eme-BAC-Sciences-Physiques-1er-semestre-sections-internationales-option-francais-modele-1.pdf",
        "dest": os.path.join(PDF_DIR, "physique_chimie", "devoirs", "PC_Devoir1_S1_Modele1.pdf"),
        "titre": "Devoir 1 PC S1 (Modèle 1)"
    },
    {
        "url": "https://moutamadris.ma/wp-content/uploads/2022/05/devoir-1-maths-2bac-sciences-physiques-BIOF-1er-semestre-modele-1.pdf",
        "dest": os.path.join(PDF_DIR, "mathematiques", "devoirs", "Maths_Devoir1_S1_Modele1.pdf"),
        "titre": "Devoir 1 Maths S1 (Modèle 1)"
    },
    {
        "url": "https://moutamadris.ma/wp-content/uploads/2022/05/devoir-1-Sciences-de-la-Vie-et-de-la-Terre-2bac-sciences-physiques-BIOF-1er-semestre-modele-1.pdf",
        "dest": os.path.join(PDF_DIR, "svt", "national", "SVT_Devoir1_S1_Modele1.pdf"),
        "titre": "Devoir 1 SVT S1 (Modèle 1)"
    }
]

def download_file(item):
    url = item["url"]
    dest = item["dest"]
    titre = item["titre"]
    
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print(f"[OK] Déjà présent : {titre} -> {os.path.basename(dest)}")
        return True

    print(f"[*] Téléchargement en cours : {titre}...")
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read()
            if len(content) > 500:
                with open(dest, 'wb') as f:
                    f.write(content)
                print(f"   [+] Succès ! ({len(content) // 1024} Ko enregistrés)")
                return True
            else:
                print(f"   [-] Fichier trop petit ou indisponible.")
    except Exception as e:
        print(f"   [!] Échec du téléchargement pour {titre} ({e})")
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("TELECHARGEUR D'ANNALES ET DEVOIRS (2BAC MAROC 2026)")
    print(f"Dossier de destination : {PDF_DIR}")
    print("=" * 60)
    
    success_count = 0
    for item in DEVOIRS_TO_DOWNLOAD:
        if download_file(item):
            success_count += 1
        time.sleep(0.5)
        
    print("=" * 60)
    print(f"Terminé : {success_count}/{len(DEVOIRS_TO_DOWNLOAD)} fichiers prêts dans le dossier 'pdf/' !")
    print("Vous pouvez ajouter vos propres fichiers PDF dans le dossier 'pdf/' à tout moment.")
    print("=" * 60)
