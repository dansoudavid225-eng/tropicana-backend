from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_donnees_initiales'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('icone', models.CharField(blank=True, max_length=10)),
                ('texte', models.TextField()),
                ('ordre', models.PositiveIntegerField(default=0)),
                ('actif', models.BooleanField(default=True)),
            ],
            options={'verbose_name': 'Mission', 'ordering': ['ordre']},
        ),
        migrations.CreateModel(
            name='FondateurConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('citation', models.TextField(default="Le plus grand laboratoire, c'est notre propre corps.")),
                ('nom', models.CharField(default='Felicien Prosper DURAND', max_length=200)),
                ('role', models.TextField(default='Fondateur · Vétérinaire diplômé\nSpécialiste en biologie cellulaire, Cuba')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='fondateur/')),
            ],
            options={'verbose_name': 'Configuration Fondateur'},
        ),
    ]
