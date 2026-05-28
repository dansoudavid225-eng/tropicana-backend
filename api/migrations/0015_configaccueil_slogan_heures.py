from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_donnees_configaccueil'),
    ]

    operations = [
        migrations.AddField(
            model_name='configaccueil',
            name='slogan',
            field=models.CharField(
                max_length=300,
                default='Un sang qui circule, une vie qui rayonne.',
                help_text='Slogan affiché en bas du footer sous le logo.',
            ),
        ),
        migrations.AddField(
            model_name='configaccueil',
            name='heures_ouverture',
            field=models.CharField(
                max_length=200,
                default='Lun – Sam : 8h00 – 18h00',
                help_text='Horaires affichés dans la colonne Contact du footer.',
            ),
        ),
    ]
