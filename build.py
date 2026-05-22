#!/usr/bin/env python3
"""
Build-Skript: Liest _data/*.yaml und generiert HTML-Dateien.
Wird von Netlify automatisch bei jedem Git-Push ausgeführt.
"""
import yaml, os
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('_templates'), autoescape=True)

# Daten laden
with open('_data/kategorien.yaml', encoding='utf-8') as f:
    kategorien = yaml.safe_load(f)

with open('_data/about.yaml', encoding='utf-8') as f:
    about = yaml.safe_load(f)

os.makedirs('dist', exist_ok=True)

# index.html
tmpl = env.get_template('index.html')
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(tmpl.render(kategorien=kategorien))
print('✓ dist/index.html')

# about.html
tmpl = env.get_template('about.html')
with open('dist/about.html', 'w', encoding='utf-8') as f:
    f.write(tmpl.render(about=about))
print('✓ dist/about.html')

# course.html (statisch, kein Daten-Template nötig)
tmpl = env.get_template('course.html')
with open('dist/course.html', 'w', encoding='utf-8') as f:
    f.write(tmpl.render())
print('✓ dist/course.html')

# Statische Dateien kopieren
import shutil
for fname in ['styles.css', 'scripts.js']:
    shutil.copy(fname, f'dist/{fname}')
    print(f'✓ dist/{fname}')

# Admin-Ordner kopieren
if os.path.exists('dist/admin'):
    shutil.rmtree('dist/admin')
shutil.copytree('admin', 'dist/admin')
print('✓ dist/admin/')

# Bilder-Ordner kopieren falls vorhanden
if os.path.exists('images'):
    if os.path.exists('dist/images'):
        shutil.rmtree('dist/images')
    shutil.copytree('images', 'dist/images')
    print('✓ dist/images/')

print('\nBuild fertig → dist/')
