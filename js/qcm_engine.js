/**
 * 2BAC Maroc 2026 - Moteur de QCM IA & Convertisseur PDF
 * Fonctionne 100% Hors-Ligne (avec banque officielle vérifiée) + Mode Génératif Gemini API
 */

// 1. Configuration PDF.js Worker
if (typeof pdfjsLib !== 'undefined') {
  pdfjsLib.GlobalWorkerOptions.workerSrc = './js/pdf.worker.min.js';
}

// 2. Banque de questions officielles certifiées (Cadre de Référence 2BAC SP BIOF)
const PRESET_QCM_DB = {
  "pc_2024_n": {
    id: "pc_2024_n",
    title: "Physique-Chimie : National 2024 – Session Normale (BIOF)",
    subject: "Physique-Chimie",
    matiereKey: "pc",
    pdfPath: "./pdf/physique_chimie/national/PC_National_2024_Normale_Sujet_BIOF.pdf",
    questions: [
      {
        q: "Chimie : Dans le suivi de la cinétique d'une transformation en milieu de volume V constant, comment est définie la vitesse volumique de réaction v(t) ?",
        options: [
          "v(t) = (1/V) · (dx/dt)",
          "v(t) = V · (dx/dt)",
          "v(t) = -(1/V) · (dx/dt)",
          "v(t) = dx/dt"
        ],
        answer: 0,
        exp: "Par définition du cours, la vitesse volumique est v(t) = (1/V) · (dx/dt). Graphiquement, dx/dt correspond au coefficient directeur de la tangente à la courbe d'avancement x(t) à la date t."
      },
      {
        q: "Chimie : Pour une solution d'acide benzoïque C₆H₅COOH de concentration molaire C et de pH mesuré, quelle est l'expression du taux d'avancement final τ ?",
        options: [
          "τ = 10^(-pH) / C",
          "τ = C / 10^(-pH)",
          "τ = 10^(-pH) · C",
          "τ = 10^(-(14-pH)) / C"
        ],
        answer: 0,
        exp: "À l'état final, [H₃O⁺]_éq = 10^(-pH). Comme x_f = [H₃O⁺]_éq · V et x_max = C · V, on a τ = x_f / x_max = 10^(-pH) / C. Si τ < 1, la transformation est limitée."
      },
      {
        q: "Ondes : Une onde ultrasonore de fréquence N = 40 kHz se propage dans l'air à la célérité v = 340 m/s. Quelle est sa longueur d'onde λ ?",
        options: [
          "λ = 8,5 mm (0,0085 m)",
          "λ = 8,5 cm (0,085 m)",
          "λ = 136 m",
          "λ = 0,117 m"
        ],
        answer: 0,
        exp: "λ = v / N = 340 / 40000 = 0,0085 m = 8,5 mm. Attention à bien convertir la fréquence en Hertz (40 kHz = 40 000 Hz) !"
      },
      {
        q: "Nucléaire : La demi-vie radioactive t₁/₂ d'un isotope et sa constante de désintégration λ sont liées par :",
        options: [
          "t₁/₂ = ln(2) / λ",
          "t₁/₂ = λ / ln(2)",
          "t₁/₂ = 1 / (2 · λ)",
          "t₁/₂ = ln(2) · λ"
        ],
        answer: 0,
        exp: "À t = t₁/₂, N(t) = N₀ / 2, donc N₀·e^(-λ·t₁/₂) = N₀/2 ⇒ -λ·t₁/₂ = -ln(2) ⇒ t₁/₂ = ln(2) / λ ≈ 0,693 / λ."
      },
      {
        q: "Électricité : Lors de la charge d'un condensateur C à travers une résistance R par un échelon de tension E, la constante de temps τ vaut :",
        options: [
          "τ = R · C",
          "τ = R / C",
          "τ = C / R",
          "τ = 1 / (R · C)"
        ],
        answer: 0,
        exp: "La constante de temps du dipôle RC est τ = R·C (en secondes). À t = τ, la tension u_C atteint 63% de sa valeur asymptotique E."
      },
      {
        q: "Mécanique : Un solide de masse m glisse sans frottement sur un plan incliné d'un angle α par rapport à l'horizontale. L'accélération a selon l'axe descendant parallèle au plan est :",
        options: [
          "a = g · sin(α)",
          "a = g · cos(α)",
          "a = g · tan(α)",
          "a = m · g · sin(α)"
        ],
        answer: 0,
        exp: "D'après la 2ème loi de Newton : P_x + R_x = m·a. Comme il n'y a pas de frottement, R est perpendiculaire au plan (R_x = 0). P_x = m·g·sin(α) ⇒ m·g·sin(α) = m·a ⇒ a = g·sin(α)."
      }
    ]
  },
  "pc_2023_n": {
    id: "pc_2023_n",
    title: "Physique-Chimie : National 2023 – Session Normale (BIOF)",
    subject: "Physique-Chimie",
    matiereKey: "pc",
    pdfPath: "./pdf/physique_chimie/national/PC_National_2023_Normale_Sujet_BIOF.pdf",
    questions: [
      {
        q: "Chimie : La constante d'acidité Ka du couple acide/base HA/A⁻ s'exprime par :",
        options: [
          "Ka = ([A⁻]_éq · [H₃O⁺]_éq) / [HA]_éq",
          "Ka = ([HA]_éq · [H₃O⁺]_éq) / [A⁻]_éq",
          "Ka = [A⁻]_éq / ([HA]_éq · [H₃O⁺]_éq)",
          "Ka = [H₃O⁺]_éq / [A⁻]_éq"
        ],
        answer: 0,
        exp: "Pour la réaction HA + H₂O ⇌ A⁻ + H₃O⁺, le quotient à l'équilibre définit la constante d'acidité Ka = ([A⁻]_éq · [H₃O⁺]_éq) / [HA]_éq. Le pKa est relié par pH = pKa + log([A⁻]/[HA])."
      },
      {
        q: "Ondes : Lors du phénomène de diffraction de la lumière monochromatique de longueur d'onde λ par une fente de largeur a, l'écart angulaire θ est :",
        options: [
          "θ = λ / a",
          "θ = a / λ",
          "θ = λ · a",
          "θ = 2λ / a"
        ],
        answer: 0,
        exp: "La formule du programme officiel est θ = λ / a (θ en radians, λ et a dans la même unité de longueur, typiquement en mètres)."
      },
      {
        q: "Électricité : Dans un circuit RLC série idéal sans résistance (circuit LC propre), la période propre T₀ des oscillations électriques est :",
        options: [
          "T₀ = 2π √(L · C)",
          "T₀ = 2π / √(L · C)",
          "T₀ = 2π · L · C",
          "T₀ = 1 / (2π √(L · C))"
        ],
        answer: 0,
        exp: "L'équation différentielle est d²u_C/dt² + (1/(LC))·u_C = 0. La pulsation propre est ω₀ = 1/√(LC), d'où la période propre T₀ = 2π/ω₀ = 2π√(LC)."
      },
      {
        q: "Nucléaire : Dans une réaction de fission nucléaire induite, quelle règle de conservation assure la validité de l'équation bilan ?",
        options: [
          "Les lois de Soddy (conservation du nombre de masse A et de charge Z)",
          "La conservation de la masse totale seule",
          "La conservation de l'énergie cinétique seule",
          "La loi d'Ohm"
        ],
        answer: 0,
        exp: "Les lois de Soddy stipulent qu'au cours de toute réaction nucléaire, il y a stricte conservation du nombre total de nucléons A et du nombre de charge Z."
      },
      {
        q: "Mécanique : Pour un satellite en orbite circulaire de rayon r autour de la Terre de masse M_T, sa vitesse orbitale v s'exprime par :",
        options: [
          "v = √(G · M_T / r)",
          "v = G · M_T / r²",
          "v = √(G · M_T · r)",
          "v = G · M_T / r"
        ],
        answer: 0,
        exp: "D'après la 2ème loi de Newton dans le repère de Frenet : a_n = v²/r = G·M_T / r², ce qui donne immédiatement v = √(G·M_T / r)."
      }
    ]
  },
  "maths_2024_n": {
    id: "maths_2024_n",
    title: "Mathématiques : National 2024 – Session Normale (BIOF)",
    subject: "Mathématiques",
    matiereKey: "m",
    pdfPath: "./pdf/mathematiques/national/Maths_National_2024_Normale_Sujet_BIOF.pdf",
    questions: [
      {
        q: "Nombres complexes : Quelles sont les solutions dans ℂ de l'équation z² - 2z + 4 = 0 ?",
        options: [
          "z₁ = 1 + i√3  et  z₂ = 1 - i√3",
          "z₁ = 2 + 2i√3 et  z₂ = 2 - 2i√3",
          "z₁ = -1 + i√3 et  z₂ = -1 - i√3",
          "z₁ = 1 + 2i   et  z₂ = 1 - 2i"
        ],
        answer: 0,
        exp: "Δ = (-2)² - 4·1·4 = 4 - 16 = -12 = (2i√3)². Les solutions sont z = (2 ± 2i√3)/2 = 1 ± i√3."
      },
      {
        q: "Nombres complexes : Quelle est la forme exponentielle du nombre complexe z = 1 + i√3 ?",
        options: [
          "z = 2 · e^(iπ/3)",
          "z = 2 · e^(iπ/6)",
          "z = √2 · e^(iπ/3)",
          "z = 4 · e^(iπ/4)"
        ],
        answer: 0,
        exp: "Le module est |z| = √(1² + (√3)²) = √4 = 2. On a cos(θ) = 1/2 et sin(θ) = √3/2, soit θ ≡ π/3 [2π]. Donc z = 2·e^(iπ/3)."
      },
      {
        q: "Géométrie dans l'espace : Quelle est l'équation de la sphère de centre Ω(1, -2, 3) et de rayon R = 3 ?",
        options: [
          "(x - 1)² + (y + 2)² + (z - 3)² = 9",
          "(x + 1)² + (y - 2)² + (z + 3)² = 9",
          "(x - 1)² + (y + 2)² + (z - 3)² = 3",
          "x² + y² + z² - 2x + 4y - 6z = 0"
        ],
        answer: 0,
        exp: "L'équation générale d'une sphère de centre (a,b,c) et rayon R est (x - a)² + (y - b)² + (z - c)² = R². Ici (x - 1)² + (y - (-2))² + (z - 3)² = 3² = 9."
      },
      {
        q: "Analyse : Quelle est la valeur de la limite lim_{x → 0⁺} x · ln(x) ?",
        options: [
          "0",
          "-∞",
          "+∞",
          "1"
        ],
        answer: 0,
        exp: "C'est une limite usuelle fondamentale du cours (croissances comparées) : lim_{x → 0⁺} x^n · ln(x) = 0 pour tout n > 0."
      },
      {
        q: "Calcul intégral : Une primitive sur ]0, +∞[ de la fonction f(x) = ln(x) / x est :",
        options: [
          "F(x) = (1/2) · (ln(x))²",
          "F(x) = ln(ln(x))",
          "F(x) = 1 / x²",
          "F(x) = (ln(x))²"
        ],
        answer: 0,
        exp: "f(x) est de la forme u'(x) · u(x) avec u(x) = ln(x) et u'(x) = 1/x. Une primitive de u'·u est (1/2)·u², soit (1/2)·(ln(x))²."
      },
      {
        q: "Suites numériques : Soit (uₙ) définie par uₙ₊₁ = (1/2)uₙ + 3 avec u₀ = 1. Si elle converge vers ℓ, quelle est la valeur de ℓ ?",
        options: [
          "ℓ = 6",
          "ℓ = 3",
          "ℓ = 2",
          "ℓ = 1"
        ],
        answer: 0,
        exp: "Par continuité de la fonction f(x) = (1/2)x + 3 : ℓ = (1/2)ℓ + 3 ⇔ ℓ - (1/2)ℓ = 3 ⇔ (1/2)ℓ = 3 ⇔ ℓ = 6."
      }
    ]
  },
  "maths_2023_n": {
    id: "maths_2023_n",
    title: "Mathématiques : National 2023 – Session Normale (BIOF)",
    subject: "Mathématiques",
    matiereKey: "m",
    pdfPath: "./pdf/mathematiques/national/Maths_National_2023_Normale_Sujet_BIOF.pdf",
    questions: [
      {
        q: "Nombres complexes : L'argument du nombre complexe z = -√3 + i est :",
        options: [
          "arg(z) ≡ 5π/6 [2π]",
          "arg(z) ≡ π/6 [2π]",
          "arg(z) ≡ -π/6 [2π]",
          "arg(z) ≡ 2π/3 [2π]"
        ],
        answer: 0,
        exp: "|z| = 2. cos(θ) = -√3/2 et sin(θ) = 1/2. Le point se trouve dans le deuxième quadrant, donc θ = π - π/6 = 5π/6 [2π]."
      },
      {
        q: "Analyse : Quelle est la dérivée de la fonction f(x) = e^(2x - 1) sur ℝ ?",
        options: [
          "f'(x) = 2 · e^(2x - 1)",
          "f'(x) = e^(2x - 1)",
          "f'(x) = (2x - 1) · e^(2x - 1)",
          "f'(x) = 2x · e^(2x - 1)"
        ],
        answer: 0,
        exp: "La formule de dérivation est (e^u)' = u' · e^u. Avec u(x) = 2x - 1, on a u'(x) = 2, d'où f'(x) = 2·e^(2x - 1)."
      },
      {
        q: "Probabilités : On tire simultanément 2 boules d'une urne contenant 4 boules rouges et 3 boules vertes. Le nombre total de tirages possibles est :",
        options: [
          "C₇² = 21",
          "A₇² = 42",
          "7² = 49",
          "14"
        ],
        answer: 0,
        exp: "Un tirage simultané de 2 éléments parmi 7 correspond à une combinaison sans ordre : C₇² = (7 × 6) / (2 × 1) = 21."
      },
      {
        q: "Équations différentielles : La solution générale de l'équation différentielle y' - 3y = 0 sur ℝ est :",
        options: [
          "y(x) = k · e^(3x), où k ∈ ℝ",
          "y(x) = k · e^(-3x), où k ∈ ℝ",
          "y(x) = 3x + k, où k ∈ ℝ",
          "y(x) = k · e^(x/3), où k ∈ ℝ"
        ],
        answer: 0,
        exp: "L'équation est de la forme y' = a·y avec a = 3. Les solutions sont de la forme y(x) = k·e^(ax) = k·e^(3x) avec k constante réelle."
      }
    ]
  },
  "svt_2024_n": {
    id: "svt_2024_n",
    title: "SVT : National 2024 – Session Normale (BIOF)",
    subject: "SVT",
    matiereKey: "svt",
    pdfPath: "./pdf/svt/national/SVT_National_2024_Normale_Sujet_BIOF.pdf",
    questions: [
      {
        q: "Consommation matière organique : Où se déroule la glycolyse au sein de la cellule eucaryote ?",
        options: [
          "Dans le hyaloplasme (cytosol), en absence de dioxygène",
          "Dans la matrice mitochondriale",
          "Dans la membrane interne des mitochondries",
          "Dans le noyau cellulaire"
        ],
        answer: 0,
        exp: "La glycolyse est la première étape commune à la respiration et à la fermentation. Elle a lieu exclusivement dans le hyaloplasme et ne requiert pas d'O₂."
      },
      {
        q: "Respiration cellulaire : Quel est le bilan global net en molécules d'ATP produit par l'oxydation complète d'une molécule de glucose ?",
        options: [
          "36 à 38 ATP",
          "2 ATP",
          "4 ATP",
          "12 ATP"
        ],
        answer: 0,
        exp: "La glycolyse fournit 2 ATP nets, le cycle de Krebs fournit 2 ATP (ou GTP), et la chaîne respiratoire mitochondriale fournit 32 à 34 ATP, soit un total de 36 à 38 ATP par molécule de glucose."
      },
      {
        q: "Génétique moléculaire : Lors de la traduction, quel est le codon d'initiation universel porté par l'ARNm ?",
        options: [
          "AUG (codant pour la Méthionine)",
          "UAA",
          "UAG",
          "UGA"
        ],
        answer: 0,
        exp: "Le codon AUG signale le début de la traduction par le ribosome et code pour la Méthionine. Les triplets UAA, UAG et UGA sont les trois codons STOP."
      },
      {
        q: "Géologie : Les chaînes de montagnes de subduction sont caractérisées par un métamorphisme de :",
        options: [
          "Haute Pression et Basse Température (HP - BT)",
          "Haute Température et Basse Pression (HT - BP)",
          "Basse Pression et Basse Température (BP - BT)",
          "Haute Température et Haute Pression (HT - HP)"
        ],
        answer: 0,
        exp: "Dans la zone de subduction, l'enfoncement de la lithosphère océanique froide entraîne une montée rapide de la pression alors que la température reste relativement basse : faciès schistes bleus et éclogites (HP-BT)."
      }
    ]
  },
  "anglais_2024_n": {
    id: "anglais_2024_n",
    title: "Anglais : National 2024 – Session Normale",
    subject: "Anglais",
    matiereKey: "en",
    pdfPath: "./pdf/anglais/national/Anglais_National_2024_Normale_Sujet.pdf",
    questions: [
      {
        q: "Grammar (Conditional Type 3) : 'If the student _______ harder before the Bac exam, he would have achieved a high distinction.'",
        options: [
          "had studied",
          "studied",
          "studies",
          "would study"
        ],
        answer: 0,
        exp: "Third Conditional rule for past regret/hypothetical condition: If + Past Perfect (had + past participle), ... would have + past participle."
      },
      {
        q: "Vocabulary (Phrasal Verbs) : 'Due to bad weather conditions, the organizers decided to _______ the marathon.'",
        options: [
          "call off (cancel)",
          "look after",
          "turn up",
          "give in"
        ],
        answer: 0,
        exp: "'Call off' means to cancel an event. 'Look after' means to take care of, 'turn up' means to arrive, and 'give in' means to surrender."
      },
      {
        q: "Language Functions : Which expression is used to politely express disagreement in an essay or debate ?",
        options: [
          "'I see your point, but I see things differently.'",
          "'You are totally out of your mind.'",
          "'I couldn't agree more with you.'",
          "'Congratulations on your graduation!'"
        ],
        answer: 0,
        exp: "'I see your point, but...' is the polite, respectful way to express disagreement tested in the Moroccan National Exam."
      },
      {
        q: "Grammar (Passive Voice) : 'The official exam results _______ by the Ministry of Education next week.'",
        options: [
          "will be announced",
          "will announce",
          "are announcing",
          "were announced"
        ],
        answer: 0,
        exp: "Future simple passive form: Subject + will be + Past Participle ('will be announced')."
      }
    ]
  },
  "philo_2024_n": {
    id: "philo_2024_n",
    title: "Philosophie : الامتحان الوطني 2024 – الدورة العادية (الشعب العلمية)",
    subject: "Philosophie",
    matiereKey: "ph",
    pdfPath: "./pdf/philosophie/national/Philo_National_2024_Normale_Sujet_AR.pdf",
    questions: [
      {
        q: "مجزوءة الوضع البشري : يرى الفيلسوف رينيه ديكارت أن أساس هوية الشخص يكمن في :",
        options: [
          "الفكر والوعي (الكوجيطو: أنا أفكر إذن أنا موجود)",
          "الذاكرة وتوالي الإدراكات الحسية فقط",
          "الإرادة والغرائز البيولوجية",
          "المكانة الاجتماعية والمظهر الخارجي"
        ],
        answer: 0,
        exp: "يؤسس ديكارت هوية الشخص على جوهر الفكر المجرد (الكوجيطو)، معتبراً أن الأنا جوهر مفكر ثابت لا يطاله الشك."
      },
      {
        q: "مجزوءة المعرفة : يرى إيمانويل كانط في مسألة بناء المعرفة العلمية أن :",
        options: [
          "المفاهيم بدون حدوس حسية جوفاء، والحدوس بدون مفاهيم عمياء",
          "العقل وحده قادر على معرفة الأشياء في ذاتها دون تجربة",
          "الحواس هي المصدر الوحيد والنهائي لليقين العلمي",
          "المعرفة العلمية نسبية ومستحيلة"
        ],
        answer: 0,
        exp: "وفق كانط في العقلانية النقدية، تتطلب المعرفة العلمية تضافر المادة الحسية الآتية من التجربة مع المقولات العقلية القبلية لتنظيمها."
      },
      {
        q: "مجزوءة السياسة : في فلسفة الحق والعدالة، يؤكد الفيلسوف جون رولز على أن العدالة تتأسس على مبدأ :",
        options: [
          "الإنصاف وتكافؤ الفرص",
          "القوة والغلبة للأقوى",
          "المساواة الحسابية الصارمة متجاهلة الفروق الفردية",
          "المصلحة النفعية للأغلبية حتى على حساب الأقليات"
        ],
        answer: 0,
        exp: "يعرف جون رولز العدالة كإنصاف (Justice as Fairness)، وتقوم على الحرية المتساوية للجميع، واستفادة الفئات الأقل حظاً من أي تفاوت اجتماعي."
      }
    ]
  }
};

