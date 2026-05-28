from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_produits_deux_sachets_only'),
    ]

    operations = [
        # Champ code_promo dans Commande
        migrations.AddField(
            model_name='commande',
            name='code_promo',
            field=models.CharField(blank=True, max_length=50, help_text='Code promo utilisé'),
        ),

        # Nouveau modèle CodePromo
        migrations.CreateModel(
            name='CodePromo',
            fields=[
                ('id',                models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('code',              models.CharField(max_length=50, unique=True)),
                ('type_reduction',    models.CharField(max_length=20, choices=[('pourcentage', 'Pourcentage (%)'), ('fixe', 'Montant fixe (FCFA)')], default='pourcentage')),
                ('valeur',            models.DecimalField(max_digits=10, decimal_places=0)),
                ('limite_utilisations', models.PositiveIntegerField(null=True, blank=True)),
                ('nb_utilisations',   models.PositiveIntegerField(default=0)),
                ('date_expiration',   models.DateTimeField(null=True, blank=True)),
                ('actif',             models.BooleanField(default=True)),
                ('date_creation',     models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Code Promo',
                'verbose_name_plural': 'Codes Promo',
                'ordering': ['-date_creation'],
            },
        ),
    ]
