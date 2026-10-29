# Call Me Maybe — TODO & suivi de progression

> **École 42 — Projet déjà validé, repris pour approfondir l'Applied AI Engineering.**  
> **Priorité du cursus :** passer ensuite à **RAG Against the Machine**, à rendre **et valider avant le 30 avril 2027** (pace 22).  
> **Objectif de ce document :** suivre ce qui a été **vérifié**, ce qui reste à développer, et les critères permettant de considérer le projet terminé.

**Dernière mise à jour :** 28 octobre 2026  
**Étape pédagogique actuelle :** **5 / 12 — Prompt dynamique et premier test de function calling avec Qwen**  
**Avancement estimé du développement :** **≈ 25 %**, estimation indicative et non note officielle.  
**Source de référence :** sujet officiel `Call_me_maybe.pdf` fourni pour le projet ; en cas de doute, **le sujet prime**.

## Légende

- `[x]` **Fait et observé** dans nos échanges / résultats du terminal.
- `[ ]` **À faire, à vérifier ou à finaliser**. Une case non cochée ne signifie pas nécessairement que le fichier n'existe pas.
- **P0 — Obligatoire** pour satisfaire le sujet et obtenir un programme utilisable.
- **P1 — Qualité** nécessaire à une soumission robuste et défendable.
- **P2 — Bonus ciblé** utile au parcours d'AI Engineer, uniquement **après** la partie obligatoire.
- **Hors périmètre actuel :** autres bonus non prioritaires ; ne pas retarder RAG pour les réaliser.

---

## 0. État connu de notre codebase

Arborescence observée le 28 octobre 2026 :

```text
Call_Me_Maybe/
├── data/
│   └── input/
│       ├── function_calling_tests.json
│       └── functions_definition.json
├── llm_sdk/
│   ├── llm_sdk/__init__.py
│   ├── pyproject.toml
│   └── uv.lock
├── Makefile
├── pyproject.toml
├── README.md
├── src/
│   ├── __init__.py
│   ├── __main__.py
│   ├── decoder.py
│   ├── file_handler.py
│   ├── llm.py
│   ├── models.py
│   ├── pipeline.py
│   ├── prompting.py
│   └── select_token.py
├── tests/
└── uv.lock
```

**Attention :** `tree` ne montre pas les fichiers cachés par défaut (`.gitignore`, `.venv`, `.python-version`...) et affiche les `__pycache__` : ces derniers ne doivent pas être versionnés. L'existence d'un fichier (`decoder.py`, `pipeline.py`, `Makefile`...) n'établit **pas** que son contenu remplit déjà le sujet.

### Composants effectivement testés

- [x] `uv sync` fonctionnel ; environnement Python 3.11 utilisé.
- [x] Import de `Small_LLM_Model` depuis `llm_sdk`.
- [x] Chargement de `Qwen/Qwen3-0.6B` sur le Mac M2.
- [x] `src/file_handler.py` : lecture réussie d'un fichier JSON ; erreur explicite pour un chemin inexistant.
- [x] `src/models.py` : validation Pydantic des **11 prompts** du jeu fourni.
- [x] `src/models.py` : validation des **5 définitions de fonctions** fournies.
- [x] `ParametreDefinition` : rejet des types non autorisés avec `Literal` (test `banana`).
- [x] `src/llm.py` : `encode()`, `decode()` et observation des token IDs de `Greet shrek`.
- [x] Lecture de `vocab.json` via le chemin retourné par le SDK ; observation de l'entrée `Ġsh`.
- [x] `get_logits_from_input_ids()` : réception de **151 936** scores pour une requête testée.
- [x] Première boucle de génération greedy de 10 tokens, sans API `generate()`.
- [x] `src/select_token.py` : sélection du meilleur logit parmi des IDs autorisés.
- [x] Démonstration du contrôle : token ` Paris` choisi sans contrainte, ` located` choisi quand le meilleur token est exclu.
- [x] `src/prompting.py` : construction et affichage d'un prompt contenant les **5 fonctions** et la requête `What is the sum of 2 and 3?`.

