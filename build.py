#!/usr/bin/env python3
import yaml, os, shutil
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('_templates'), autoescape=True)

# Kategorien: jede Datei in _kategorien/ ist eine Kategorie
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

os.makedirs('dist', exist_ok=True)

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

# Statische Dateien
for fname in ['styles.css', 'scripts.js']:
    shutil.copy(fname, f'dist/{fname}')
    print(f'✓ dist/{fname}')

# Admin
if os.path.exists('dist/admin'):
    shutil.rmtree('dist/admin')
shutil.copytree('admin', 'dist/admin')
print('✓ dist/admin/')

# Bilder
if os.path.exists('images'):
    if os.path.exists('dist/images'):
        shutil.rmtree('dist/images')
    shutil.copytree('images', 'dist/images')
    print('✓ dist/images/')

print(f'\nBuild fertig → dist/  ({len(kategorien)} Kategorien)')
