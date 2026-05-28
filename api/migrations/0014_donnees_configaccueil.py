from django.db import migrations


def inserer(apps, schema_editor):
    ConfigAccueil = apps.get_model('api', 'ConfigAccueil')
    ConfigAccueil.objects.get_or_create(pk=1, defaults=dict(
        tasse_label="Un moment rien que pour vous",
        tasse_citation="Redécouvrez le plaisir d'un moment de calme",
        tasse_bouton="Commander maintenant",
        tasse_lien="/boutique",
        cta_label="Prêt à prendre soin de vous ?",
        cta_texte="Commandez votre Thé Pio Pio dès aujourd'hui.",
        cta_bouton="Commander dès 2 500 FCFA",
        cta_lien="/boutique",
    ))


def supprimer(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [('api', '0013_configaccueil')]
    operations = [migrations.RunPython(inserer, supprimer)]