### Points connus à reprendre

- [ ] Corriger les petites fautes de texte dans le prompt (`funciton` → `function`, ponctuation, etc.).
- [ ] Nettoyer le code d'exploration temporaire dans `src/llm.py` ou le déplacer dans des scripts/tests d'expérimentation.
- [ ] Vérifier les types, signatures, docstrings et traitements d'erreur de tous les modules actuels.
- [ ] Vérifier le contenu réel de `decoder.py`, `pipeline.py`, `__main__.py`, `Makefile` et `README.md` avant de leur attribuer un état « terminé ».

---

## 1. Roadmap pédagogique — 12 étapes

| Étape | Sujet | État |
|---|---|---|
| 1 | Environnement, `uv`, SDK, Qwen | ✅ Fait |
| 2 | Lecture JSON, exceptions, modèles Pydantic | ✅ Fondamentaux faits ; robustesse finale à tester |
| 3 | Tokenisation et vocabulaire | ✅ Fait |
| 4 | Logits, greedy decoding, sélection de tokens | ✅ Fait en prototype |
| 5 | Prompt dynamique pour function calling | 🔄 Construction faite ; **test réel Qwen à faire** |
| 6 | Parseur de JSON et préfixes valides | ⬜ À faire |
| 7 | Masquage des logits et génération contrainte | ⬜ À faire |
| 8 | Contraintes dynamiques sur noms, arguments, types | ⬜ À faire |
| 9 | Pipeline complet, entrée/sortie, CLI | ⬜ À faire |
| 10 | Tests, précision, robustesse, performance | ⬜ À faire |
| 11 | Makefile, lint, README, préparation du rendu | ⬜ À vérifier / compléter |
| 12 | Défense technique et bonus ciblés | ⬜ À faire après la partie obligatoire |

---

## 2. P0 — Étape 5 : premier vrai function calling avec Qwen (PROCHAINE SÉANCE)

**Pourquoi :** mesurer ce que le modèle sait produire avec le prompt seul, avant d'imposer des contraintes de génération.

- [x] Charger les fonctions via `load_json_file()` et les valider avec `FunctionDefinition`.
- [x] Convertir les objets Pydantic avec `model_dump()` puis `json.dumps()`.
- [x] Construire une chaîne contenant instructions + fonctions disponibles + demande utilisateur.
- [ ] Relire le prompt pour limiter l'ambiguïté et les instructions inutiles.
- [ ] Charger `Small_LLM_Model` **une seule fois** pour l'expérience.
- [ ] Utiliser `build_prompt(...)`, puis `model.encode(...)`.
- [ ] Générer une réponse avec une boucle token par token, sans contrainte dans un premier temps.
- [ ] Séparer les tokens d'entrée des tokens générés (`prompt_length`).
- [ ] Ajouter une limite `max_new_tokens` et un mécanisme d'arrêt sûr.
- [ ] Afficher et analyser la sortie brute obtenue pour `What is the sum of 2 and 3?`.
- [ ] Recommencer sur au moins une requête `greet`, une `reverse_string` et une requête `regex`.
- [ ] Relever les erreurs éventuelles : prose ajoutée, JSON incomplet, mauvais nom, arguments incorrects.
- [ ] **Ne pas confondre** un JSON obtenu spontanément et une garantie de constrained decoding.

**Critère de sortie :** nous savons expliquer ce que Qwen produit sans contraintes et pourquoi le prompt seul ne suffit pas.

---

## 3. P0 — Étape 6 : parseur JSON et validation des préfixes (`src/decoder.py`)

**Pourquoi :** décider si un token candidat peut prolonger le JSON en cours sans rendre impossible une sortie finale valide.

