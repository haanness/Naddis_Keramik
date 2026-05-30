#!/usr/bin/env python3
import yaml, os, shutil
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('_templates'), autoescape=True)

# Daten laden
with open('_data/nav.yaml', encoding='utf-8') as f:
    nav = yaml.safe_load(f)
with open('_data/about.yaml', encoding='utf-8') as f:
    about = yaml.safe_load(f)
with open('_data/course.yaml', encoding='utf-8') as f:
    course = yaml.safe_load(f)

kategorien = []
for fname in sorted(os.listdir('_kategorien')):
    if not (fname.endswith('.yaml') or fname.endswith('.yml')):
        continue
    with open(os.path.join('_kategorien', fname), encoding='utf-8') as f:
        kat = yaml.safe_load(f)
    if not kat:
        continue
    if 'bilder' not in kat or kat['bilder'] is None:
        kat['bilder'] = []
    kategorien.append(kat)

# dist/ aufbauen
os.makedirs('dist/de', exist_ok=True)
os.makedirs('dist/it', exist_ok=True)
os.makedirs('dist/en', exist_ok=True)

for fname in ['styles.css', 'scripts.js']:
    shutil.copy(fname, f'dist/{fname}')
    print(f'✓ dist/{fname}')

if os.path.exists('dist/admin'):
    shutil.rmtree('dist/admin')
shutil.copytree('admin', 'dist/admin')
print('✓ dist/admin/')

os.makedirs('dist/images/portfolio', exist_ok=True)
if os.path.exists('images/portfolio'):
    for fname in os.listdir('images/portfolio'):
        shutil.copy2(f'images/portfolio/{fname}', f'dist/images/portfolio/{fname}')
    print(f'✓ dist/images/portfolio/ ({len(os.listdir("images/portfolio"))} Bilder)')

# Seiten für alle drei Sprachen generieren
for lang in ['de', 'it', 'en']:
    ctx = dict(nav=nav, kategorien=kategorien, lang=lang)

    # index.html
    with open(f'dist/{lang}/index.html', 'w', encoding='utf-8') as f:
        f.write(env.get_template('index.html').render(**ctx))
    print(f'✓ dist/{lang}/index.html')

    # Kategorieseiten
    for i, kat in enumerate(kategorien):
        slug = kat.get('slug', '')
        if not slug:
            continue
        prev_kat = kategorien[i - 1] if i > 0 else None
        next_kat = kategorien[i + 1] if i < len(kategorien) - 1 else None
        with open(f'dist/{lang}/{slug}.html', 'w', encoding='utf-8') as f:
            f.write(env.get_template('kategorie.html').render(
                kat=kat, prev_kat=prev_kat, next_kat=next_kat, **ctx
            ))
    print(f'✓ dist/{lang}/ Kategorien ({len(kategorien)})')

    # about.html
    with open(f'dist/{lang}/about.html', 'w', encoding='utf-8') as f:
        f.write(env.get_template('about.html').render(about=about, **ctx))
    print(f'✓ dist/{lang}/about.html')

    # course.html
    with open(f'dist/{lang}/course.html', 'w', encoding='utf-8') as f:
        f.write(env.get_template('course.html').render(course=course, **ctx))
    print(f'✓ dist/{lang}/course.html')

# Root index.html: leitet zur Browsersprache weiter (DE als Standard)
root_redirect = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<script>
  var lang = (navigator.language || navigator.userLanguage || 'de').toLowerCase();
  if (lang.startsWith('it')) {
    window.location.replace('/it/index.html');
  } else if (lang.startsWith('en')) {
    window.location.replace('/en/index.html');
  } else {
    window.location.replace('/de/index.html');
  }
</script>
<meta http-equiv="refresh" content="0;url=/de/index.html">
</head>
<body></body>
</html>"""

with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(root_redirect)
print('✓ dist/index.html (Sprachweiche)')

print(f'\nBuild fertig → dist/ (DE + IT + EN, {len(kategorien)} Kategorien)')
