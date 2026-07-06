import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tropicana_backend.settings')
django.setup()

from api.models import Temoignage

temoignages = [
    {'nom': 'Agnès M.',    'ville': 'Cotonou',    'note': 5, 'texte': "Depuis que je bois le Thé Pio Pio chaque soir, je dors beaucoup mieux. Je le recommande à toute ma famille."},
    {'nom': 'Kofi D.',     'ville': 'Porto-Novo', 'note': 5, 'texte': "Mes douleurs aux articulations ont vraiment diminué après 3 semaines. Produit naturel et vraiment efficace."},
    {'nom': 'Rachel B.',   'ville': 'Parakou',    'note': 5, 'texte': "Je l'ai commandé pour ma mère âgée. Elle dit que son énergie est revenue. Merci Tropicana Pio Pio !"},
    {'nom': 'Mariam K.',   'ville': 'Cotonou',    'note': 5, 'texte': "Un thé exceptionnel ! Mon transit intestinal s'est amélioré dès la première semaine."},
    {'nom': 'Faustin D.',  'ville': 'Porto-Novo', 'note': 5, 'texte': "Je le donne à mes enfants depuis 3 mois. Moins de maladies fréquentes, ils sont en pleine forme !"},
    {'nom': 'Rachelle A.', 'ville': 'Parakou',    'note': 5, 'texte': "Je revends le Thé Pio Pio dans ma boutique. Mes clients adorent et reviennent toujours commander."},
]

for t in temoignages:
    Temoignage.objects.create(**t, type_video='aucune', approuve=True)

print('Temoignages:', Temoignage.objects.count())
for t in Temoignage.objects.all():
    print(f'  - {t.nom} ({t.ville})')