- [ ] Définir clairement l'interface d'un validateur : préfixe courant, schéma attendu, verdict.
- [ ] Distinguer **JSON complet valide** et **préfixe incomplet mais encore valide**.
- [ ] Suivre les états structurels nécessaires : objets, tableaux, clés, séparateurs `:`, virgules et fermeture.
- [ ] Gérer les chaînes JSON : guillemets, caractères échappés (`\"`, `\\`), caractères spéciaux, Unicode.
- [ ] Gérer les valeurs numériques, y compris les formes partielles en cours de génération (signe, décimales, exposants si pris en charge).
- [ ] Prévoir les littéraux JSON (`true`, `false`, `null`) pour les schémas correspondants.
- [ ] Vérifier les fermetures correctes des structures imbriquées.
- [ ] Reconnaître l'état **objet attendu complètement terminé** pour arrêter la génération.
- [ ] Empêcher toute sortie supplémentaire après la fin de l'objet autorisé.
- [ ] Écrire des tests pour les préfixes valides, invalides, incomplets et les caractères échappés.
- [ ] Éviter d'utiliser `json.loads()` seul comme test de préfixe : il rejette naturellement les objets non terminés mais encore générables.

**Critère de sortie :** le validateur accepte les préfixes qui peuvent encore aboutir à un JSON conforme et rejette les impossibilités structurelles.

---

## 4. P0 — Étape 7 : constrained decoding token par token (`src/decoder.py` + `src/select_token.py`)

**Pourquoi :** remplacer le simple choix greedy par un choix parmi des tokens dont l'ajout reste autorisé.

