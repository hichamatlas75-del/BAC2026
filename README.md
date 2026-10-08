# 🎓 2BAC Maroc 2026 – Hub de Révision (Sciences Physiques BIOF)

[![PWA Ready](https://img.shields.io/badge/PWA-Ready-10b981.svg)](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps)
[![Curriculum](https://img.shields.io/badge/Programme-Maroc%202026-2563eb.svg)](https://www.alloschool.com)
[![Offline](https://img.shields.io/badge/Mode-100%25%20Hors--Ligne-f59e0b.svg)](#)

Plateforme web progressive (PWA) complète et autonome conçue pour la préparation intensive et la réussite au **Baccalauréat marocain 2026 (2ème BAC Sciences Physiques - Option BIOF)**.

---

## 🌟 Fonctionnalités Clés

* 📖 **Programme Officiel Bilingue (Arabe & Français)** :
  * ⚗️ **Physique-Chimie** (Coeff 7) : Ondes, Nucléaire, Électricité, Mécanique, Cinétique, Équilibres, Piles, Estérification.
  * 📐 **Mathématiques** (Coeff 7) : Analyse, Suites, Logarithmes, Exponentielles, Nombres Complexes, Intégrales, Probabilités.
  * 🧬 **SVT** (Coeff 5) : Énergie & ATP, Génétique humaine & méiose, Géologie.
  * 🇬🇧 **Anglais** (Coeff 2) & 🧠 **Philosophie** (Coeff 2).
* 💡 **Fiches Mémo & Formules Clés** : Toutes les définitions et formules officielles accessibles directement sur chaque chapitre.
* 🏛️ **Annales Nationales Corrigées (2008 – 2025)** : Liens officiels vers les sujets et corrigés détaillés (Session Normale & Rattrapage).
* 📂 **Bibliothèque Locale de PDF** : Dossier `./pdf/` intégré pour stocker et consulter tous ses sujets et devoirs 100% hors-ligne.
* 🎯 **Simulateur de Note & Mention Bac** : Calcule en temps réel votre moyenne générale selon les coefficients officiels du Baccalauréat marocain.
* 🍅 **Chronomètre Pomodoro Intégré** : 25 min de révision / 5 min de pause avec bips sonores et vibrations haptiques.
* ⏳ **Compte à Rebours Bac 2026** : Suivi des jours, heures, minutes et secondes avant le coup d'envoi de la session normale.
* 📱 **PWA Installable** : Fonctionne sur Android, iOS, Windows et Mac comme une application native.

---

## 🚀 Installation & Utilisation

### En local :
1. Ouvrez simplement `index.html` dans n'importe quel navigateur (Google Chrome, Microsoft Edge, Mozilla Firefox, Safari).
2. Cliquez sur **📲 Installer** pour ajouter l'application à votre écran d'accueil.

### Téléchargement des PDF :
Pour récupérer automatiquement les premiers devoirs modèles dans le dossier `pdf/` :
```bash
python telecharger_examens.py
```

---

## 📂 Structure du Répertoire

```text
BAC2026/
├── index.html                   # Application principale PWA enrichie
├── 2BAC Maroc – Hub de révision.html
├── manifest.webmanifest         # Configuration PWA
├── sw.js                        # Service Worker (Cache hors-ligne)
├── icon.svg / icon-192.png / icon-512.png
├── telecharger_examens.py       # Script d'automatisation des téléchargements PDF
└── pdf/                         # Dossier des annales et devoirs PDF locaux
    ├── physique_chimie/
    ├── mathematiques/
    └── svt/
```
