#!/usr/bin/env python3
import yaml, os, shutil
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('_templates'), autoescape=True)

# Kategorien einlesen
kategorien = []
kat_dir = '_kategorien'
if os.path.exists(kat_dir):
    for fname in sorted(os.listdir(kat_dir)):
        if fname.endswith('.yaml') or fname.endswith('.yml'):
            with open(os.path.join(kat_dir, fname), encoding='utf-8') as f:
                kat = yaml.safe_load(f)
                if kat:
                    kategorien.append(kat)

# About-Daten
with open('_data/about.yaml', encoding='utf-8') as f:
    about = yaml.safe_load(f)

# dist/ vorbereiten
os.makedirs('dist', exist_ok=True)

# Statische Dateien zuerst kopieren
for fname in ['styles.css', 'scripts.js']:
    shutil.copy(fname, f'dist/{fname}')
    print(f'✓ dist/{fname}')

# Admin
if os.path.exists('dist/admin'):
    shutil.rmtree('dist/admin')
shutil.copytree('admin', 'dist/admin')
print('✓ dist/admin/')

# Bilder — IMMER kopieren, auch wenn leer
os.makedirs('dist/images/portfolio', exist_ok=True)
if os.path.exists('images/portfolio'):
    for fname in os.listdir('images/portfolio'):
        src = os.path.join('images/portfolio', fname)
        dst = os.path.join('dist/images/portfolio', fname)
        shutil.copy2(src, dst)
    count = len(os.listdir('images/portfolio'))
    print(f'✓ dist/images/portfolio/  ({count} Bilder)')
else:
    print('✓ dist/images/portfolio/  (leer, Ordner angelegt)')

# index.html
tmpl = env.get_template('index.html')
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(tmpl.render(kategorien=kategorien))
print('✓ dist/index.html')

# Kategorie-Seiten
tmpl = env.get_template('kategorie.html')
for kat in kategorien:
    slug = kat.get('slug', '')
    if not slug:
        continue
    with open(f'dist/{slug}.html', 'w', encoding='utf-8') as f:
        f.write(tmpl.render(kat=kat))
    print(f'✓ dist/{slug}.html  ({len(kat.get("bilder", []))} Bilder)')

# about.html
tmpl = env.get_template('about.html')
with open('dist/about.html', 'w', encoding='utf-8') as f:
    f.write(tmpl.render(about=about))
print('✓ dist/about.html')

# course.html
tmpl = env.get_template('course.html')
with open('dist/course.html', 'w', encoding='utf-8') as f:
    f.write(tmpl.render())
print('✓ dist/course.html')

print(f'\nBuild fertig → dist/  ({len(kategorien)} Kategorien)')
