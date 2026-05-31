# Migration initiale — générée pour la production PostgreSQL
# Crée toutes les tables en une seule fois sans conflits
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [

        # ── Utilisateur ───────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id',            models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('password',      models.CharField(max_length=128, verbose_name='password')),
                ('last_login',    models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser',  models.BooleanField(default=False)),
                ('email',         models.EmailField(max_length=254, unique=True)),
                ('prenom',        models.CharField(max_length=100)),
                ('nom',           models.CharField(max_length=100)),
                ('telephone',     models.CharField(blank=True, max_length=20)),
                ('ville',         models.CharField(blank=True, max_length=100)),
                ('is_active',     models.BooleanField(default=True)),
                ('is_staff',      models.BooleanField(default=False)),
                ('date_inscription', models.DateTimeField(default=django.utils.timezone.now)),
                ('google_id',        models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('photo_url',        models.URLField(blank=True, null=True)),
                ('groups',        models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={'verbose_name': 'Utilisateur', 'verbose_name_plural': 'Utilisateurs', 'ordering': ['-date_inscription']},
        ),

        # ── Produit ───────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id',           models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nom',          models.CharField(max_length=200)),
                ('slug',         models.SlugField(max_length=200, unique=True)),
                ('description',  models.TextField(blank=True)),
                ('prix',         models.DecimalField(decimal_places=0, max_digits=10)),
                ('image',        models.ImageField(blank=True, null=True, upload_to='produits/')),
                ('unite',        models.CharField(blank=True, max_length=50)),
                ('badge',        models.CharField(blank=True, max_length=100)),
                ('disponible',   models.BooleanField(default=True)),
                ('stock',        models.PositiveIntegerField(default=0)),
                ('quantite_min', models.PositiveIntegerField(default=1)),
                ('ordre',        models.PositiveIntegerField(default=0)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'Produit', 'verbose_name_plural': 'Produits', 'ordering': ['ordre', 'nom']},
        ),

        # ── Commande ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id',               models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nom_client',       models.CharField(max_length=200)),
                ('email_client',     models.EmailField()),
                ('telephone_client', models.CharField(max_length=20)),
                ('ville_livraison',  models.CharField(max_length=100)),
                ('adresse_livraison', models.TextField(blank=True)),
                ('mode_paiement',    models.CharField(max_length=20, default='livraison',
                    choices=[('livraison','Paiement à la livraison'),('mobile_money','Mobile Money'),('fedapay','Fedapay (carte / mobile)')])),
                ('statut',           models.CharField(max_length=20, default='en_attente',
                    choices=[('en_attente','En attente'),('confirmee','Confirmee'),('en_livraison','En livraison'),('livree','Livree'),('annulee','Annulee')])),
                ('notes',            models.TextField(blank=True)),
                ('total',            models.DecimalField(decimal_places=0, default=0, max_digits=12)),
                ('fedapay_ref',      models.CharField(blank=True, max_length=100)),
                ('payee',            models.BooleanField(default=False)),
                ('code_promo',       models.CharField(blank=True, max_length=50)),
                ('date_commande',    models.DateTimeField(auto_now_add=True)),
                ('utilisateur',      models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='commandes', to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Commande', 'verbose_name_plural': 'Commandes', 'ordering': ['-date_commande']},
        ),

        # ── LigneCommande ─────────────────────────────────────────────────────
        migrations.CreateModel(
            name='LigneCommande',
            fields=[
                ('id',           models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('quantite',     models.PositiveIntegerField(default=1)),
                ('prix_unitaire', models.DecimalField(decimal_places=0, max_digits=10)),
                ('commande',     models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lignes', to='api.commande')),
                ('produit',      models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.produit')),
            ],
            options={'verbose_name': 'Ligne de commande', 'verbose_name_plural': 'Lignes de commande'},
        ),

        # ── Temoignage ────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Temoignage',
            fields=[
                ('id',           models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nom',          models.CharField(max_length=100)),
                ('email',        models.EmailField(blank=True)),
                ('ville',        models.CharField(blank=True, max_length=100)),
                ('note',         models.PositiveIntegerField(default=5)),
                ('commentaire',  models.TextField()),
                ('approuve',     models.BooleanField(default=False)),
                ('image',        models.ImageField(blank=True, null=True, upload_to='temoignages/')),
                ('video_url',    models.URLField(blank=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('utilisateur',  models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Témoignage', 'verbose_name_plural': 'Témoignages', 'ordering': ['-date_creation']},
        ),

        # ── MessageContact ────────────────────────────────────────────────────
        migrations.CreateModel(
            name='MessageContact',
            fields=[
                ('id',        models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nom',       models.CharField(max_length=100)),
                ('email',     models.EmailField()),
                ('telephone', models.CharField(blank=True, max_length=20)),
                ('sujet',     models.CharField(max_length=200, blank=True)),
                ('message',   models.TextField()),
                ('lu',        models.BooleanField(default=False)),
                ('date_envoi', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'Message de contact', 'verbose_name_plural': 'Messages de contact', 'ordering': ['-date_envoi']},
        ),

        # ── NewsletterAbonne ──────────────────────────────────────────────────
        migrations.CreateModel(
            name='NewsletterAbonne',
            fields=[
                ('id',               models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('email',            models.EmailField(unique=True)),
                ('actif',            models.BooleanField(default=True)),
                ('date_inscription', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'Abonné newsletter', 'verbose_name_plural': 'Abonnés newsletter'},
        ),

        # ── ResetPasswordToken ────────────────────────────────────────────────
        migrations.CreateModel(
            name='ResetPasswordToken',
            fields=[
                ('id',         models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('token',      models.CharField(max_length=100, unique=True)),
                ('expire_a',   models.DateTimeField()),
                ('utilise',    models.BooleanField(default=False)),
                ('utilisateur', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),

        # ── PanierSauvegarde ──────────────────────────────────────────────────
        migrations.CreateModel(
            name='PanierSauvegarde',
            fields=[
                ('id',       models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('donnees',  models.JSONField(default=dict)),
                ('mis_a_jour', models.DateTimeField(auto_now=True)),
                ('utilisateur', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='panier', to=settings.AUTH_USER_MODEL)),
            ],
        ),

        # ── LogConnexion ──────────────────────────────────────────────────────
        migrations.CreateModel(
            name='LogConnexion',
            fields=[
                ('id',         models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('email',      models.CharField(max_length=254)),
                ('ip',         models.GenericIPAddressField(null=True, blank=True)),
                ('resultat',   models.CharField(max_length=10, choices=[('succes','Succès'),('echec','Échec')])),
                ('user_agent', models.CharField(blank=True, max_length=255)),
                ('date',       models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'Log connexion', 'verbose_name_plural': 'Logs connexion', 'ordering': ['-date']},
        ),

        # ── Slider ────────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id',       models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('titre',    models.CharField(max_length=200)),
                ('sous_titre', models.CharField(blank=True, max_length=300)),
                ('image',    models.ImageField(blank=True, null=True, upload_to='slider/')),
                ('lien',     models.CharField(blank=True, max_length=200)),
                ('actif',    models.BooleanField(default=True)),
                ('ordre',    models.PositiveIntegerField(default=0)),
            ],
            options={'verbose_name': 'Slide', 'ordering': ['ordre']},
        ),

        # ── Bienfait ──────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Bienfait',
            fields=[
                ('id',          models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('icone',       models.CharField(max_length=10, blank=True)),
                ('titre',       models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('actif',       models.BooleanField(default=True)),
                ('ordre',       models.PositiveIntegerField(default=0)),
            ],
            options={'verbose_name': 'Bienfait', 'ordering': ['ordre']},
        ),

        # ── Partenaire ────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Partenaire',
            fields=[
                ('id',    models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nom',   models.CharField(max_length=200)),
                ('logo',  models.ImageField(blank=True, null=True, upload_to='partenaires/')),
                ('site',  models.URLField(blank=True)),
                ('actif', models.BooleanField(default=True)),
                ('ordre', models.PositiveIntegerField(default=0)),
            ],
            options={'verbose_name': 'Partenaire', 'ordering': ['ordre']},
        ),

        # ── HistoireChapitre ──────────────────────────────────────────────────
        migrations.CreateModel(
            name='HistoireChapitre',
            fields=[
                ('id',          models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('titre',       models.CharField(max_length=200)),
                ('contenu',     models.TextField()),
                ('image',       models.ImageField(blank=True, null=True, upload_to='histoire/')),
                ('actif',       models.BooleanField(default=True)),
                ('ordre',       models.PositiveIntegerField(default=0)),
            ],
            options={'verbose_name': 'Chapitre histoire', 'ordering': ['ordre']},
        ),

        # ── ArticleBlog ───────────────────────────────────────────────────────
        migrations.CreateModel(
            name='ArticleBlog',
            fields=[
                ('id',               models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('titre',            models.CharField(max_length=300)),
                ('slug',             models.SlugField(max_length=300, unique=True)),
                ('contenu',          models.TextField()),
                ('extrait',          models.TextField(blank=True)),
                ('image',            models.ImageField(blank=True, null=True, upload_to='blog/')),
                ('publie',           models.BooleanField(default=False)),
                ('date_publication', models.DateTimeField(auto_now_add=True)),
                ('auteur',           models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Article blog', 'ordering': ['-date_publication']},
        ),

        # ── Mission ───────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id',          models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('icone',       models.CharField(blank=True, max_length=10)),
                ('titre',       models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('actif',       models.BooleanField(default=True)),
                ('ordre',       models.PositiveIntegerField(default=0)),
            ],
            options={'verbose_name': 'Mission', 'ordering': ['ordre']},
        ),

        # ── FondateurConfig ───────────────────────────────────────────────────
        migrations.CreateModel(
            name='FondateurConfig',
            fields=[
                ('id',          models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nom',         models.CharField(default='', max_length=200)),
                ('titre',       models.CharField(default='', max_length=200)),
                ('citation',    models.TextField(blank=True)),
                ('biographie',  models.TextField(blank=True)),
                ('photo',       models.ImageField(blank=True, null=True, upload_to='fondateur/')),
            ],
            options={'verbose_name': 'Config Fondateur'},
        ),

        # ── ConfigAccueil ─────────────────────────────────────────────────────
        migrations.CreateModel(
            name='ConfigAccueil',
            fields=[
                ('id',              models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('hero_titre',      models.CharField(blank=True, max_length=300)),
                ('hero_sous_titre', models.TextField(blank=True)),
                ('hero_bouton',     models.CharField(blank=True, max_length=100)),
                ('hero_image',      models.ImageField(blank=True, null=True, upload_to='accueil/')),
                ('slogan',          models.CharField(blank=True, max_length=300)),
                ('heures_ouverture', models.CharField(blank=True, max_length=200)),
                ('section_produits_titre', models.CharField(blank=True, max_length=200)),
                ('section_bienfaits_titre', models.CharField(blank=True, max_length=200)),
                ('section_temoignages_titre', models.CharField(blank=True, max_length=200)),
            ],
            options={'verbose_name': 'Config Accueil'},
        ),

        # ── ConfigSite ────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='ConfigSite',
            fields=[
                ('id',              models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nom_site',        models.CharField(default='Tropicana Pio Pio', max_length=100)),
                ('slogan',          models.CharField(blank=True, max_length=300)),
                ('email_contact',   models.EmailField(blank=True)),
                ('telephone',       models.CharField(blank=True, max_length=20)),
                ('adresse',         models.TextField(blank=True)),
                ('facebook',        models.URLField(blank=True)),
                ('instagram',       models.URLField(blank=True)),
                ('whatsapp',        models.CharField(blank=True, max_length=20)),
                ('couleur_primaire', models.CharField(default='#2D6A4F', max_length=7)),
                ('couleur_secondaire', models.CharField(default='#F4A261', max_length=7)),
                ('meta_description', models.TextField(blank=True)),
            ],
            options={'verbose_name': 'Config Site'},
        ),

        # ── FAQ ───────────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id',       models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=300)),
                ('reponse',  models.TextField()),
                ('actif',    models.BooleanField(default=True)),
                ('ordre',    models.PositiveIntegerField(default=0)),
            ],
            options={'verbose_name': 'FAQ', 'ordering': ['ordre']},
        ),

        # ── CodePromo ─────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='CodePromo',
            fields=[
                ('id',                models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('code',              models.CharField(max_length=50, unique=True)),
                ('type_reduction',    models.CharField(max_length=20, choices=[('pourcentage','Pourcentage (%)'),('fixe','Montant fixe (FCFA)')], default='pourcentage')),
                ('valeur',            models.DecimalField(decimal_places=0, max_digits=10)),
                ('limite_utilisations', models.PositiveIntegerField(blank=True, null=True)),
                ('nb_utilisations',   models.PositiveIntegerField(default=0)),
                ('date_expiration',   models.DateTimeField(blank=True, null=True)),
                ('actif',             models.BooleanField(default=True)),
                ('date_creation',     models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'Code Promo', 'ordering': ['-date_creation']},
        ),

        # ── ZoneLivraison ─────────────────────────────────────────────────────
        migrations.CreateModel(
            name='ZoneLivraison',
            fields=[
                ('id',         models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('ville',      models.CharField(max_length=100, unique=True)),
                ('prix',       models.DecimalField(decimal_places=0, default=0, max_digits=8)),
                ('delai',      models.CharField(default='24-48h', max_length=100)),
                ('disponible', models.BooleanField(default=True)),
                ('ordre',      models.PositiveIntegerField(default=0)),
            ],
            options={'verbose_name': 'Zone de livraison', 'ordering': ['ordre', 'ville']},
        ),

        # ── Blacklist ─────────────────────────────────────────────────────────
        migrations.CreateModel(
            name='Blacklist',
            fields=[
                ('id',             models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('type_blacklist', models.CharField(max_length=10, choices=[('email','Email'),('ip','Adresse IP')])),
                ('valeur',         models.CharField(max_length=255, unique=True)),
                ('raison',         models.CharField(blank=True, max_length=255)),
                ('date_ajout',     models.DateTimeField(auto_now_add=True)),
                ('ajoute_par',     models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Blacklist', 'ordering': ['-date_ajout']},
        ),

        # ── HistoriqueCommande ────────────────────────────────────────────────
        migrations.CreateModel(
            name='HistoriqueCommande',
            fields=[
                ('id',             models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('ancien_statut',  models.CharField(blank=True, max_length=20)),
                ('nouveau_statut', models.CharField(max_length=20)),
                ('note',           models.TextField(blank=True)),
                ('date',           models.DateTimeField(auto_now_add=True)),
                ('commande',       models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historique', to='api.commande')),
                ('modifie_par',    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'verbose_name': 'Historique commande', 'ordering': ['-date']},
        ),

        # ── ReponseAvis ───────────────────────────────────────────────────────
        migrations.CreateModel(
            name='ReponseAvis',
            fields=[
                ('id',          models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('texte',       models.TextField()),
                ('date',        models.DateTimeField(auto_now_add=True)),
                ('modifie_par', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('temoignage',  models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='reponse', to='api.temoignage')),
            ],
            options={'verbose_name': 'Réponse avis'},
        ),

        # ── AlerteStock ───────────────────────────────────────────────────────
        migrations.CreateModel(
            name='AlerteStock',
            fields=[
                ('id',              models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('seuil',           models.PositiveIntegerField(default=5)),
                ('email_alerte',    models.EmailField(blank=True)),
                ('derniere_alerte', models.DateTimeField(blank=True, null=True)),
                ('produit',         models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='alerte_stock', to='api.produit')),
            ],
            options={'verbose_name': 'Alerte stock'},
        ),
    ]
