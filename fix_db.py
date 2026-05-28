#!/usr/bin/env python
"""
Répare la base SQLite : ajoute les colonnes manquantes puis applique les migrations.
Lance : python fix_db.py
"""
import os, sys, sqlite3, glob

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, '.')

# ── Trouver la base SQLite ──────────────────────────────────────────────────
candidates = glob.glob('*.sqlite3') + glob.glob('db.sqlite3') + glob.glob('**/*.sqlite3', recursive=True)
db_path = None
for c in candidates:
    if 'venv' not in c:
        db_path = c
        break

if not db_path:
    print("❌ Aucune base SQLite trouvée. Lance d'abord : python manage.py migrate")
    sys.exit(1)

print(f"✅ Base trouvée : {db_path}")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# ── Vérifier / ajouter les colonnes manquantes ─────────────────────────────
fixes = [
    ("api_commande", "fedapay_ref", "VARCHAR(100) NOT NULL DEFAULT ''"),
    ("api_commande", "payee",       "BOOL NOT NULL DEFAULT 0"),
]

for table, col, col_def in fixes:
    cur.execute(f"PRAGMA table_info({table})")
    cols = [row[1] for row in cur.fetchall()]
    if col not in cols:
        cur.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_def}")
        print(f"  ✅ Colonne ajoutée : {table}.{col}")
    else:
        print(f"  ℹ️  Déjà présente  : {table}.{col}")

conn.commit()
conn.close()

# ── Appliquer toutes les migrations en attente ────────────────────────────
print("\n⏳ Application des migrations Django...")
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tropicana_backend.settings')
django.setup()
from django.core.management import call_command
call_command('migrate', '--run-syncdb')
print("\n✅ Tout est bon ! Relance le serveur : python manage.py runserver")
