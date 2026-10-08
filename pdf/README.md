# 📂 Base de Données Intégrale de PDF (2BAC Maroc 2026 / 2027)

Ce dossier rassemble **plus de 625 fichiers PDF officiels et pédagogiques** (annales nationales complètes 2008 à 2024 avec corrigés officiels, cours complets, fiches résumés, séries d'exercices et devoirs surveillés) issus des programmes officiels, de **Moutamadris.ma** et de **AlloSchool** pour la filière **Sciences Physiques (Option Français / BIOF & Général)**.

Tous ces documents sont utilisables **100% hors-ligne**, directement consultables dans votre navigateur ou convertibles instantanément en **QCM IA interactifs** dans l'application PWA.

---

## 🗂️ Arborescence & Organisation par Matière et par Leçon

```text
pdf/
├── catalogue_global_complet.json    # Catalogue consolidé complet des 625+ documents PDF
├── catalogue_moutamadris.json       # Catalogue des cours, résumés et exercices Moutamadris.ma
├── catalogue_annales.json           # Catalogue des 277 épreuves et corrigés nationaux AlloSchool (2008-2024)
│
├── mathematiques/                   # 194 documents PDF (BIOF Français)
│   ├── cours/                       # Limites, Continuité, Dérivation, Logarithme (ln), Exponentielle, Complexes, Calcul Intégral, Probabilités
│   ├── resumes/                     # 93 fiches de synthèse de formules et méthodes par notion
│   ├── devoirs/                     # Devoirs surveillés semestriels modèles
│   └── national/                    # 64 annales nationales officielles 2008-2024 (Sujets + Corrigés officiels) + séries de préparation
│
├── anglais/                         # 157 documents PDF (Anglais Bac National)
│   ├── cours/                       # 55 cours : Units 1-10, Grammar Guides, Irregular Verbs, Writing Packs
│   ├── resumes/                     # 14 fiches de synthèse : Writing samples, Connectors, Reviews
│   ├── exercices/                   # 23 séries d'exercices et quizzes ciblés
│   └── national/                    # 65 annales nationales officielles 2008-2024 (Sujets + Corrigés détaillés) + méthodes de compréhension
│
├── physique_chimie/                 # 124 documents PDF (BIOF Français)
│   ├── cours/                       # 42 cours complets : Ondes mécaniques/lumineuses, Décroissance radioactive, Noyaux/Masse/Énergie, RC/RL/RLC, Mécanique de Newton, Acide-Base, Électrolyse
│   ├── resumes/                     # 9 fiches de résumés de lois physiques et chimiques
│   ├── exercices/                   # 12 séries d'exercices d'entraînement par leçon
│   ├── devoirs/                     # Devoirs surveillés types
│   └── national/                    # 60 annales nationales officielles 2008-2024 (Sujets + Corrigés officiels Normale et Rattrapage)
│
├── svt/                             # 86 documents PDF (BIOF Français)
│   ├── cours/                       # 35 cours : Consommation de matière organique et libération d'énergie (ATP), Génétique humaine et moléculaire, Immunologie, Géologie, Pollution
│   ├── exercices/                   # Séries d'exercices d'application scientifique
│   └── national/                    # 47 annales nationales officielles 2016-2024 (Sujets + Corrigés officiels Normale et Rattrapage)
│
├── philosophie/                     # 64 documents PDF (باللغة العربية)
│   ├── cours/                       # دروس مجزوءات: الوضع البشري، المعرفة، السياسة، الأخلاق، منهجيات القولة والنص والسؤال
│   └── national/                    # 60 امتحاناً وطنياً رسمياً موحداً من 2009 إلى 2024 (المواضيع + عناصر الإجابة والتصحيح الرسمي)
│
├── examens_blancs/                  # Épreuves d'entraînement des lycées d'excellence
└── fiches_resumes/                  # Mémos et tableaux récapitulatifs
```

---

## ⚡ Fonctionnalités PWA Associées

1. **Lecteur PDF Intégré** : Ouverture immédiate en un clic dans n'importe quel navigateur (Chrome, Firefox, Safari, Edge) sans lecteur tiers.
2. **Convertisseur QCM IA** : Chaque cours, exercice ou examen national PDF peut être injecté dans le moteur QCM IA pour générer automatiquement des questions interactives à choix multiples avec correction immédiate.
3. **Mise en Cache Hors-Ligne** : Synchronisé avec le Service Worker PWA (`sw.js`) pour un accès permanent même sans réseau.
4. **Recherche et Filtrage Avancés** : Filtrage dynamique instantané par matière, par catégorie (cours, résumés, exercices, examens nationaux) et par année (2008 à 2024).
