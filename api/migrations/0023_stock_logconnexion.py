from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_supprimer_autres_produits'),
    ]

    operations = [
        # ✅ Champ stock sur Produit
        migrations.AddField(
            model_name='produit',
            name='stock',
            field=models.PositiveIntegerField(default=0, help_text='0 = stock illimité'),
        ),
        # ✅ Modèle LogConnexion
        migrations.CreateModel(
            name='LogConnexion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(db_index=True)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True)),
                ('resultat', models.CharField(choices=[('succes', 'Succès'), ('echec', 'Échec'), ('bloque', 'Bloqué (throttle)')], max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Log connexion',
                'verbose_name_plural': 'Logs connexions',
                'ordering': ['-date'],
            },
        ),
        migrations.AddIndex(
            model_name='logconnexion',
            index=models.Index(fields=['email', 'date'], name='api_logconn_email_date_idx'),
        ),
    ]
