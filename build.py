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
    if fname.endswith('.yaml') or fname.endswith('.yml'):
        with open(os.path.join('_kategorien', fname), encoding='utf-8') as f:
            kat = yaml.safe_load(f)
            if kat:
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
    print(f'✓ dist/images/portfolio/  ({len(os.listdir("images/portfolio"))} Bilder)')

ctx = dict(nav=nav, kategorien=kategorien)

with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(env.get_template('index.html').render(**ctx))
print('✓ dist/index.html')

for kat in kategorien:
    slug = kat.get('slug', '')
    if not slug:
        continue
    with open(f'dist/{slug}.html', 'w', encoding='utf-8') as f:
        f.write(env.get_template('kategorie.html').render(kat=kat, **ctx))
    print(f'✓ dist/{slug}.html  ({len(kat.get("bilder", []))} Bilder)')

with open('dist/about.html', 'w', encoding='utf-8') as f:
    f.write(env.get_template('about.html').render(about=about, **ctx))
print('✓ dist/about.html')

with open('dist/course.html', 'w', encoding='utf-8') as f:
    f.write(env.get_template('course.html').render(course=course, **ctx))
print('✓ dist/course.html')

print(f'\nBuild fertig → dist/  ({len(kategorien)} Kategorien)')