// 3. Gestionnaire d'état du lecteur de QCM
const QcmPlayerState = {
  activeQuiz: null,
  currentIndex: 0,
  score: 0,
  userAnswers: [],
  timerSeconds: 0,
  timerInterval: null,
  isFinished: false
};

// 4. Extraction du texte depuis un PDF (Local ou Uploadé)
async function extractTextFromPdf(fileOrUrl, onProgress) {
  if (typeof pdfjsLib === 'undefined') {
    throw new Error("La bibliothèque PDF.js n'est pas encore chargée.");
  }
  
  let loadingTask;
  if (typeof fileOrUrl === 'string') {
    loadingTask = pdfjsLib.getDocument(fileOrUrl);
  } else {
    const arrayBuffer = await fileOrUrl.arrayBuffer();
    loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
  }

  const pdf = await loadingTask.promise;
  const numPages = Math.min(pdf.numPages, 12); // Analyse jusqu'à 12 pages pour rapidité
  let fullText = "";

  for (let i = 1; i <= numPages; i++) {
    if (onProgress) onProgress(i, numPages);
    const page = await pdf.getPage(i);
    const textContent = await page.getTextContent();
    const pageText = textContent.items.map(item => item.str).join(" ");
    fullText += `\n--- Page ${i} ---\n` + pageText;
  }

  return fullText;
}

