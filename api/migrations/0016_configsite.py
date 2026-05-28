from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('api', '0015_configaccueil_slogan_heures')]

    operations = [
        migrations.CreateModel(
            name='ConfigSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('telephone', models.CharField(default='+229 01 95 96 77 62', max_length=50)),
                ('telephone_raw', models.CharField(default='+2290195967762', max_length=50)),
                ('email', models.EmailField(default='tropicanapiopio@gmail.com')),
                ('adresse', models.CharField(default='Oganla Gare Nord, Porto-Novo, Bénin', max_length=300)),
                ('description_footer', models.TextField(default='Thé 100% naturel à base de verveine blanche citronnée. Cultivé et produit à Porto-Novo, Bénin.')),
                ('tiktok_url', models.URLField(blank=True, default='https://www.tiktok.com/@thepio08')),
                ('facebook_url', models.URLField(blank=True, default='https://facebook.com/profile.php?id=61569744814995')),
                ('paiements', models.CharField(default='MTN Money,Moov Money,Wave,Orange', max_length=500)),
                ('prix_affiche', models.CharField(default='dès 2 500 FCFA', max_length=100)),
                ('prix_mini', models.CharField(default='1 000 FCFA', max_length=100)),
                ('argument1_icone', models.CharField(default='🌱', max_length=10)),
                ('argument1_titre', models.CharField(default='100 % Bio', max_length=100)),
                ('argument1_sous', models.CharField(default='Sans engrais ni herbicides', max_length=200)),
                ('argument2_icone', models.CharField(default='🔬', max_length=10)),
                ('argument2_titre', models.CharField(default='Fondé sur la science', max_length=100)),
                ('argument2_sous', models.CharField(default='Formulé par un vétérinaire', max_length=200)),
                ('argument3_icone', models.CharField(default='👨\u200d👩\u200d👧', max_length=10)),
                ('argument3_titre', models.CharField(default='Toute la famille', max_length=100)),
                ('argument3_sous', models.CharField(default='Recommandé dès 2 ans', max_length=200)),
                ('argument4_icone', models.CharField(default='🇧🇯', max_length=10)),
                ('argument4_titre', models.CharField(default='Made in Bénin', max_length=100)),
                ('argument4_sous', models.CharField(default='Livraison nationale', max_length=200)),
                ('stat1_num', models.CharField(default='500+', max_length=50)),
                ('stat1_label', models.CharField(default='Familles béninoises satisfaites', max_length=200)),
                ('stat1_icone', models.CharField(default='👨\u200d👩\u200d👧\u200d👦', max_length=10)),
                ('stat1_desc', models.CharField(default='Partout au Bénin', max_length=200)),
                ('stat2_num', models.CharField(default='100%', max_length=50)),
                ('stat2_label', models.CharField(default='Bio, zéro additif', max_length=200)),
                ('stat2_icone', models.CharField(default='🌱', max_length=10)),
                ('stat2_desc', models.CharField(default='Sans engrais ni herbicide', max_length=200)),
                ('stat3_num', models.CharField(default='Dès 2 ans', max_length=50)),
                ('stat3_label', models.CharField(default='Pour toute la famille', max_length=200)),
                ('stat3_icone', models.CharField(default='👶', max_length=10)),
                ('stat3_desc', models.CharField(default='Enfants, adultes, seniors', max_length=200)),
                ('stat4_num', models.CharField(default='24h', max_length=50)),
                ('stat4_label', models.CharField(default='Délai de livraison', max_length=200)),
                ('stat4_icone', models.CharField(default='📦', max_length=10)),
                ('stat4_desc', models.CharField(default='Partout au Bénin', max_length=200)),
            ],
            options={'verbose_name': 'Configuration Globale du Site'},
        ),
    ]
