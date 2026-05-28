from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_resetpasswordtoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='PanierSauvegarde',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donnees', models.JSONField(default=dict)),
                ('mis_a_jour', models.DateTimeField(auto_now=True)),
                ('utilisateur', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='panier_sauvegarde',
                    to='api.utilisateur',
                )),
            ],
            options={
                'verbose_name': 'Panier sauvegardé',
            },
        ),
    ]