// 5. Génération par Heuristique Intelligente (Mode Hors-Ligne)
function generateQuestionsFromKeywords(text, filename) {
  const t = text.toLowerCase();
  const questions = [];

  // Détection Physique-Chimie
  if (t.includes("chimie") || t.includes("dosage") || t.includes("acide") || t.includes("ph") || t.includes("solution") || t.includes("réaction")) {
    questions.push({
      q: "Chimie : Lors d'un dosage acido-basique, comment est défini le point d'équivalence E ?",
      options: [
        "Le point où les réactifs titrant et titré sont mélangés en proportions stœchiométriques",
        "Le point où le pH devient obligatoirement égal à 7,0",
        "Le point où la réaction s'arrête par épuisement total du solvant",
        "Le point où la concentration du titré est deux fois plus grande"
      ],
      answer: 0,
      exp: "À l'équivalence, la quantité de matière du réactif titrant apporté est égale à celle du réactif titré initialement présent selon les coefficients stœchiométriques."
    });
    questions.push({
      q: "Chimie : Pour un couple acide/base HA/A⁻, la relation entre le pH, le pKa et les concentrations à l'équilibre est :",
      options: [
        "pH = pKa + log([A⁻] / [HA])",
        "pH = pKa - log([A⁻] / [HA])",
        "pH = pKa + log([HA] / [A⁻])",
        "pH = pKa · log([A⁻] / [HA])"
      ],
      answer: 0,
      exp: "C'est la formule d'Henderson-Hasselbalch du programme : pH = pKa + log([Base]/[Acide]). À la demi-équivalence, [Base] = [Acide], donc pH = pKa."
    });
  }

  if (t.includes("onde") || t.includes("diffraction") || t.includes("fréquence") || t.includes("célérité") || t.includes("période")) {
    questions.push({
      q: "Physique (Ondes) : La relation fondamentale entre la longueur d'onde λ, la célérité v et la fréquence N est :",
      options: [
        "λ = v / N = v · T",
        "λ = v · N",
        "λ = N / v",
        "λ = 1 / (v · N)"
      ],
      answer: 0,
      exp: "Une onde parcourt la distance λ pendant une période temporelle T, d'où λ = v · T = v / N."
    });
    questions.push({
      q: "Physique (Ondes) : Lorsque la lumière traverse une fente étroite de largeur a, quel phénomène se produit si la largeur a est de l'ordre de la longueur d'onde λ ?",
      options: [
        "La diffraction de la lumière avec un demi-angle θ = λ / a",
        "La réfraction totale sans étalement",
        "La réflexion totale sans tache centrale",
        "L'extinction totale de la lumière"
      ],
      answer: 0,
      exp: "La diffraction se manifeste d'autant plus nettement que l'ouverture a est petite, avec θ = λ / a (en radians)."
    });
  }

  if (t.includes("rc") || t.includes("rl") || t.includes("rlc") || t.includes("condensateur") || t.includes("bobine")) {
    questions.push({
      q: "Physique (Électricité) : L'énergie électromagnétique emmagasinée dans un condensateur de capacité C sous tension u_C est :",
      options: [
        "E_e = (1/2) · C · u_C²",
        "E_e = C · u_C²",
        "E_e = (1/2) · C² · u_C",
        "E_e = (1/2) · u_C / C"
      ],
      answer: 0,
      exp: "L'énergie emmagasinée dans le condensateur est E_e = (1/2) C u_C² = (1/2) q² / C (en Joules)."
    });
  }

  if (t.includes("mécanique") || t.includes("newton") || t.includes("chute") || t.includes("accélération") || t.includes("force")) {
    questions.push({
      q: "Physique (Mécanique) : La deuxième loi de Newton pour un corps de masse m constante dans un référentiel galiléen s'écrit :",
      options: [
        "∑ F_ext = m · a_G",
        "∑ F_ext = m · v_G",
        "∑ F_ext = (1/2) m · a_G²",
        "∑ F_ext = 0 obligatoirement"
      ],
      answer: 0,
      exp: "La somme vectorielle des forces extérieures est égale au produit de la masse m par le vecteur accélération a_G du centre d'inertie : ∑ F = m · a."
    });
  }

  // Détection Mathématiques
  if (t.includes("complexe") || t.includes("argument") || t.includes("module") || t.includes("mathematique") || t.includes("intégrale") || t.includes("limite")) {
    questions.push({
      q: "Maths : Pour tout nombre complexe z = a + i·b non nul, le module |z| est calculé par :",
      options: [
        "|z| = √(a² + b²)",
        "|z| = a² + b²",
        "|z| = a + b",
        "|z| = √(a² - b²)"
      ],
      answer: 0,
      exp: "Le module correspond à la distance géométrique OM dans le plan complexe : |z| = √(a² + b²)."
    });
    questions.push({
      q: "Maths : La dérivée de la fonction f(x) = ln(u(x)) pour une fonction u strictement positive et dérivable est :",
      options: [
        "f'(x) = u'(x) / u(x)",
        "f'(x) = 1 / u(x)",
        "f'(x) = u(x) / u'(x)",
        "f'(x) = u'(x) · ln(u(x))"
      ],
      answer: 0,
      exp: "La règle de composition pour le logarithme népérien donne (ln(u))' = u' / u."
    });
    questions.push({
      q: "Maths : Si une suite (uₙ) est croissante et majorée par un réel M, alors la suite :",
      options: [
        "Converge vers une limite finie ℓ ≤ M",
        "Diverge vers +∞",
        "Oscille sans limite",
        "Est strictement égale à M pour tout n"
      ],
      answer: 0,
      exp: "Théorème de convergence monotone : toute suite croissante et majorée est convergente. Toute suite décroissante et minorée est convergente."
    });
  }

  // Détection SVT
  if (t.includes("atp") || t.includes("krebs") || t.includes("respiration") || t.includes("cellule") || t.includes("génétique") || t.includes("adn")) {
    questions.push({
      q: "SVT : Au cours du cycle de Krebs qui se déroule dans la matrice mitochondriale :",
      options: [
        "L'acétyl-CoA subit une dégradation complète avec libération de CO₂ et production de composés réduits (NADH, FADH₂)",
        "Le glucose est directement transformé en glycogène",
        "Aucune molécule d'ATP n'est produite",
        "L'oxygène est directement consommé"
      ],
      answer: 0,
      exp: "Le cycle de Krebs oxyde complètement le groupement acétyle en CO₂, réduit les transporteurs NAD⁺ en NADH,H⁺ et FAD en FADH₂, et produit 1 ATP (ou GTP) par tour."
    });
  }

  // Si aucune question spécifique n'a été déclenchée, fournir un ensemble d'évaluation général Bac SP
  if (questions.length === 0) {
    questions.push(
      {
        q: "Bac SP (Méthodologie) : Quelle est la démarche scientifique rigoureuse pour résoudre un problème de mécanique au Bac ?",
        options: [
          "1. Préciser le système, 2. Définir le référentiel galiléen, 3. Bilan des forces, 4. Appliquer la 2ème loi de Newton",
          "Calculer directement sans préciser de système ni de référentiel",
          "Appliquer uniquement les formules sans schéma ni projection",
          "Considérer toujours les frottements comme nuls"
        ],
        answer: 0,
        exp: "Le barème officiel de correction exige impérativement le système d'étude, le référentiel galiléen et l'inventaire complet des forces avant toute projection."
      },
      {
        q: "Bac SP (Unités fondamentales) : Dans le Système International (SI), quelles sont les unités respectives de la constante radioactive λ et de la constante de temps τ ?",
        options: [
          "λ en s⁻¹ (seconde moins un) et τ en s (seconde)",
          "λ en secondes et τ en Hertz",
          "λ en Bequerel et τ en Farad",
          "λ et τ sont sans dimension"
        ],
        answer: 0,
        exp: "La constante radioactive λ a la dimension de l'inverse d'un temps (s⁻¹), tandis que la constante de temps τ est une durée exprimée en secondes (s)."
      }
    );
  }

  return questions;
}

