from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_force_configsite_columns'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteContentConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donnees', models.JSONField(blank=True, default=dict)),
                ('date_maj', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Contenu du site (éditorial)',
                'verbose_name_plural': 'Contenu du site (éditorial)',
            },
        ),
    ]
