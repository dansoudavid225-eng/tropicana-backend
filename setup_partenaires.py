"""
Script à lancer UNE SEULE FOIS pour créer les partenaires avec leurs logos.
Usage: python setup_partenaires.py

Mettre les logos dans le même dossier que ce script avant de lancer.
  - wpsa.jpeg
  - wangnigni.jpeg
  - ongrail.jpeg
  - artisan_nomade.jpeg
"""
import os, sys, django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tropicana_backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from api.models import Partenaire
from django.core.files import File

BASE = os.path.dirname(os.path.abspath(__file__))

partenaires = [
    {
        'nom':   "World's Poultry Science Association",
        'lien':  'https://wpsa.com/',
        'tag':   'Partenaire scientifique',
        'ordre': 0,
        'logo_fichier': 'wpsa.jpeg',
    },
    {
        'nom':   'Wangnigni 229',
        'lien':  'https://wangnigni229.com/',
        'tag':   'Partenaire local',
        'ordre': 1,
        'logo_fichier': 'wangnigni.jpeg',
    },
    {
        'nom':   'ONG Rail Bénin',
        'lien':  'https://ongrail.com/',
        'tag':   'Partenaire social',
        'ordre': 2,
        'logo_fichier': 'ongrail.jpeg',
    },
    {
        'nom':   'Artisan Nomade',
        'lien':  'https://www.facebook.com/profile.php?id=61563163111239',
        'tag':   'Partenaire artisanat',
        'ordre': 3,
        'logo_fichier': 'artisan_nomade.jpeg',
    },
]

for p in partenaires:
    logo_path = os.path.join(BASE, p['logo_fichier'])

    obj, created = Partenaire.objects.get_or_create(
        nom=p['nom'],
        defaults=dict(lien=p['lien'], tag=p['tag'], ordre=p['ordre'], actif=True)
    )

    if not created:
        obj.lien  = p['lien']
        obj.tag   = p['tag']
        obj.ordre = p['ordre']

    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            obj.logo.save(p['logo_fichier'], File(f), save=False)
        print(f"✅ Logo uploadé : {p['nom']}")
    else:
        print(f"⚠️  Logo non trouvé : {logo_path}  (le partenaire est créé sans logo)")

    obj.save()

print("\n✅ Tous les partenaires sont configurés !")
print("Vérifie sur : http://localhost:8000/django-admin/api/partenaire/")
