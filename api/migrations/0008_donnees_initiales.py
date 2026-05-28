"""
Migration de données initiales — pré-remplit la base avec le contenu
qui était codé en dur dans le frontend (bienfaits, histoire, partenaires, blog).
"""
from django.db import migrations


def inserer_donnees(apps, schema_editor):
    Bienfait         = apps.get_model('api', 'Bienfait')
    HistoireChapitre = apps.get_model('api', 'HistoireChapitre')
    Partenaire       = apps.get_model('api', 'Partenaire')
    ArticleBlog      = apps.get_model('api', 'ArticleBlog')

    # ── Bienfaits ──────────────────────────────────────────────────────
    bienfaits = [
        ('❤️', 'Circulation sanguine',  'Nourrit les cellules, libère les artères naturellement', 0),
        ('😴', 'Sommeil profond',        'Endormissement rapide et repos vraiment réparateur', 1),
        ('🦴', 'Articulations',          'Réduit les inflammations et soulage les douleurs', 2),
        ('🌿', 'Digestion douce',        'Stimule le transit, apaise les ballonnements', 3),
        ('🧘', 'Anti-stress',            'Effet relaxant naturel dès la première tasse', 4),
        ('✨', 'Purification',           "Nettoie et détoxifie l'organisme en profondeur", 5),
    ]
    for icone, titre, description, ordre in bienfaits:
        Bienfait.objects.get_or_create(
            titre=titre,
            defaults=dict(icone=icone, description=description, ordre=ordre, actif=True)
        )

    # ── Chapitres de l'histoire ────────────────────────────────────────
    chapitres = [
        ('01', 'Les laboratoires de Cuba', 0,
         "Vétérinaire de formation, diplômé de Cuba où il a achevé ses études dans le plus grand "
         "laboratoire de diagnostic du pays, le fondateur de TROPICANA PIO PIO n'a jamais cessé "
         "d'observer, d'analyser et de comprendre le vivant. C'est dans les salles d'histologie et "
         "d'hématologie de ce prestigieux laboratoire qu'une conviction profonde s'est forgée en lui : "
         "une cellule saine est une cellule bien irriguée."),
        ('02', 'Le retour au Bénin', 1,
         "De retour au Bénin, fort de cette expertise scientifique, il tourne son regard vers les "
         "ressources naturelles de sa terre. C'est alors qu'il redécouvre une plante ancestrale, "
         "cultivée depuis des siècles dans les cours royales d'Égypte : la verveine blanche à odeur "
         "citronnée — le roi des thés."),
        ('03', 'La naissance de Tropicana Pio Pio', 2,
         "Convaincu que ce trésor naturel méritait d'être partagé avec le plus grand nombre, le "
         "fondateur décide d'en faire une filière sérieuse et structurée. Il commence à cultiver la "
         "verveine blanche ainsi que d'autres plantes médicinales menacées de disparition. "
         "Aujourd'hui, TROPICANA PIO PIO est né de cette rencontre entre la rigueur scientifique "
         "et la sagesse ancestrale africaine."),
        ('04', 'Notre ambition', 3,
         "Notre thé, 100% bio, sans additifs, est produit à Porto-Novo et recommandé pour toute la "
         "famille — des enfants dès 2 ans aux personnes du troisième âge. Notre ambition : rayonner "
         "à l'échelle nationale, sous-régionale et internationale, et faire du Thé Pio Pio un "
         "ambassadeur du bien-être africain dans le monde entier."),
    ]
    for numero, titre, ordre, texte in chapitres:
        HistoireChapitre.objects.get_or_create(
            titre=titre,
            defaults=dict(numero=numero, texte=texte, ordre=ordre, actif=True)
        )

    # ── Partenaires ────────────────────────────────────────────────────
    partenaires = [
        ("World's Poultry Science Association", 'https://wpsa.com/', 'Partenaire scientifique', 0),
        ('ONG Rail Bénin',                      '#',                  'Partenaire local',         1),
    ]
    for nom, lien, tag, ordre in partenaires:
        Partenaire.objects.get_or_create(
            nom=nom,
            defaults=dict(lien=lien, tag=tag, ordre=ordre, actif=True)
        )

    # ── Articles de blog ───────────────────────────────────────────────
    articles = [
        {
            'titre':            'Les 7 bienfaits prouvés de la verveine blanche citronnée',
            'slug':             'verveine-blanche-bienfaits',
            'categorie':        'Plantes médicinales',
            'date_publication': '2025-04-10',
            'temps_lecture':    '5 min',
            'extrait':          "Découvrez pourquoi la verveine blanche est au cœur de notre formule "
                                "et comment elle agit sur votre corps au quotidien.",
            'contenu':          "La verveine blanche citronnée (Lippia citriodora) est cultivée depuis "
                                "des siècles dans les cours royales d'Égypte. Riche en antioxydants et "
                                "en composés anti-inflammatoires, elle agit sur la circulation sanguine, "
                                "le sommeil, les articulations et la digestion.\n\n"
                                "**1. Circulation sanguine**\nSes flavonoïdes aident à dilater les "
                                "vaisseaux et à fluidifier le sang naturellement.\n\n"
                                "**2. Sommeil**\nSon effet sédatif léger favorise un endormissement "
                                "rapide sans accoutumance.\n\n"
                                "**3. Anti-inflammatoire**\nL'acide rosmarinique qu'elle contient réduit "
                                "les douleurs articulaires en usage régulier.",
            'publie':           True,
        },
        {
            'titre':            'Le Thé Pio Pio en famille : dès 2 ans, pour tous',
            'slug':             'the-famille-enfants',
            'categorie':        'Famille & Santé',
            'date_publication': '2025-03-22',
            'temps_lecture':    '3 min',
            'extrait':          "Pourquoi notre thé est recommandé pour toute la famille, des enfants "
                                "dès 2 ans aux seniors. Conseils d'utilisation.",
            'contenu':          "Le Thé Pio Pio est formulé pour être doux et sans effets secondaires. "
                                "Voici nos recommandations par tranche d'âge :\n\n"
                                "**Enfants (2-12 ans)** : 1 tasse le soir, légèrement sucrée au miel.\n\n"
                                "**Adolescents et adultes** : 1 à 2 tasses par jour, matin ou soir.\n\n"
                                "**Seniors** : 2 tasses par jour recommandées pour les articulations "
                                "et la circulation.",
            'publie':           True,
        },
        {
            'titre':            'Devenir distributeur Tropicana Pio Pio au Bénin',
            'slug':             'distributeur-the-piopio',
            'categorie':        'Distribution',
            'date_publication': '2025-02-15',
            'temps_lecture':    '4 min',
            'extrait':          "Vous souhaitez vendre le Thé Pio Pio dans votre boutique ou votre "
                                "région ? Découvrez nos conditions de partenariat.",
            'contenu':          "Nous cherchons des distributeurs sérieux dans toutes les villes du "
                                "Bénin. Voici comment rejoindre notre réseau :\n\n"
                                "**Conditions** : achat minimum de 10 boîtes, prix distributeur "
                                "négocié, formation produit offerte.\n\n"
                                "**Avantages** : marge attractive, support marketing, livraison "
                                "directe chez vous.\n\n"
                                "Contactez-nous au +229 01 95 96 77 62 ou via WhatsApp pour plus "
                                "d'informations.",
            'publie':           True,
        },
    ]
    for art in articles:
        ArticleBlog.objects.get_or_create(
            slug=art['slug'],
            defaults=art
        )


def supprimer_donnees(apps, schema_editor):
    """Rollback : supprime uniquement les entrées créées par cette migration."""
    Bienfait         = apps.get_model('api', 'Bienfait')
    HistoireChapitre = apps.get_model('api', 'HistoireChapitre')
    ArticleBlog      = apps.get_model('api', 'ArticleBlog')

    titres_bienfaits = [
        'Circulation sanguine', 'Sommeil profond', 'Articulations',
        'Digestion douce', 'Anti-stress', 'Purification',
    ]
    Bienfait.objects.filter(titre__in=titres_bienfaits).delete()

    titres_histoire = [
        'Les laboratoires de Cuba', 'Le retour au Bénin',
        'La naissance de Tropicana Pio Pio', 'Notre ambition',
    ]
    HistoireChapitre.objects.filter(titre__in=titres_histoire).delete()

    slugs = ['verveine-blanche-bienfaits', 'the-famille-enfants', 'distributeur-the-piopio']
    ArticleBlog.objects.filter(slug__in=slugs).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_slider_bienfait_partenaire_histoirechapitre_articleblog'),
    ]

    operations = [
        migrations.RunPython(inserer_donnees, supprimer_donnees),
    ]
