from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_donnees_faq_produits'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResetPasswordToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64, unique=True)),
                ('expire_le', models.DateTimeField()),
                ('utilise', models.BooleanField(default=False)),
                ('cree_le', models.DateTimeField(auto_now_add=True)),
                ('utilisateur', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='reset_tokens',
                    to='api.utilisateur',
                )),
            ],
            options={
                'verbose_name': 'Token réinitialisation mot de passe',
                'ordering': ['-cree_le'],
            },
        ),
    ]
