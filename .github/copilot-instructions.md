# Copilot instructions — Exercice Python interactif

**But**: Permettre à un agent AI d'être immédiatement productif sur ce dépôt minimaliste (page statique d'exercices Python exécutés dans le navigateur).

## Vue d'ensemble
- Code principal : `index.html` (page statique).
- Pattern principal : éditeur Ace + Pyodide chargé depuis CDN → exécution asynchrone du code utilisateur → capture de stdout vers une div HTML → validation JS côté client.
- Composants clés à connaître :
  - Chargement Pyodide : `<script src="https://cdn.jsdelivr.net/pyodide/v0.23.4/full/pyodide.js"></script>`
  - Editeur Ace : `<script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.32.7/ace.js"></script>`
  - Éditeur : `<div id="editor">...</div>` (le code initial est le contenu HTML de ce div)
  - Validation : fonction `checkResult(output)` (compare lignes à un tableau `expected`).

## Actions courantes (pour un agent)
- Ouvrir et tester localement :
  - Servir la page via un serveur HTTP (les CDNs et Pyodide peuvent échouer depuis `file://`). Exemple :

    ```bash
    python -m http.server 8000
    # puis ouvrir http://localhost:8000
    ```

  - Alternativement utiliser l'extension Live Server de VS Code.
- Déboguer : utiliser la Console et l'onglet Réseau du navigateur. Les erreurs de `pyodide.runPythonAsync` remontent dans la console et sont aussi affichées dans `#output`.

## Conventions et points importants
- Validation simple côté client :
  - `pyodide.setStdout({ batched: (msg) => outputDiv.innerText += msg + "\n" });` redirige les `print()` vers `#output`.
  - `checkResult(output)` attend une sortie ligne-par-ligne (ex: `["0","2","4","6","8","10"]`).
  - Si vous ajoutez un nouvel exercice, mettez à jour le tableau `expected` et (si besoin) la logique de parsing dans `checkResult`.
- Code initial & reset :
  - Le code initial est pris depuis `editor.getValue()` au chargement et stocké dans `initialCode`.
  - `resetCode()` appelle `editor.setValue(initialCode)`.
- Bouton d'exécution : désactivé tant que Pyodide n'est pas prêt (`runBtn.disabled = true` jusqu'à la fin de `main()`). Ne changer que si vous modifiez la séquence d'initialisation.

## Guide rapide pour ajouter / modifier un exercice
1. Modifier le titre et la consigne dans la section HTML (`h1`, `.consigne`).
2. Remplacer le contenu du `<div id="editor">...</div>` par le code initial souhaité.
3. Adapter la validation en modifiant `expected` et/ou `checkResult` (dans le `<script>` en bas de la page).
4. Tester localement via `python -m http.server` et vérifier la console / sortie.

## Modèles & générateur (template)
- Fichier modèle : `templates/exercise-template.html` — contient des placeholders : `{{TITLE}}`, `{{DESCRIPTION}}`, `{{INITIAL_CODE}}`, `{{EXPECTED_LINES}}` (où `EXPECTED_LINES` est un JSON array, ex: `["0","2","4"]`).
- Générateur pratique : `scripts/create_exercise.py`
  - Exemple d'utilisation :

```bash
python scripts/create_exercise.py \
  --slug boucle-while \
  --title "Boucle While" \
  --description "Objectif : afficher 0,2,4,6,8,10 (un par ligne)" \
  --code-file sample_code.py \
  --expected 0,2,4,6,8,10
```

  - Le script génère `exercises/<slug>.html` en remplaçant automatiquement les placeholders.
  - Si vous modifiez la structure du template, mettez à jour le script ou adaptez `{{EXPECTED_LINES}}` au format JSON attendu par `checkResult()`.

## Règles pour les agents AI (comportements attendus)
- Priorité : ne modifiez que `index.html` ou les fichiers dans `exercises/` à moins qu'une refactorisation soit explicitement demandée.
- Lorsque vous changez la validation, fournissez toujours un exemple d'entrée attendue (tests manuels via `expected`) et montrez un extrait de sortie attendu.
- Si vous mettez à jour une dépendance CDN (ex: version Pyodide), testez la page en local et vérifiez que `runBtn` s'active et que `pyodide.runPythonAsync` fonctionne sans erreurs réseau.

## Questions ouvertes / limites détectées
- Il n'y a pas de suite de tests automatisés ni de script de build dans le dépôt. Documenter et ajouter des tests serait une amélioration future (à demander explicitement).
- Les validations sont limitées à des comparaisons lignes-à-lignes ; pour des sorties plus complexes, ajoutez une logique de parsing plus robuste dans `checkResult`.

---
Si vous voulez, je peux :
- Ajouter un template (boilerplate) pour créer facilement de nouveaux exercices (HTML + validation JS),
- Ou intégrer une petite suite de tests automatisés (ex: Puppeteer/Playwright) qui lance la page et vérifie la validation.

Dites-moi quelle option vous préférez ou si une partie du texte doit être reformulée ou complétée.