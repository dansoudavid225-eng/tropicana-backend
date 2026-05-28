from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0012_donnees_slider_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='ConfigAccueil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('tasse_label', models.CharField(default='Un moment rien que pour vous', max_length=200)),
                ('tasse_citation', models.TextField(default="Redécouvrez le plaisir d'un moment de calme")),
                ('tasse_bouton', models.CharField(default='Commander maintenant', max_length=100)),
                ('tasse_lien', models.CharField(default='/boutique', max_length=200)),
                ('tasse_image', models.ImageField(blank=True, null=True, upload_to='accueil/')),
                ('cta_label', models.CharField(default='Prêt à prendre soin de vous ?', max_length=200)),
                ('cta_texte', models.TextField(default="Commandez votre Thé Pio Pio dès aujourd'hui.")),
                ('cta_bouton', models.CharField(default='Commander dès 2 500 FCFA', max_length=100)),
                ('cta_lien', models.CharField(default='/boutique', max_length=200)),
            ],
            options={'verbose_name': "Configuration Page d'accueil"},
        ),
    ]
