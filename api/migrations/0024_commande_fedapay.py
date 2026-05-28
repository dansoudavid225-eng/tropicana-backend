from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_stock_logconnexion'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='fedapay_ref',
            field=models.CharField(blank=True, max_length=100, help_text='ID transaction Fedapay'),
        ),
        migrations.AddField(
            model_name='commande',
            name='payee',
            field=models.BooleanField(default=False, help_text='True quand Fedapay confirme le paiement'),
        ),
        migrations.AlterField(
            model_name='commande',
            name='mode_paiement',
            field=models.CharField(
                max_length=30,
                choices=[
                    ('mtn_money',   'MTN Money'),
                    ('moov_money',  'Moov Money'),
                    ('wave',        'Wave'),
                    ('orange_money','Orange Money'),
                    ('fedapay',     'Fedapay (carte / mobile)'),
                    ('virement',    'Virement bancaire'),
                    ('livraison',   'Paiement a la livraison'),
                ],
                default='livraison',
            ),
        ),
    ]
