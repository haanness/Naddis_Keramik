#!/usr/bin/env python3
import yaml, os, shutil
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('_templates'), autoescape=True)

# ── Daten laden ──────────────────────────────────────────
with open('_data/nav.yaml', encoding='utf-8') as f:
    nav = yaml.safe_load(f)

with open('_data/about.yaml', encoding='utf-8') as f:
    about = yaml.safe_load(f)

with open('_data/course.yaml', encoding='utf-8') as f:
    course = yaml.safe_load(f)

# Kategorien
kategorien = []
for fname in sorted(os.listdir('_kategorien')):
    if fname.endswith('.yaml') or fname.endswith('.yml'):
        with open(os.path.join('_kategorien', fname), encoding='utf-8') as f:
            kat = yaml.safe_load(f)
            if kat:
                kategorien.append(kat)

# Freie Seiten
freie_seiten = []
if os.path.exists('_seiten'):
    for fname in sorted(os.listdir('_seiten')):
        if fname.endswith('.yaml') or fname.endswith('.yml'):
            with open(os.path.join('_seiten', fname), encoding='utf-8') as f:
                seite = yaml.safe_load(f)
                if seite:
                    freie_seiten.append(seite)

# ── dist/ vorbereiten ────────────────────────────────────
os.makedirs('dist', exist_ok=True)

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
os.makedirs('dist/images/portfolio', exist_ok=True)
if os.path.exists('images/portfolio'):
    for fname in os.listdir('images/portfolio'):
        shutil.copy2(f'images/portfolio/{fname}', f'dist/images/portfolio/{fname}')
    print(f'✓ dist/images/portfolio/  ({len(os.listdir("images/portfolio"))} Bilder)')

# ── Seiten generieren ────────────────────────────────────
ctx = dict(nav=nav, kategorien=kategorien)

# index.html
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(env.get_template('index.html').render(**ctx))
print('✓ dist/index.html')

# Kategorieseiten
for kat in kategorien:
    slug = kat.get('slug', '')
    if not slug:
        continue
    with open(f'dist/{slug}.html', 'w', encoding='utf-8') as f:
        f.write(env.get_template('kategorie.html').render(kat=kat, **ctx))
    print(f'✓ dist/{slug}.html  ({len(kat.get("bilder", []))} Bilder)')

# about.html
with open('dist/about.html', 'w', encoding='utf-8') as f:
    f.write(env.get_template('about.html').render(about=about, **ctx))
print('✓ dist/about.html')

# course.html
with open('dist/course.html', 'w', encoding='utf-8') as f:
    f.write(env.get_template('course.html').render(course=course, **ctx))
print('✓ dist/course.html')

# Freie Seiten
for seite in freie_seiten:
    slug = seite.get('slug', '')
    if not slug:
        continue
    with open(f'dist/{slug}.html', 'w', encoding='utf-8') as f:
        f.write(env.get_template('freie-seite.html').render(seite=seite, **ctx))
    print(f'✓ dist/{slug}.html  (freie Seite)')

print(f'\nBuild fertig → dist/  ({len(kategorien)} Kategorien, {len(freie_seiten)} freie Seiten)')