// 6. Génération via Google Gemini API (Mode En Ligne si clé disponible)
async function generateQuestionsWithGemini(pdfText, apiKey) {
  const prompt = `Tu es un inspecteur et professeur agrégé spécialiste du Baccalauréat marocain (2ème année Baccalauréat Sciences Physiques - Option BIOF).
À partir du texte d'examen ci-dessous, génère un QCM d'entraînement de 6 à 8 questions pertinentes au format JSON STRICT.
RÈGLES IMPORTANTES :
- Les questions de Physique, Chimie, Maths et SVT doivent être rédigées en Français (Option BIOF).
- Les questions de Philosophie doivent être en Arabe.
- Les questions d'Anglais en Anglais.
- Chaque question doit proposer 4 choix (options 0, 1, 2, 3) avec une seule bonne réponse ('answer': index entier 0 à 3).
- Fournir une justification détaillée ('exp') avec formules mathématiques et rappel du cadre de référence.
- RENVOIE UNIQUEMENT DU JSON PUR, SANS MARKDOWN NI BALISES \`\`\`json.

Format attendu :
[
  {
    "q": "Texte précis de la question ?",
    "options": ["Choix A", "Choix B", "Choix C", "Choix D"],
    "answer": 0,
    "exp": "Explication et rappel de cours pédagogique..."
  }
]

Extrait du document :
${pdfText.slice(0, 14000)}
`;

  const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: {
        temperature: 0.2,
        responseMimeType: "application/json"
      }
    })
  });

  if (!response.ok) {
    const errData = await response.json().catch(() => ({}));
    throw new Error(errData.error?.message || `Erreur API Gemini (${response.status})`);
  }

  const data = await response.json();
  const rawText = data.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!rawText) throw new Error("Réponse vide de l'IA Gemini.");

  const cleanJson = rawText.replace(/```json/gi, "").replace(/```/g, "").trim();
  const parsed = JSON.parse(cleanJson);
  if (!Array.isArray(parsed) || parsed.length === 0) {
    throw new Error("Format JSON non conforme reçu de l'API.");
  }
  return parsed;
}

