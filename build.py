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
os.makedirs('dist', exist_ok=True)

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

ctx = dict(nav=nav, kategorien=kategorien)

# index.html
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(env.get_template('index.html').render(**ctx))
print('✓ dist/index.html')

# Kategorieseiten mit prev/next
for i, kat in enumerate(kategorien):
    slug = kat.get('slug', '')
    if not slug:
        continue
    prev_kat = kategorien[i - 1] if i > 0 else None
    next_kat = kategorien[i + 1] if i < len(kategorien) - 1 else None
    with open(f'dist/{slug}.html', 'w', encoding='utf-8') as f:
        f.write(env.get_template('kategorie.html').render(
            kat=kat,
            prev_kat=prev_kat,
            next_kat=next_kat,
            **ctx
        ))
    for j, b in enumerate(kat.get('bilder', [])):
        felder = [k for k in b.keys() if k != 'bild']
        if any(b.get(k) for k in felder):
            print(f'  Bild {j+1}: {[b.get(k) for k in felder]}')
    print(f'✓ dist/{slug}.html ({len(kat.get("bilder",[]))} Bilder)')

# about.html
with open('dist/about.html', 'w', encoding='utf-8') as f:
    f.write(env.get_template('about.html').render(about=about, **ctx))
print('✓ dist/about.html')

# course.html
with open('dist/course.html', 'w', encoding='utf-8') as f:
    f.write(env.get_template('course.html').render(course=course, **ctx))
print('✓ dist/course.html')

print(f'\nBuild fertig → dist/ ({len(kategorien)} Kategorien)')
