from django.db import migrations


def creer_produits(apps, schema_editor):
    Produit = apps.get_model('api', 'Produit')

    # Créer le sachet verveine citronnelle
    Produit.objects.get_or_create(
        slug='the-pio-pio-sachet-verveine',
        defaults={
            'nom':         'Thé Pio Pio — Sachet verveine citronnelle',
            'description': (
                'Le Thé Pio Pio fait à base de verveine à la citronnelle, 100% Bio. '
                'Cultivé naturellement à Porto-Novo, Bénin. Reconnu pour ses vertus relaxantes, '
                'nettoyantes des artères et riche en vitamine K. Votre allié bien-être au quotidien.'
            ),
            'prix':         1000,
            'unite':        'sachet',
            'badge':        '🌿 100% Bio',
            'image':        '',
            'disponible':   True,
            'stock':        0,
            'quantite_min': 1,
        }
    )

    # Supprimer tous les produits sauf les deux sachets
    Produit.objects.exclude(slug__in=[
        'the-pio-pio-sachet-unitaire',
        'the-pio-pio-sachet-verveine',
    ]).delete()


def restaurer(apps, schema_editor):
    Produit = apps.get_model('api', 'Produit')
    Produit.objects.filter(slug='the-pio-pio-sachet-verveine').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_produit_quantite_min_sachet_unitaire'),
    ]

    operations = [
        migrations.RunPython(creer_produits, restaurer),
    ]
