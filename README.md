# Naddi's Ceramiche — Website

Statische Portfolio-Website mit Decap CMS zur einfachen Inhaltsverwaltung.

---

## Einmalige Einrichtung (ca. 20 Minuten)

### 1. GitHub-Konto erstellen
→ https://github.com/signup (kostenlos)

### 2. Neues Repository erstellen
- Auf GitHub: **New repository**
- Name: `naddis-ceramiche` (oder beliebig)
- **Public** auswählen
- Repository erstellen

### 3. Dateien hochladen
- Im neuen Repo auf **"uploading an existing file"** klicken
- Alle Dateien aus diesem ZIP hochladen
- Commit: "Initial upload"

### 4. Netlify-Konto erstellen
→ https://app.netlify.com/signup (kostenlos, am besten mit GitHub-Login)

### 5. Seite deployen
- Netlify Dashboard → **"Add new site" → "Import an existing project"**
- GitHub auswählen → dein Repo auswählen
- Build-Einstellungen werden automatisch aus `netlify.toml` gelesen
- **"Deploy site"** klicken → nach ~1 Minute ist die Seite live

### 6. Netlify Identity aktivieren
- Im Netlify Dashboard: **Site configuration → Identity → Enable Identity**
- Unter **Registration**: auf **"Invite only"** stellen
- Unter **Services → Git Gateway**: **Enable Git Gateway** klicken

### 7. Einladung an Nadia senden
- Identity → **"Invite users"** → E-Mail-Adresse eingeben
- Nadia bekommt eine E-Mail, setzt ihr Passwort und kann sofort loslegen

---

## CMS benutzen

**Login:** `https://deine-seite.netlify.app/admin`

Im CMS kann Nadia:
- **Kategorien:** Neue Bilder zu einer Kategorie hinzufügen, Reihenfolge ändern, neue Kategorien anlegen
- **About me:** Texte und Profilfoto aktualisieren
- Nach dem Speichern wird die Seite automatisch neu gebaut (~1 Minute)

---

## Dateistruktur

```
_data/
  kategorien.yaml   ← Portfolio-Inhalte (vom CMS bearbeitet)
  about.yaml        ← About-Seite (vom CMS bearbeitet)
_templates/
  base.html         ← Gemeinsames Layout
  index.html        ← Portfolio-Template
  about.html        ← About-Template
  course.html       ← Course-Template
admin/
  config.yml        ← CMS-Konfiguration
  index.html        ← CMS-Interface
images/portfolio/   ← Hochgeladene Bilder landen hier
build.py            ← Generiert dist/ aus Templates + Daten
netlify.toml        ← Netlify Build-Konfiguration
styles.css          ← Alle Styles
scripts.js          ← Minimales JavaScript
```
