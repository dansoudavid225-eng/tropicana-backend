from django.db import migrations


ZONES_LIVRAISON = [
    ('Cotonou',       1000, 'Même jour',  1),
    ('Porto-Novo',    1000, '24h',        2),
    ('Abomey-Calavi', 1500, '24h',        3),
    ('Parakou',       3000, '48-72h',     4),
    ('Bohicon',       2000, '24-48h',     5),
    ('Natitingou',    4000, '48-72h',     6),
    ('Kandi',         4500, '48-72h',     7),
    ('Lokossa',       2500, '24-48h',     8),
    ('Ouidah',        1500, '24h',        9),
    ('Abomey',        2500, '24-48h',    10),
]

PRODUITS = [
    {
        'nom':         'Sachet unitaire Thé Pio Pio',
        'slug':        'the-pio-pio-sachet-unitaire',
        'description': 'Découvrez le Thé Pio Pio — votre allié bien-être au quotidien. Ingrédient phare : la verveine blanche citronnée, reconnue pour ses vertus relaxantes, nettoyante naturelle des arteres, riche en vitamine K.',
        'prix':        100,
        'unite':       'sachet',
        'badge':       '🌿 Nouveau produit',
        'disponible':  True,
        'stock':       0,
        'quantite_min': 6,
    },
    {
        'nom':         'Thé Pio Pio — Sachet verveine citronnelle',
        'slug':        'the-pio-pio-sachet-verveine',
        'description': 'Le Thé Pio Pio fait à base de verveine à la citronnelle, 100% Bio. Cultivé naturellement à Porto-Novo, Bénin.',
        'prix':        1000,
        'unite':       'sachet',
        'badge':       '🌿 100% Bio',
        'disponible':  True,
        'stock':       0,
        'quantite_min': 1,
    },
]

FAQS = [
    ('Quels sont les bienfaits du thé Pio Pio ?', 'Le thé Pio Pio est riche en antioxydants, favorise la relaxation, nettoie les artères et est riche en vitamine K.', 1),
    ('Comment préparer le thé Pio Pio ?', 'Faites infuser un sachet dans 200ml d eau chaude pendant 5 minutes. Ajoutez du miel ou du citron selon votre gout.', 2),
    ('Livrez-vous partout au Bénin ?', 'Oui, nous livrons dans toutes les grandes villes du Bénin. Les délais et frais varient selon la ville.', 3),
    ('Comment passer une commande ?', 'Rendez-vous sur notre page boutique, choisissez vos produits et remplissez le formulaire de commande. Notre équipe vous contactera sous 2h.', 4),
]


def creer_donnees(apps, schema_editor):
    Produit      = apps.get_model('api', 'Produit')
    ZoneLivraison = apps.get_model('api', 'ZoneLivraison')
    FAQ          = apps.get_model('api', 'FAQ')

    for p in PRODUITS:
        safe_fields = {k: v for k, v in p.items() if k != 'ordre'}
        Produit.objects.get_or_create(slug=safe_fields['slug'], defaults=safe_fields)

    for ville, prix, delai, ordre in ZONES_LIVRAISON:
        ZoneLivraison.objects.get_or_create(ville=ville, defaults={'prix': prix, 'delai': delai, 'ordre': ordre, 'disponible': True})

    for i, (question, reponse, ordre) in enumerate(FAQS):
        FAQ.objects.get_or_create(question=question, defaults={'reponse': reponse, 'ordre': ordre, 'actif': True})


def supprimer_donnees(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(creer_donnees, supprimer_donnees),
    ]
