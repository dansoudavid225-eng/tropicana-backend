from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_newsletter_abonne'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('titre', models.CharField(max_length=200)),
                ('sous_titre', models.TextField(blank=True)),
                ('image', models.ImageField(upload_to='sliders/')),
                ('lien', models.CharField(blank=True, max_length=200)),
                ('texte_bouton', models.CharField(blank=True, default='Voir plus', max_length=100)),
                ('actif', models.BooleanField(default=True)),
                ('ordre', models.PositiveIntegerField(default=0)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
            ],
            options={'verbose_name': 'Slider / Banniere', 'ordering': ['ordre']},
        ),
        migrations.CreateModel(
            name='Bienfait',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('icone', models.CharField(blank=True, max_length=10)),
                ('titre', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('ordre', models.PositiveIntegerField(default=0)),
                ('actif', models.BooleanField(default=True)),
            ],
            options={'verbose_name': 'Bienfait', 'ordering': ['ordre']},
        ),
        migrations.CreateModel(
            name='Partenaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('nom', models.CharField(max_length=200)),
                ('logo', models.ImageField(upload_to='partenaires/')),
                ('lien', models.URLField(blank=True)),
                ('tag', models.CharField(blank=True, default='Partenaire', max_length=100)),
                ('actif', models.BooleanField(default=True)),
                ('ordre', models.PositiveIntegerField(default=0)),
            ],
            options={'verbose_name': 'Partenaire', 'ordering': ['ordre']},
        ),
        migrations.CreateModel(
            name='HistoireChapitre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('numero', models.CharField(default='01', max_length=10)),
                ('titre', models.CharField(max_length=200)),
                ('texte', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='histoire/')),
                ('ordre', models.PositiveIntegerField(default=0)),
                ('actif', models.BooleanField(default=True)),
                ('date_modif', models.DateTimeField(auto_now=True)),
            ],
            options={'verbose_name': "Chapitre de l'histoire", 'ordering': ['ordre']},
        ),
        migrations.CreateModel(
            name='ArticleBlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('titre', models.CharField(max_length=300)),
                ('slug', models.SlugField(unique=True)),
                ('categorie', models.CharField(blank=True, default='Sante naturelle', max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog/')),
                ('extrait', models.TextField()),
                ('contenu', models.TextField()),
                ('temps_lecture', models.CharField(default='3 min', max_length=20)),
                ('publie', models.BooleanField(default=True)),
                ('date_publication', models.DateField()),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('date_modif', models.DateTimeField(auto_now=True)),
            ],
            options={'verbose_name': 'Article de blog', 'ordering': ['-date_publication']},
        ),
    ]
