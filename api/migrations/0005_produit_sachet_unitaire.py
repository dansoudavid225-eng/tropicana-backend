from django.db import migrations


def ajouter_sachet_unitaire(apps, schema_editor):
    Produit = apps.get_model('api', 'Produit')
    if not Produit.objects.filter(slug='the-pio-pio-sachet-1').exists():
        Produit.objects.create(
            nom='Thé Pio Pio — Sachet unitaire',
            slug='the-pio-pio-sachet-1',
            description=(
                'Découvrez le Thé Pio Pio à la pièce ! Un sachet de verveine blanche citronnée '
                '100 % bio, cultivée sans engrais ni herbicides à Porto-Novo. Idéal pour tester '
                'nos thés ou pour une pause bien-être immédiate. Disponible en boutique.'
            ),
            prix=1000,
            unite='sachet unitaire',
            badge='🏪 En boutique',
            disponible=True,
        )


def supprimer_sachet_unitaire(apps, schema_editor):
    Produit = apps.get_model('api', 'Produit')
    Produit.objects.filter(slug='the-pio-pio-sachet-1').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_produits_initiaux'),
    ]

    operations = [
        migrations.RunPython(ajouter_sachet_unitaire, supprimer_sachet_unitaire),
    ]
