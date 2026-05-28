"""
Migration : Ajout des champs vidéo au modèle Temoignage
          + Ajout des champs Google OAuth au modèle Utilisateur

Générez-la avec :
    python manage.py makemigrations api --name="video_temoignages_google_auth"

Ou utilisez ce fichier directement en le plaçant dans api/migrations/
en vous assurant que le numéro est bien le suivant après 0001_initial.
"""

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        # ── Utilisateur : champs Google OAuth ──────────────────────────────
        migrations.AddField(
            model_name='utilisateur',
            name='google_id',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='photo_url',
            field=models.URLField(blank=True, null=True),
        ),
        # Rendre telephone et ville optionnels (pour les comptes Google
        # où l'utilisateur n'a pas encore renseigné ces infos)
        migrations.AlterField(
            model_name='utilisateur',
            name='telephone',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='ville',
            field=models.CharField(blank=True, max_length=100),
        ),

        # ── Temoignage : champs vidéo ───────────────────────────────────────
        migrations.AddField(
            model_name='temoignage',
            name='type_video',
            field=models.CharField(
                choices=[('aucune', 'Pas de vidéo'), ('upload', 'Fichier vidéo uploadé'), ('lien', 'Lien externe (YouTube / TikTok…)')],
                default='aucune',
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='temoignage',
            name='video_fichier',
            field=models.FileField(
                blank=True,
                help_text='Fichier vidéo (MP4, MOV, WEBM — max 100 Mo)',
                null=True,
                upload_to='temoignages/videos/',
            ),
        ),
        migrations.AddField(
            model_name='temoignage',
            name='video_lien',
            field=models.URLField(
                blank=True,
                help_text='Lien YouTube, TikTok, Instagram Reels…',
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='temoignage',
            name='video_thumbnail',
            field=models.ImageField(
                blank=True,
                help_text='Image de prévisualisation (optionnel)',
                null=True,
                upload_to='temoignages/thumbnails/',
            ),
        ),
        # Rendre le texte optionnel (on peut avoir une vidéo sans texte)
        migrations.AlterField(
            model_name='temoignage',
            name='texte',
            field=models.TextField(blank=True),
        ),
        # Passer approuve à False par défaut (modération avant publication)
        migrations.AlterField(
            model_name='temoignage',
            name='approuve',
            field=models.BooleanField(default=False),
        ),
    ]
