#!/usr/bin/env python3
"""Simple generator pour créer un fichier exercice à partir du template.
Usage example:
  python scripts/create_exercise.py --slug boucle-while --title "Boucle While" \
    --description "Objectif: afficher 0,2,4,6,8,10" --code-file sample_code.py \
    --expected 0,2,4,6,8,10

Le script crée `exercises/<slug>.html` en remplaçant les placeholders du template.
"""
import argparse
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'templates' / 'exercise-template.html'
OUT_DIR = ROOT / 'exercices'

parser = argparse.ArgumentParser(description='Générateur d\'exercice à partir du template')
parser.add_argument('--slug', required=True, help='identifiant/nom de fichier (sans extension)')
parser.add_argument('--title', required=True, help='Titre de l\'exercice')
parser.add_argument('--description', required=True, help='HTML ou texte court décrivant la consigne')
parser.add_argument('--code-file', help='Fichier contenant le code initial (si présent)')
parser.add_argument('--code', help='Code initial en ligne (sans passer par un fichier)')
parser.add_argument('--expected', required=True, help='Valeurs attendues séparées par des virgules (ex: 0,2,4)')

args = parser.parse_args()

if not TEMPLATE.exists():
    raise SystemExit(f"Template introuvable: {TEMPLATE}")

if args.code_file:
    code_path = Path(args.code_file)
    if not code_path.exists():
        raise SystemExit(f"Fichier de code introuvable: {code_path}")
    code = code_path.read_text()
elif args.code:
    code = args.code
else:
    code = '# Ecrivez votre code ici\n'

expected_list = [s.strip() for s in args.expected.split(',') if s.strip() != '']
expected_json = json.dumps(expected_list)

out = OUT_DIR
out.mkdir(parents=True, exist_ok=True)

content = TEMPLATE.read_text(encoding='utf-8')
content = content.replace('{{TITLE}}', args.title)
content = content.replace('{{DESCRIPTION}}', args.description)
content = content.replace('{{INITIAL_CODE}}', code)
# Replace expected placeholder (support with or without spaces)
content = content.replace('{{EXPECTED_LINES}}', expected_json)
content = content.replace('{{ EXPECTED_LINES }}', expected_json)

out_file = out / f"{args.slug}.html"
out_file.write_text(content, encoding='utf-8')
print(f"Exercice créé: {out_file}")
