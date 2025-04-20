import os
import hashlib

LIST_FILE = 'icons.txt'
TEMPLATE_FILE = 'template.html'
OUTPUT_DIR = '.' # Hauptverzeichnis des Repos
GENERATED_PAGES_PREFIX = 'favicon_page_' # Präfix für generierte Dateinamen

def get_existing_pages(directory, prefix):
    """Findet vorhandene, von diesem Skript generierte Seiten."""
    pages = set()
    for filename in os.listdir(directory):
        if filename.startswith(prefix) and filename.endswith('.html'):
            pages.add(filename)
    return pages

def create_page_filename(icon_url):
    """Erstellt einen eindeutigen Dateinamen basierend auf der URL."""
    # Hash der URL verwenden, um Kollisionen zu vermeiden und eine feste Länge zu haben
    url_hash = hashlib.md5(icon_url.encode()).hexdigest()
    return f"{GENERATED_PAGES_PREFIX}{url_hash}.html"

# --- Hauptlogik ---
print("Skript gestartet: Generiere Favicon-Seiten...")

try:
    with open(TEMPLATE_FILE, 'r') as f:
        template_content = f.read()
    print(f"Vorlage '{TEMPLATE_FILE}' gelesen.")
except FileNotFoundError:
    print(f"FEHLER: Vorlagendatei '{TEMPLATE_FILE}' nicht gefunden!")
    exit(1)

try:
    with open(LIST_FILE, 'r') as f:
        icon_urls = [line.strip() for line in f if line.strip()]
    print(f"Liste '{LIST_FILE}' gelesen mit {len(icon_urls)} URLs.")
except FileNotFoundError:
    print(f"FEHLER: Listendatei '{LIST_FILE}' nicht gefunden!")
    exit(1)

existing_files = get_existing_pages(OUTPUT_DIR, GENERATED_PAGES_PREFIX)
print(f"{len(existing_files)} bereits generierte Seiten gefunden.")

new_pages_created = 0
for url in icon_urls:
    output_filename = create_page_filename(url)

    if output_filename not in existing_files:
        print(f"Generiere neue Seite für: {url} -> {output_filename}")
        page_content = template_content.replace('%%ICON_URL%%', url)

        try:
            with open(os.path.join(OUTPUT_DIR, output_filename), 'w') as f:
                f.write(page_content)
            new_pages_created += 1
        except Exception as e:
             print(f"FEHLER beim Schreiben von {output_filename}: {e}")
    # else:
    #     print(f"Seite {output_filename} existiert bereits für URL: {url}") # Optional: zum Debuggen

print(f"Skript beendet. {new_pages_created} neue Seiten erstellt.")

# Wichtig für GitHub Actions, um zu wissen, ob Änderungen gemacht wurden
# Gibt eine Variable aus, die im Workflow verwendet werden kann (optional, aber sauber)
print(f"::set-output name=new_pages_count::{new_pages_created}")