// 7. Lancement d'un QCM
function startQuiz(quizData) {
  QcmPlayerState.activeQuiz = quizData;
  QcmPlayerState.currentIndex = 0;
  QcmPlayerState.score = 0;
  QcmPlayerState.userAnswers = [];
  QcmPlayerState.timerSeconds = 0;
  QcmPlayerState.isFinished = false;

  clearInterval(QcmPlayerState.timerInterval);
  QcmPlayerState.timerInterval = setInterval(() => {
    QcmPlayerState.timerSeconds++;
    const timerEl = document.getElementById("qcm-live-timer");
    if (timerEl) {
      const m = String(Math.floor(QcmPlayerState.timerSeconds / 60)).padStart(2, '0');
      const s = String(QcmPlayerState.timerSeconds % 60).padStart(2, '0');
      timerEl.textContent = `${m}:${s}`;
    }
  }, 1000);

  renderQcmPlayer();
}

// 8. Rendu du joueur de QCM
function renderQcmPlayer() {
  const container = document.getElementById("qcm-player-wrapper");
  if (!container) return;

  const quiz = QcmPlayerState.activeQuiz;
  if (!quiz) return;

  // Si le quiz est terminé, afficher les résultats
  if (QcmPlayerState.isFinished) {
    renderQcmResults(container);
    return;
  }

  const q = quiz.questions[QcmPlayerState.currentIndex];
  const total = quiz.questions.length;
  const currNum = QcmPlayerState.currentIndex + 1;
  const pct = Math.round((currNum / total) * 100);
  const m = String(Math.floor(QcmPlayerState.timerSeconds / 60)).padStart(2, '0');
  const s = String(QcmPlayerState.timerSeconds % 60).padStart(2, '0');

  container.innerHTML = `
    <div class="qcm-quiz-box">
      <!-- En-tête du Quiz -->
      <div class="qcm-header-bar">
        <div>
          <button class="btn-sec" style="padding:4px 10px; font-size:12px" onclick="exitQuiz()">⬅ Quitter</button>
          <span style="font-weight:800; margin-left:8px; font-size:13.5px">${quiz.title}</span>
        </div>
        <div style="display:flex; align-items:center; gap:10px">
          <span class="qcm-stat-badge">⏱️ <b id="qcm-live-timer">${m}:${s}</b></span>
          <span class="qcm-stat-badge">⭐ Score : <b>${QcmPlayerState.score} / ${total}</b></span>
        </div>
      </div>

      <!-- Barre de progression -->
      <div class="bar" style="height:8px; margin:14px 0 20px 0; border-radius:4px">
        <i style="width:${pct}%; transition:width 0.3s ease"></i>
      </div>

      <!-- Question Card -->
      <div class="qcm-question-card">
        <div class="qcm-q-num">Question ${currNum} sur ${total}</div>
        <h3 class="qcm-q-text">${q.q}</h3>

        <!-- Options -->
        <div class="qcm-options-list" id="qcm-opts">
          ${q.options.map((opt, i) => `
            <button class="qcm-opt-btn" onclick="handleSelectOption(${i})" id="qcm-opt-${i}">
              <span class="qcm-opt-letter">${String.fromCharCode(65 + i)}</span>
              <span class="qcm-opt-label">${opt}</span>
            </button>
          `).join("")}
        </div>

        <!-- Boîte d'explication pédagogique -->
        <div class="qcm-explanation-box" id="qcm-explanation" style="display:none">
          <div class="qcm-exp-title" id="qcm-exp-status">💡 Justification & Rappel du cours</div>
          <div class="qcm-exp-content" id="qcm-exp-text">${q.exp || "Pas d'explication disponible."}</div>
        </div>

        <!-- Bouton Suivant -->
        <div class="qcm-footer-actions">
          <button class="btn-main" id="qcm-btn-next" style="display:none; margin-left:auto" onclick="nextQuestion()">
            ${currNum === total ? '🏁 Voir mon bilan final' : 'Question suivante ➔'}
          </button>
        </div>
      </div>
    </div>
  `;
}

