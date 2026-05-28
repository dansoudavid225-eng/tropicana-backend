from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_codepromo_commande_code_promo'),
    ]

    operations = [

        # ── HistoriqueCommande ────────────────────────────────────────────
        migrations.CreateModel(
            name='HistoriqueCommande',
            fields=[
                ('id',             models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('ancien_statut',  models.CharField(blank=True, max_length=20)),
                ('nouveau_statut', models.CharField(max_length=20)),
                ('note',           models.TextField(blank=True)),
                ('date',           models.DateTimeField(auto_now_add=True)),
                ('commande',       models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historique', to='api.commande')),
                ('modifie_par',    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.utilisateur')),
            ],
            options={'verbose_name': 'Historique commande', 'verbose_name_plural': 'Historiques commandes', 'ordering': ['-date']},
        ),

        # ── ZoneLivraison ─────────────────────────────────────────────────
        migrations.CreateModel(
            name='ZoneLivraison',
            fields=[
                ('id',          models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('ville',       models.CharField(max_length=100, unique=True)),
                ('prix',        models.DecimalField(decimal_places=0, default=0, max_digits=8)),
                ('delai',       models.CharField(default='24-48h', max_length=100)),
                ('disponible',  models.BooleanField(default=True)),
                ('ordre',       models.PositiveIntegerField(default=0)),
            ],
            options={'verbose_name': 'Zone de livraison', 'verbose_name_plural': 'Zones de livraison', 'ordering': ['ordre', 'ville']},
        ),

        # ── Blacklist ─────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Blacklist',
            fields=[
                ('id',             models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('type_blacklist', models.CharField(max_length=10, choices=[('email', 'Email'), ('ip', 'Adresse IP')])),
                ('valeur',         models.CharField(max_length=255, unique=True)),
                ('raison',         models.CharField(blank=True, max_length=255)),
                ('date_ajout',     models.DateTimeField(auto_now_add=True)),
                ('ajoute_par',     models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.utilisateur')),
            ],
            options={'verbose_name': 'Blacklist', 'verbose_name_plural': 'Blacklist', 'ordering': ['-date_ajout']},
        ),

        # ── ReponseAvis ───────────────────────────────────────────────────
        migrations.CreateModel(
            name='ReponseAvis',
            fields=[
                ('id',          models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('texte',       models.TextField()),
                ('date',        models.DateTimeField(auto_now_add=True)),
                ('modifie_par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.utilisateur')),
                ('temoignage',  models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reponse', to='api.temoignage')),
            ],
            options={'verbose_name': 'Réponse avis', 'verbose_name_plural': 'Réponses avis'},
        ),

        # ── AlerteStock ───────────────────────────────────────────────────
        migrations.CreateModel(
            name='AlerteStock',
            fields=[
                ('id',              models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('seuil',           models.PositiveIntegerField(default=5)),
                ('email_alerte',    models.EmailField(blank=True)),
                ('derniere_alerte', models.DateTimeField(blank=True, null=True)),
                ('produit',         models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='alerte_stock', to='api.produit')),
            ],
            options={'verbose_name': 'Alerte stock', 'verbose_name_plural': 'Alertes stock'},
        ),

        # ── Données initiales zones de livraison ──────────────────────────
        migrations.RunPython(
            lambda apps, se: apps.get_model('api', 'ZoneLivraison').objects.bulk_create([
                apps.get_model('api', 'ZoneLivraison')(ville='Cotonou',        prix=1000, delai='Même jour',  disponible=True, ordre=1),
                apps.get_model('api', 'ZoneLivraison')(ville='Porto-Novo',     prix=1000, delai='24h',        disponible=True, ordre=2),
                apps.get_model('api', 'ZoneLivraison')(ville='Abomey-Calavi',  prix=1500, delai='24h',        disponible=True, ordre=3),
                apps.get_model('api', 'ZoneLivraison')(ville='Parakou',        prix=3000, delai='48-72h',     disponible=True, ordre=4),
                apps.get_model('api', 'ZoneLivraison')(ville='Bohicon',        prix=2000, delai='24-48h',     disponible=True, ordre=5),
                apps.get_model('api', 'ZoneLivraison')(ville='Natitingou',     prix=4000, delai='48-72h',     disponible=True, ordre=6),
                apps.get_model('api', 'ZoneLivraison')(ville='Kandi',          prix=4500, delai='48-72h',     disponible=True, ordre=7),
                apps.get_model('api', 'ZoneLivraison')(ville='Lokossa',        prix=2500, delai='24-48h',     disponible=True, ordre=8),
                apps.get_model('api', 'ZoneLivraison')(ville='Ouidah',         prix=1500, delai='24h',        disponible=True, ordre=9),
                apps.get_model('api', 'ZoneLivraison')(ville='Abomey',         prix=2500, delai='24-48h',     disponible=True, ordre=10),
            ]),
            migrations.RunPython.noop
        ),
    ]
