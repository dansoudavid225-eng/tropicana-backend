from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_produit_sachet_unitaire'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterAbonne',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('actif', models.BooleanField(default=True)),
                ('date_inscription', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Abonné Newsletter',
                'verbose_name_plural': 'Abonnés Newsletter',
                'ordering': ['-date_inscription'],
            },
        ),
    ]