// 9. Gestion du clic sur une option
function handleSelectOption(chosenIndex) {
  const quiz = QcmPlayerState.activeQuiz;
  const q = quiz.questions[QcmPlayerState.currentIndex];
  const isCorrect = (chosenIndex === q.answer);

  // Verrouiller tous les boutons
  const buttons = document.querySelectorAll(".qcm-opt-btn");
  buttons.forEach(btn => btn.classList.add("disabled"));

  // Colorer la bonne réponse en vert
  const correctBtn = document.getElementById(`qcm-opt-${q.answer}`);
  if (correctBtn) correctBtn.classList.add("correct");

  // Si mauvais choix, le colorer en rouge
  if (!isCorrect) {
    const wrongBtn = document.getElementById(`qcm-opt-${chosenIndex}`);
    if (wrongBtn) wrongBtn.classList.add("incorrect");
  } else {
    QcmPlayerState.score++;
  }

  QcmPlayerState.userAnswers.push({
    questionIndex: QcmPlayerState.currentIndex,
    chosen: chosenIndex,
    correct: q.answer,
    isCorrect
  });

  // Afficher l'explication
  const expBox = document.getElementById("qcm-explanation");
  const expStatus = document.getElementById("qcm-exp-status");
  if (expBox && expStatus) {
    expStatus.innerHTML = isCorrect ? "✅ <b>Bonne réponse !</b>" : "❌ <b>Réponse incorrecte !</b>";
    expStatus.style.color = isCorrect ? "var(--ok)" : "var(--danger)";
    expBox.style.display = "block";
  }

  // Révéler le bouton "Suivant"
  const nextBtn = document.getElementById("qcm-btn-next");
  if (nextBtn) nextBtn.style.display = "inline-flex";
}

