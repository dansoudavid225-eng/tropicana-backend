from django.db import migrations, models


def creer_sachet_unitaire(apps, schema_editor):
    Produit = apps.get_model('api', 'Produit')
    Produit.objects.get_or_create(
        slug='the-pio-pio-sachet-unitaire',
        defaults={
            'nom':         'Sachet unitaire Thé Pio Pio',
            'description': (
                'Découvrez le Thé Pio Pio — votre allié bien-être au quotidien. '
                'Ingrédient phare : la verveine blanche citronnée, reconnue pour ses vertus relaxantes, '
                'nettoyante naturelle des artères, riche en vitamine K essentielle pour votre équilibre interne. '
                'Commande minimale : 6 sachets.'
            ),
            'prix':         100,
            'unite':        'sachet',
            'badge':        '🌿 Nouveau produit',
            'image':        '',
            'disponible':   True,
            'stock':        0,
            'quantite_min': 6,
        }
    )


def supprimer_sachet_unitaire(apps, schema_editor):
    Produit = apps.get_model('api', 'Produit')
    Produit.objects.filter(slug='the-pio-pio-sachet-unitaire').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_commande_fedapay'),
    ]

    operations = [
        # 1. Ajouter le champ quantite_min
        migrations.AddField(
            model_name='produit',
            name='quantite_min',
            field=models.PositiveIntegerField(
                default=1,
                help_text='Quantité minimale de commande',
            ),
        ),
        # 2. Créer le produit sachet unitaire
        migrations.RunPython(creer_sachet_unitaire, supprimer_sachet_unitaire),
    ]