- [ ] Concevoir une fonction `get_allowed_tokens(...)` ou un mécanisme équivalent fondé sur le validateur.
- [ ] Consulter le vocabulaire du tokenizer pour connaître les fragments associés aux IDs.
- [ ] Traiter correctement les espaces intégrés aux tokens et les tokens à plusieurs caractères.
- [ ] Prendre en compte les subtilités byte-level/Unicode : décoder isolément un token n'est pas toujours équivalent à décoder une séquence complète.
- [ ] Vérifier les IDs spéciaux et la différence observée entre les **151 643** entrées de `vocab.json` et les **151 936** positions de logits : ne pas supposer un alignement naïf.
- [ ] Récupérer les logits depuis **l'API publique du SDK exclusivement**.
- [ ] Interdire les tokens incompatibles (logit `-inf` ou sélection directe parmi les IDs permis, selon l'architecture choisie).
- [ ] Réutiliser et fiabiliser `select_token()` : gérer explicitement la liste vide, les indices hors plage et les scores invalides.
- [ ] Mettre à jour le contexte avec le token choisi à chaque itération.
- [ ] Arrêter uniquement à la fin d'une sortie JSON **complète et conforme**, ou sur une erreur/limite explicite.
- [ ] Définir un comportement sûr si aucun token valide n'est disponible.
- [ ] Définir un plafond de tokens et un plafond de durée pour éviter les boucles infinies.
- [ ] Tester qu'un token préféré par Qwen est bien refusé lorsqu'il casserait le schéma.

**Critère de sortie :** une génération contrôlée produit un JSON complet et décodable, sans dépendre de l'obéissance spontanée du modèle à une instruction textuelle.

---

## 5. P0 — Étape 8 : schémas dynamiques de function calling

**Pourquoi :** générer non seulement du JSON, mais un appel de fonction valide pour **les définitions chargées à l'exécution**.

- [ ] Définir la structure générée par Qwen : `{"name": ..., "parameters": {...}}`.
- [ ] Construire la liste des **noms de fonctions autorisés dynamiquement**, jamais codés en dur.
- [ ] Faire choisir la fonction **par le LLM** ; ne pas utiliser de règles du type `if "sum" in prompt`.
- [ ] Conditionner les arguments autorisés sur la fonction effectivement sélectionnée.
- [ ] Imposer les noms de paramètres exacts définis dans `functions_definition.json`.
- [ ] Garantir la présence de tous les arguments requis et l'absence d'arguments supplémentaires.
- [ ] Respecter les types déclarés (`number`, `string`, et les autres types effectivement supportés).
- [ ] Distinguer une chaîne contenant `"2"` d'un nombre JSON `2` ; éviter les confusions booléen/entier en Python.
- [ ] Vérifier qu'un objet généré est cohérent **dans son ensemble** (pas seulement chaque token séparément).
- [ ] Faire évoluer les modèles Pydantic si les définitions d'évaluation exigent des formes non encore gérées.
- [ ] Ajouter une validation finale indépendante du texte généré.
- [ ] Tester avec des définitions de fonctions **différentes des cinq exemples fournis**.
- [ ] Éviter toute hypothèse codée en dur sur l'ordre des fonctions ou des arguments.

**Critère de sortie :** une nouvelle liste de fonctions utilisables peut être chargée sans modifier le code métier.

---

## 6. P0 — Étape 9 : pipeline et interface CLI (`src/pipeline.py`, `src/__main__.py`)

**Pourquoi :** transformer les prototypes en un programme exécutable conforme au sujet.

- [ ] Définir le pipeline : **lecture → validation → prompt → inférence → décodage contraint → validation → écriture**.
- [ ] Charger Qwen une seule fois puis réutiliser la même instance pour tous les prompts.
- [ ] Charger et valider les fichiers `functions_definition` et `input`.
- [ ] Traiter chaque requête et conserver l'ordre des prompts d'entrée.
- [ ] Ajouter `prompt` dans le résultat via Python à partir de l'entrée initiale (sans le faire recopier au LLM).
- [ ] Garantir **exactement** trois clés par entrée de sortie : `prompt`, `name`, `parameters`.
- [ ] Produire un **tableau JSON unique** dans `data/output/function_calls.json`.
- [ ] Créer `data/output/` automatiquement si nécessaire.
- [ ] Écrire avec `encoding="utf-8"`, sérialisation JSON fiable, sans texte supplémentaire ni `NaN`/`Infinity` non conformes.
- [ ] Gérer proprement fichiers manquants, JSON malformé, définitions incohérentes et génération impossible.
- [ ] Ajouter la CLI exigée par le sujet :

  ```bash
  uv run python -m src
  uv run python -m src \
    --functions_definition data/input/functions_definition.json \
    --input data/input/function_calling_tests.json \
    --output data/output/function_calls.json
  ```

- [ ] Vérifier les valeurs par défaut et les chemins personnalisés (`--functions_definition`, `--input`, `--output`).
- [ ] Éviter de laisser un fichier de sortie trompeur ou incomplet en cas d'échec global ; journaliser des erreurs compréhensibles.
- [ ] Vérifier que les résultats sont produits **sans appel à une API de génération interdite** ni méthode privée du SDK.

**Critère de sortie :** `uv run python -m src` génère le fichier attendu pour toutes les entrées fournies.

---

## 7. P1 — Étape 10 : tests, fiabilité et performances (`tests/`)

### Tests fonctionnels

- [ ] Exécuter le pipeline sur les **11 prompts** du jeu de test fourni.
- [ ] Vérifier la fonction sélectionnée et les arguments extraits pour chaque prompt.
- [ ] Tester les cinq fonctions d'exemple : addition, salutation, inversion, racine carrée, remplacement regex.
- [ ] Ajouter de nouveaux prompts et de nouvelles définitions pour vérifier la généralisation.
- [ ] Tester chaînes vides, espaces, guillemets, caractères Unicode et caractères échappés.
- [ ] Tester nombres négatifs, décimaux, grands nombres et représentations numériques délicates.
- [ ] Tester fonctions à plusieurs paramètres, noms similaires, consignes ambiguës.
- [ ] Tester fichier absent, JSON invalide, tableau vide, champs manquants, types incorrects.
- [ ] Tester la détection d'une liste de tokens autorisés vide et d'une génération qui atteint sa limite.

### Mesures exigées par le sujet

- [ ] **≥ 90 %** de bonnes sélections de fonctions **et** d'extractions d'arguments sur les jeux évalués.
- [ ] **100 %** de fichiers JSON analysables et conformes aux schémas de fonctions.
- [ ] **Moins de 5 minutes** pour traiter l'ensemble des prompts de test sur matériel standard.
- [ ] Mesurer le temps total et, si possible, le temps par prompt.
- [ ] Distinguer les échecs **sémantiques** (mauvaise fonction/valeur) des échecs **structurels** (JSON/schema).
- [ ] Optimiser seulement après avoir identifié un véritable goulot d'étranglement.

### Outillage de test

- [ ] Développer une suite de tests automatisés (par exemple `pytest` ou `unittest`).
- [ ] Tester séparément Pydantic, parseur, sélection de tokens, pipeline et format de sortie.
- [ ] Conserver des tests de non-régression pour les bugs rencontrés.

**Critère de sortie :** les exigences du sujet sont démontrées par des tests reproductibles, et pas seulement par une démonstration ponctuelle.

---

## 8. P1 — Étape 11 : qualité, Makefile, README, rendu

### Qualité Python

- [ ] Vérifier Python **3.10+** selon le sujet (notre environnement local actuel est Python 3.11).
- [ ] Vérifier les dépendances et le verrouillage `uv.lock` : `uv sync` doit fonctionner sur un environnement propre.
- [ ] Vérifier que les classes du projet utilisent **Pydantic** pour la validation.
- [ ] Respecter les interfaces **publiques** de `llm_sdk` uniquement.
- [ ] Ne pas importer dans notre implémentation les bibliothèques interdites par le sujet (`torch`, `transformers`, `huggingface`, `dspy`, `outlines`, etc.). Le fait que le SDK fourni utilise des dépendances internes ne nous autorise pas à les appeler directement.
- [ ] Ajouter ou corriger les annotations de types et les docstrings (PEP 257).
- [ ] Faire passer **flake8** et **mypy** ; revoir les exceptions et ressources ouvertes.

### Makefile — fichier existant, règles à vérifier

- [ ] `make install` : installer/synchroniser les dépendances.
- [ ] `make run` : exécuter l'application.
- [ ] `make debug` : utiliser le débogueur Python.
- [ ] `make clean` : retirer les fichiers temporaires et caches.
- [ ] `make lint` : exécuter exactement les vérifications exigées :

  ```bash
  flake8 .
  mypy . --warn-return-any --warn-unused-ignores \
    --ignore-missing-imports --disallow-untyped-defs \
    --check-untyped-defs
  ```

### README.md — fichier existant, contenu à vérifier

- [ ] Première ligne en italique selon la formule officielle : `This project has been created as part of the 42 curriculum by <login>.` (remplacer `<login>` par le vrai login 42).
- [ ] README entièrement rédigé **en anglais**.
- [ ] Sections **Description**, **Instructions**, **Resources**.
- [ ] Expliquer comment installer et exécuter le programme, avec exemples de CLI.
- [ ] Décrire l'algorithme de constrained decoding et les décisions d'architecture.
- [ ] Documenter les résultats de précision, latence, fiabilité et les limites connues.
- [ ] Décrire les difficultés rencontrées, les corrections, la stratégie de test.
- [ ] Déclarer comment l'IA a été utilisée pour le projet.

### Préparation du dépôt

- [ ] Vérifier `.gitignore` (notamment `.venv`, `__pycache__`, `.mypy_cache`, fichiers générés).
- [ ] Conserver les fichiers requis à la racine, notamment `src/`, `llm_sdk/`, `pyproject.toml`, `uv.lock`, `data/input/` et README.
- [ ] Ne pas soumettre le dossier de sortie générée `data/output/`.
- [ ] Lancer le projet depuis un clone propre pour vérifier sa reproductibilité.
- [ ] Préparer une présentation orale du pipeline : expliquer les logits, le masque, la grammaire, le schéma et les compromis de performance.

---

## 9. P2 — Bonus ciblés utiles à l'Applied AI Engineering

> **Règle :** commencer les bonus uniquement lorsque les exigences obligatoires fonctionnent. Les bonus ne sont évalués à 42 que si la partie obligatoire est parfaite. Notre priorité reste RAG.

- [ ] **Tests automatisés approfondis** : bon investissement pour apprendre l'ingénierie de fiabilité.
- [ ] **Mesures et optimisation des performances** : profiler les étapes, ajouter cache/mémoïsation seulement lorsque pertinent.
- [ ] **Gestion d'erreurs avancée** : diagnostics explicites, limites, éventuelle stratégie de reprise sûre.
- [ ] **Arguments imbriqués** : uniquement si le décodeur principal est assez stable et si le temps le permet.

### Bonus volontairement non prioritaires

- [ ] Support complet de plusieurs modèles LLM — **reporté**.
- [ ] Réimplémentation du tokenizer / `encode` / `decode` — **reportée**.
- [ ] Visualisation sophistiquée de la génération — **reportée**.
- [ ] Démonstrations supplémentaires d'intégration tokenizer/decoder — **optionnelles** si déjà couvertes par nos tests.

**Décision d'arrêt :** ne pas prolonger Call Me Maybe pour cocher tous les bonus ; passer à **RAG Against the Machine** dès que les fondamentaux et une implémentation de qualité ont été assimilés.

---

## 10. Jalons pratiques pour les prochaines séances

- [ ] **Jalon A :** obtenir le premier appel `fn_add_numbers(a=2, b=3)` généré par Qwen **sans contrainte** et comprendre les éventuelles erreurs.
- [ ] **Jalon B :** écrire et tester un validateur de préfixes JSON sur des exemples simples.
- [ ] **Jalon C :** générer un premier objet JSON par sélection de tokens réellement contrainte.
- [ ] **Jalon D :** faire respecter un schéma de fonction (nom + paramètres + types).
- [ ] **Jalon E :** connecter le pipeline pour tous les prompts, sans traitement codé en dur.
- [ ] **Jalon F :** démontrer les objectifs de précision, conformité et temps.
- [ ] **Jalon G :** nettoyer et documenter le projet ; choisir éventuellement 1 à 3 bonus ciblés.
- [ ] **Jalon H :** clôturer l'apprentissage Call Me Maybe et commencer RAG.

### Reprise rapide dans une nouvelle conversation

> Nous travaillons sur **Call Me Maybe (École 42)** comme projet pédagogique, déjà validé auparavant. Notre méthode : **pourquoi → concept → code → terminal → architecture**. Nous avons terminé les étapes 1 à 4 ; l'étape **5 (prompt dynamique)** est entamée. `src/prompting.py` imprime déjà les cinq fonctions JSON et le premier prompt. **Prochaine action : envoyer ce prompt à Qwen, générer une sortie sans contraintes, puis analyser les résultats.** Le vrai décodeur JSON reste à construire. **Ne pas perdre de vue RAG Against the Machine, à valider avant le 30 avril 2027.**

---

## 11. Définition de « terminé »

Nous considérerons **la partie obligatoire Call Me Maybe terminée** lorsque toutes ces affirmations seront vraies :

- [ ] `uv sync` installe le projet proprement.
- [ ] `uv run python -m src` fonctionne avec les chemins par défaut **et** les options personnalisées.
- [ ] Le programme choisit les fonctions via Qwen, **sans heuristiques de sélection codées en dur**.
- [ ] Le choix des tokens est réellement contraint pendant la génération, à partir du schéma dynamique.
- [ ] `data/output/function_calls.json` contient un tableau JSON avec exactement `prompt`, `name`, `parameters` par entrée.
- [ ] Toutes les sorties sont conformes aux fonctions définies et aux types attendus.
- [ ] Les objectifs de **90 %+ précision**, **100 % conformité** et **moins de 5 minutes** sont atteints sur les tests appropriés.
- [ ] Les erreurs sont gérées clairement ; les chemins personnalisés et jeux de fonctions différents sont testés.
- [ ] `make lint`, Makefile et README répondent aux exigences du sujet.
- [ ] Nous savons **expliquer et défendre** chaque composant sans dépendre d'un code seulement copié.

**Après cela :** bonus sélectionnés uniquement si utiles, puis **RAG Against the Machine**.