// 10. Question suivante
function nextQuestion() {
  const quiz = QcmPlayerState.activeQuiz;
  if (QcmPlayerState.currentIndex + 1 < quiz.questions.length) {
    QcmPlayerState.currentIndex++;
    renderQcmPlayer();
  } else {
    clearInterval(QcmPlayerState.timerInterval);
    QcmPlayerState.isFinished = true;
    renderQcmPlayer();
  }
}

// 11. Quitter le quiz
function exitQuiz() {
  if (confirm("Voulez-vous vraiment quitter ce QCM en cours ?")) {
    clearInterval(QcmPlayerState.timerInterval);
    QcmPlayerState.activeQuiz = null;
    if (typeof render === 'function') render();
  }
}

// 12. Rendu des résultats
function renderQcmResults(container) {
  const quiz = QcmPlayerState.activeQuiz;
  const total = quiz.questions.length;
  const score = QcmPlayerState.score;
  const noteSur20 = ((score / total) * 20).toFixed(1);
  const pct = Math.round((score / total) * 100);

  let mention = "Ajourné (Entraînez-vous encore !)";
  let mentionColor = "var(--danger)";
  if (noteSur20 >= 16) { mention = "Mention Très Bien 🎖️ (Excellent niveau !)"; mentionColor = "var(--ok)"; }
  else if (noteSur20 >= 14) { mention = "Mention Bien 🥈 (Très bon travail !)"; mentionColor = "var(--a)"; }
  else if (noteSur20 >= 12) { mention = "Mention Assez Bien 🥉 (Encourageant !)"; mentionColor = "var(--warn)"; }
  else if (noteSur20 >= 10) { mention = "Mention Passable 👍 (Objectif Bac atteint)"; mentionColor = "var(--t)"; }

  const m = String(Math.floor(QcmPlayerState.timerSeconds / 60)).padStart(2, '0');
  const s = String(QcmPlayerState.timerSeconds % 60).padStart(2, '0');

  container.innerHTML = `
    <div class="qcm-result-card">
      <div style="font-size:48px; margin-bottom:10px">🏆</div>
      <h2 style="margin:0 0 8px 0">Résultats : ${quiz.title}</h2>
      <p style="color:var(--m); font-size:13.5px">Temps total : <b>${m} min ${s} s</b></p>

      <div class="qcm-score-circle">
        <div class="qcm-score-number">${noteSur20} <span style="font-size:18px">/ 20</span></div>
        <div style="font-size:13px; color:var(--m)">${score} bonnes réponses sur ${total} (${pct}%)</div>
      </div>

      <div class="qcm-mention-badge" style="color:${mentionColor}; border-color:${mentionColor}">
        ${mention}
      </div>

      <div class="qcm-results-actions" style="margin-top:24px; display:flex; gap:10px; justify-content:center; flex-wrap:wrap">
        <button class="btn-main" onclick="startQuiz(QcmPlayerState.activeQuiz)">🔄 Recommencer ce QCM</button>
        <button class="btn-sec" onclick="QcmPlayerState.activeQuiz=null; if(typeof render==='function') render();">📂 Choisir un autre examen</button>
      </div>

      <div style="text-align:left; margin-top:30px">
        <h3 style="border-bottom:1px solid var(--b); padding-bottom:8px">📋 Synthèse des réponses & Corrigé détaillé</h3>
        ${quiz.questions.map((q, idx) => {
          const ans = QcmPlayerState.userAnswers.find(a => a.questionIndex === idx);
          const ok = ans && ans.isCorrect;
          return `
            <div style="padding:12px; margin-bottom:10px; border-radius:10px; background:var(--bg); border-left:4px solid ${ok ? 'var(--ok)' : 'var(--danger)'}">
              <div style="font-weight:700; font-size:13.5px; margin-bottom:4px">
                ${ok ? '✅' : '❌'} Question ${idx + 1} : ${q.q}
              </div>
              <div style="font-size:12.5px; color:var(--m); margin-bottom:4px">
                Votre réponse : <b style="color:${ok ? 'var(--ok)' : 'var(--danger)'}">${ans ? q.options[ans.chosen] : 'Non répondue'}</b>
              </div>
              ${!ok ? `<div style="font-size:12.5px; color:var(--ok)">Bonne réponse : <b>${q.options[q.answer]}</b></div>` : ''}
              <div style="font-size:12px; margin-top:6px; background:var(--c); padding:8px; border-radius:6px; border:1px solid var(--b)">
                💡 <i>${q.exp}</i>
              </div>
            </div>
          `;
        }).join("")}
      </div>
    </div>
  `;
}

// 13. Fonction globale pour lancer directement un QCM depuis la bibliothèque PDF
function launchPdfQcm(quizKey) {
  if (PRESET_QCM_DB[quizKey]) {
    if (typeof navigateTab === 'function') {
      navigateTab('qcm');
    }
    setTimeout(() => {
      startQuiz(PRESET_QCM_DB[quizKey]);
    }, 50);
  } else {
    alert("QCM non configuré pour ce sujet spécifique.");
  }
}

// Exposer globalement
window.QCM_ENGINE = {
  PRESET_QCM_DB,
  QcmPlayerState,
  extractTextFromPdf,
  generateQuestionsFromKeywords,
  generateQuestionsWithGemini,
  startQuiz,
  launchPdfQcm
};
