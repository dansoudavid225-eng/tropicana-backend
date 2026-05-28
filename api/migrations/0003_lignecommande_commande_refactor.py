"""
Migration 0003 — Refactorisation Commande :
- Ajout de LigneCommande (multi-produits)
- Suppression des champs mono-produit (produit, quantite, prix_unitaire) de Commande
- Ajout de total sur Commande
"""
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def migrate_commandes_existantes(apps, schema_editor):
    """Transforme chaque ancienne commande mono-produit en LigneCommande."""
    Commande      = apps.get_model('api', 'Commande')
    LigneCommande = apps.get_model('api', 'LigneCommande')

    for commande in Commande.objects.all():
        if commande.produit_id and commande.quantite and commande.prix_unitaire:
            LigneCommande.objects.create(
                commande=commande,
                produit_id=commande.produit_id,
                quantite=commande.quantite,
                prix_unitaire=commande.prix_unitaire,
            )
            commande.total = commande.prix_unitaire * commande.quantite
            commande.save(update_fields=['total'])


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_video_temoignages_google_auth'),
    ]

    operations = [
        # 1. Ajouter le champ total sur Commande
        migrations.AddField(
            model_name='commande',
            name='total',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=12),
        ),

        # 2. Créer le modèle LigneCommande
        migrations.CreateModel(
            name='LigneCommande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True,
                                           serialize=False, verbose_name='ID')),
                ('quantite',      models.PositiveIntegerField(default=1)),
                ('prix_unitaire', models.DecimalField(decimal_places=0, max_digits=10)),
                ('commande', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='lignes',
                    to='api.commande',
                )),
                ('produit', models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    to='api.produit',
                )),
            ],
            options={
                'verbose_name': 'Ligne de commande',
            },
        ),

        # 3. Migrer les données existantes
        migrations.RunPython(
            code=migrate_commandes_existantes,
            reverse_code=migrations.RunPython.noop,
        ),

        # 4. Supprimer les anciens champs mono-produit de Commande
        migrations.RemoveField(model_name='commande', name='produit'),
        migrations.RemoveField(model_name='commande', name='quantite'),
        migrations.RemoveField(model_name='commande', name='prix_unitaire'),
    ]
