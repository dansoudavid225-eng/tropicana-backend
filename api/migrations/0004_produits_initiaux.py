from django.db import migrations

PRODUITS = [
    {
        'nom': 'Thé Pio Pio — Boîte 30 sachets',
        'slug': 'the-pio-pio-boite-30',
        'description': 'Notre boîte phare : 30 sachets de verveine blanche citronnée 100 % bio, cultivée sans engrais ni herbicides à Porto-Novo. Idéal pour un mois de bien-être. Recommandé pour toute la famille dès 2 ans. Favorise la circulation sanguine, le sommeil profond et la digestion douce.',
        'prix': 5000,
        'unite': 'boîte de 30 sachets',
        'badge': '⭐ Le plus populaire',
        'disponible': True,
    },
    {
        'nom': 'Thé Pio Pio — Boîte 15 sachets',
        'slug': 'the-pio-pio-boite-15',
        'description': 'La boîte découverte : 15 sachets pour découvrir les vertus de la verveine blanche citronnée Pio Pio. Parfaite pour commencer votre cure ou offrir. Cultivé au Bénin, sans additifs ni colorants.',
        'prix': 3000,
        'unite': 'boîte de 15 sachets',
        'badge': '🎁 Idéal pour débuter',
        'disponible': True,
    },
    {
        'nom': 'Thé Pio Pio — Vrac 100g',
        'slug': 'the-pio-pio-vrac-100g',
        'description': 'Pour les amateurs de thé en vrac : 100g de feuilles séchées de verveine blanche citronnée. Dosez à votre goût, infusez 5 à 8 minutes dans de l\'eau à 85°C. Arôme frais et citronné naturel.',
        'prix': 2500,
        'unite': '100g vrac',
        'badge': '',
        'disponible': True,
    },
]

def ajouter_produits(apps, schema_editor):
    Produit = apps.get_model('api', 'Produit')
    for p in PRODUITS:
        if not Produit.objects.filter(slug=p['slug']).exists():
            Produit.objects.create(**p)

def supprimer_produits(apps, schema_editor):
    Produit = apps.get_model('api', 'Produit')
    for p in PRODUITS:
        Produit.objects.filter(slug=p['slug']).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_lignecommande_commande_refactor'),
    ]

    operations = [
        migrations.RunPython(ajouter_produits, supprimer_produits),
    ]
