from django.db import migrations


def inserer(apps, schema_editor):
    Mission        = apps.get_model('api', 'Mission')
    FondateurConfig = apps.get_model('api', 'FondateurConfig')

    missions = [
        ('🌱', "Produire un thé 100% bio, sans additifs, accessible à toute la famille", 0),
        ('🌍', "Préserver les plantes médicinales africaines menacées de disparition", 1),
        ('🏆', "Faire du Thé Pio Pio un ambassadeur du bien-être africain dans le monde", 2),
        ('🚀', "Rayonner à l'échelle nationale, sous-régionale et internationale", 3),
    ]
    for icone, texte, ordre in missions:
        Mission.objects.get_or_create(texte=texte, defaults=dict(icone=icone, ordre=ordre, actif=True))

    FondateurConfig.objects.get_or_create(pk=1, defaults=dict(
        citation="Le plus grand laboratoire, c'est notre propre corps. Notre mission est de lui donner ce dont il a besoin pour fonctionner parfaitement.",
        nom='Felicien Prosper DURAND',
        role='Fondateur · Vétérinaire diplômé\nSpécialiste en biologie cellulaire, Cuba',
    ))


def supprimer(apps, schema_editor):
    Mission = apps.get_model('api', 'Mission')
    Mission.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_mission_fondateurconfig'),
    ]

    operations = [
        migrations.RunPython(inserer, supprimer),
    ]
