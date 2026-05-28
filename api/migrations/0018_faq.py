from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('api', '0017_donnees_configsite')]
    operations = [
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=400)),
                ('reponse', models.TextField()),
                ('categorie', models.CharField(blank=True, default='Général', max_length=100)),
                ('ordre', models.PositiveIntegerField(default=0)),
                ('actif', models.BooleanField(default=True)),
            ],
            options={'verbose_name': 'FAQ', 'ordering': ['ordre']},
        ),
    ]
