from django.db import migrations

PRODUITS = [
    {
        'nom': 'Sachet unitaire',
        'slug': 'the-pio-pio-sachet-1',
        'description': 'Un sachet de thé Pio Pio pour découvrir nos saveurs naturelles. Idéal pour une première dégustation ou un moment de calme bien mérité.',
        'prix': 1000,
        'unite': 'sachet',
        'badge': '🏪 En boutique',
        'disponible': True,
        'stock': 0,
    },
    {
        'nom': 'Boîte 15 sachets',
        'slug': 'the-pio-pio-boite-15',
        'description': 'Une boîte de 15 sachets de thé Pio Pio aux plantes africaines. Parfaite pour débuter une cure ou offrir en cadeau.',
        'prix': 3000,
        'unite': 'boîte',
        'badge': '🎁 Idéal pour débuter',
        'disponible': True,
        'stock': 0,
    },
    {
        'nom': 'Boîte 30 sachets',
        'slug': 'the-pio-pio-boite-30',
        'description': "Notre boîte phare : 30 sachets de thé naturel pour une cure complète d'un mois. Le meilleur rapport qualité-prix.",
        'prix': 5000,
        'unite': 'boîte',
        'badge': '⭐ Le plus populaire',
        'disponible': True,
        'stock': 0,
    },
    {
        'nom': 'Vrac 100g',
        'slug': 'the-pio-pio-vrac-100g',
        'description': "Thé Pio Pio en vrac, 100g. Pour les amateurs qui aiment doser librement et profiter d'un thé plus concentré.",
        'prix': 2500,
        'unite': '100g',
        'badge': '🌿 Vrac naturel',
        'disponible': True,
        'stock': 0,
    },
    {
        'nom': 'Pack Famille',
        'slug': 'the-pio-pio-pack-famille',
        'description': 'Le pack idéal pour toute la famille : 3 boîtes de 30 sachets à prix réduit. Profitez des bienfaits du thé Pio Pio ensemble.',
        'prix': 12000,
        'unite': 'pack',
        'badge': '👨‍👩‍👧 Pack famille',
        'disponible': True,
        'stock': 0,
    },
]


def creer_produits(apps, schema_editor):
    Produit = apps.get_model('api', 'Produit')
    # Supprimer les anciens produits hors liste
    slugs = [p['slug'] for p in PRODUITS]
    Produit.objects.exclude(slug__in=slugs).delete()
    # Créer ou mettre à jour chaque produit
    for p in PRODUITS:
        defaults = {k: v for k, v in p.items() if k != 'slug'}
        obj, created = Produit.objects.get_or_create(slug=p['slug'], defaults=defaults)
        if not created:
            for champ, valeur in defaults.items():
                setattr(obj, champ, valeur)
            obj.save()


def restaurer(apps, schema_editor):
    pass  # Irréversible


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_paniersauvegarde'),
    ]

    operations = [
        migrations.RunPython(creer_produits, restaurer),
    ]
