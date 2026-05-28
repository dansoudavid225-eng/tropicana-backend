from django.db import migrations


def inserer(apps, schema_editor):
    Slider = apps.get_model('api', 'Slider')
    Slider.objects.get_or_create(
        titre='La nature africaine',
        defaults=dict(
            sous_titre='dans votre tasse',
            lien='/boutique',
            texte_bouton='Commander dès 1 000 FCFA',
            actif=True,
            ordre=0,
            # Pas d'image : le composant utilise /images/hero-plantation.jpg par défaut
        )
    )


def supprimer(apps, schema_editor):
    Slider = apps.get_model('api', 'Slider')
    Slider.objects.filter(titre='La nature africaine').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0011_donnees_missions_fondateur'),
    ]
    operations = [
        migrations.RunPython(inserer, supprimer),
    ]
