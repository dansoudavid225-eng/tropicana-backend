from django.db import migrations


def inserer(apps, schema_editor):
    ConfigSite = apps.get_model('api', 'ConfigSite')
    ConfigSite.objects.get_or_create(pk=1)


class Migration(migrations.Migration):
    dependencies = [('api', '0016_configsite')]
    operations = [migrations.RunPython(inserer, migrations.RunPython.noop)]
