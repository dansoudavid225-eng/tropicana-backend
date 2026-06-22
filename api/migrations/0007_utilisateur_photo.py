from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_sitecontentconfig'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='photo',
            field=models.ImageField(blank=True, help_text='Photo de profil uploadée par le client.', null=True, upload_to='utilisateurs/photos/'),
        ),
    ]
