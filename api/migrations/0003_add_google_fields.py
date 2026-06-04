from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_donnees_initiales'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='google_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),

    ]
