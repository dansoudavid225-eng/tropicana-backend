#!/usr/bin/env python
"""
Script à lancer depuis le dossier backend :
  cd ~/Documents/tropicana_v10/backend
  source venv/bin/activate
  python populate_db.py
"""

import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tropicana_backend.settings')
django.setup()

from api.models import (
    Bienfait, Partenaire, HistoireChapitre, Mission,
    FondateurConfig, ConfigAccueil, ConfigSite,
    SiteContentConfig, FAQ, ArticleBlog, Slider,
)
from django.utils import timezone
import json

print("🚀 Début du peuplement de la base de données...\n")

# ─── 1. Bienfaits ─────────────────────────────────────────────────────────────
print("✅ Bienfaits...")
Bienfait.objects.all().delete()
bienfaits = [
    {'icone': '', 'titre': 'Circulation sanguine',  'description': 'Nourrit les cellules, libère les artères naturellement',      'ordre': 1},
    {'icone': '', 'titre': 'Sommeil profond',        'description': 'Endormissement rapide et repos vraiment réparateur',           'ordre': 2},
    {'icone': '', 'titre': 'Articulations',          'description': 'Réduit les inflammations et soulage les douleurs',             'ordre': 3},
    {'icone': '', 'titre': 'Digestion douce',        'description': 'Stimule le transit, apaise les ballonnements',                 'ordre': 4},
    {'icone': '', 'titre': 'Anti-stress',            'description': 'Effet relaxant naturel dès la première tasse',                 'ordre': 5},
    {'icone': '', 'titre': 'Purification',           'description': "Nettoie et détoxifie l'organisme en profondeur",               'ordre': 6},
]
for b in bienfaits:
    Bienfait.objects.create(**b, actif=True)
print(f"   → {len(bienfaits)} bienfaits créés")

# ─── 2. Missions ──────────────────────────────────────────────────────────────
print("✅ Missions...")
Mission.objects.all().delete()
missions = [
    {'icone': '', 'texte': "Produire un thé 100% bio, sans additifs, accessible à toute la famille",               'ordre': 1},
    {'icone': '', 'texte': "Préserver les plantes médicinales africaines menacées de disparition",                  'ordre': 2},
    {'icone': '', 'texte': "Faire du Thé Pio Pio un ambassadeur du bien-être africain dans le monde",              'ordre': 3},
    {'icone': '', 'texte': "Rayonner à l'échelle nationale, sous-régionale et internationale",                     'ordre': 4},
]
for m in missions:
    Mission.objects.create(**m, actif=True)
print(f"   → {len(missions)} missions créées")

# ─── 3. Chapitres Histoire ────────────────────────────────────────────────────
print("✅ Chapitres de l'histoire...")
HistoireChapitre.objects.all().delete()
chapitres = [
    {
        'numero': '01',
        'titre': 'Les laboratoires de Cuba',
        'texte': "Vétérinaire de formation, diplômé de Cuba où il a achevé ses études dans le plus grand laboratoire de diagnostic du pays, le fondateur de TROPICANA PIO PIO n'a jamais cessé d'observer, d'analyser et de comprendre le vivant. C'est dans les salles d'histologie et d'hématologie de ce prestigieux laboratoire qu'une conviction profonde s'est forgée en lui : une cellule saine est une cellule bien irriguée. Tant que le sang circule librement, les organes fonctionnent, l'énergie abonde, et la maladie s'éloigne.",
        'ordre': 1,
    },
    {
        'numero': '02',
        'titre': 'Le retour au Bénin',
        'texte': "De retour au Bénin, fort de cette expertise scientifique, il tourne son regard vers les ressources naturelles de sa terre. C'est alors qu'il redécouvre une plante ancestrale, cultivée depuis des siècles dans les cours royales d'Égypte pour le roi et ses proches : la verveine blanche à odeur citronnée — le roi des thés. Cette plante, poussant naturellement, sans engrais ni herbicides, possède une propriété remarquable : elle favorise une circulation sanguine optimale, nourrit les cellules, régule le métabolisme et favorise un sommeil réparateur.",
        'ordre': 2,
    },
    {
        'numero': '03',
        'titre': 'La naissance de Tropicana Pio Pio',
        'texte': "Convaincu que ce trésor naturel méritait d'être partagé avec le plus grand nombre, le fondateur décide d'en faire une filière sérieuse et structurée. Il commence à cultiver la verveine blanche ainsi que d'autres plantes médicinales menacées de disparition, avec le souci constant de respecter la nature et les hommes. Aujourd'hui, TROPICANA PIO PIO est né de cette rencontre entre la rigueur scientifique et la sagesse ancestrale africaine.",
        'ordre': 3,
    },
    {
        'numero': '04',
        'titre': 'Notre ambition',
        'texte': "Notre thé, 100% bio, sans additifs, est produit à Porto-Novo et recommandé pour toute la famille — des enfants dès 2 ans aux personnes du troisième âge — pour booster l'énergie, améliorer le sommeil, soulager les articulations et purifier l'organisme. Notre ambition : rayonner à l'échelle nationale, sous-régionale et internationale, et faire du Thé Pio Pio un ambassadeur du bien-être africain dans le monde entier.",
        'ordre': 4,
    },
]
for c in chapitres:
    HistoireChapitre.objects.create(**c, actif=True)
print(f"   → {len(chapitres)} chapitres créés")

# ─── 4. Fondateur ─────────────────────────────────────────────────────────────
print("✅ Configuration Fondateur...")
FondateurConfig.objects.all().delete()
FondateurConfig.objects.create(
    citation="Le plus grand laboratoire, c'est notre propre corps. Notre mission est de lui donner ce dont il a besoin pour fonctionner parfaitement.",
    nom='Felicien Prosper DURAND',
    role='Fondateur · Vétérinaire diplômé\nSpécialiste en biologie cellulaire, Cuba',
)
print("   → Fondateur créé")

# ─── 5. Config Accueil ────────────────────────────────────────────────────────
print("✅ Configuration Page d'accueil...")
ConfigAccueil.objects.all().delete()
ConfigAccueil.objects.create(
    tasse_label    = 'Un moment rien que pour vous',
    tasse_citation = "Redécouvrez le plaisir d'un moment de calme",
    tasse_bouton   = 'Commander maintenant',
    tasse_lien     = '/boutique',
    cta_label      = 'Prêt à prendre soin de vous ?',
    cta_texte      = "Commandez votre Thé Pio Pio dès aujourd'hui.",
    cta_bouton     = 'Commander dès 2 500 FCFA',
    cta_lien       = '/boutique',
    slogan         = 'Un sang qui circule, une vie qui rayonne.',
    heures_ouverture = 'Lun – Sam : 8h00 – 18h00',
)
print("   → Config accueil créée")

# ─── 6. Config Site ───────────────────────────────────────────────────────────
print("✅ Configuration Globale du Site...")
ConfigSite.objects.all().delete()
ConfigSite.objects.create(
    telephone         = '+229 01 95 96 77 62',
    telephone_raw     = '+2290195967762',
    email             = 'tropicanapiopio@gmail.com',
    adresse           = 'Oganla Gare Nord, Porto-Novo, Bénin',
    description_footer= 'Thé 100% naturel à base de verveine blanche citronnée. Cultivé et produit à Porto-Novo, Bénin.',
    tiktok_url        = 'https://www.tiktok.com/@thepio08',
    facebook_url      = 'https://facebook.com/profile.php?id=61569744814995',
    paiements         = 'MTN Money,Moov Money,Wave,Orange',
    prix_affiche      = 'dès 2 500 FCFA',
    prix_mini         = '1 000 FCFA',
    argument1_icone   = '🌱', argument1_titre = '100 % Bio',           argument1_sous = 'Sans engrais ni herbicides',
    argument2_icone   = '🔬', argument2_titre = 'Fondé sur la science', argument2_sous = 'Formulé par un vétérinaire',
    argument3_icone   = '👨‍👩‍👧', argument3_titre = 'Toute la famille',    argument3_sous = 'Recommandé dès 2 ans',
    argument4_icone   = '🇧🇯', argument4_titre = 'Made in Bénin',       argument4_sous = 'Livraison nationale',
    stat1_num   = '500+',    stat1_label = 'Familles béninoises satisfaites', stat1_icone = '👨‍👩‍👧‍👦', stat1_desc = 'Partout au Bénin',
    stat2_num   = '100%',    stat2_label = 'Bio, zéro additif',               stat2_icone = '🌱',      stat2_desc = 'Sans engrais ni herbicide',
    stat3_num   = 'Dès 2 ans', stat3_label = 'Pour toute la famille',         stat3_icone = '👶',      stat3_desc = 'Enfants, adultes, seniors',
    stat4_num   = '24h',     stat4_label = 'Délai de livraison',              stat4_icone = '📦',      stat4_desc = 'Partout au Bénin',
)
print("   → Config site créée")

# ─── 7. FAQ ───────────────────────────────────────────────────────────────────
print("✅ FAQ...")
FAQ.objects.all().delete()
faqs = [
    {'question': "À partir de quel âge peut-on consommer le Thé Pio Pio ?",      'reponse': "Le Thé Pio Pio est recommandé dès 2 ans pour toute la famille — enfants, adultes et personnes âgées.",                                                                  'categorie': 'Produit',   'ordre': 1},
    {'question': "Le thé contient-il des additifs ou conservateurs ?",             'reponse': "Non. Le Thé Pio Pio est 100% naturel, sans additifs, sans conservateurs, sans engrais ni herbicides.",                                                                   'categorie': 'Produit',   'ordre': 2},
    {'question': "Comment préparer le Thé Pio Pio ?",                             'reponse': "Faites infuser 1 sachet dans 250ml d'eau chaude (80-90°C) pendant 5 à 7 minutes. Vous pouvez ajouter du miel naturel selon votre goût.",                                 'categorie': 'Produit',   'ordre': 3},
    {'question': "Quels sont les délais de livraison ?",                           'reponse': "Nous livrons partout au Bénin sous 24h à 48h. Pour Cotonou et Porto-Novo, la livraison peut être effectuée le jour même si vous commandez avant 18h.",                  'categorie': 'Livraison', 'ordre': 4},
    {'question': "Quels modes de paiement acceptez-vous ?",                        'reponse': "Nous acceptons MTN Money, Moov Money, Wave, Orange Money et le paiement à la livraison.",                                                                                  'categorie': 'Paiement',  'ordre': 5},
    {'question': "Puis-je devenir revendeur du Thé Pio Pio ?",                    'reponse': "Oui ! Nous cherchons des distributeurs sérieux partout au Bénin. Contactez-nous via WhatsApp au +229 01 95 96 77 62 ou par email pour connaître nos conditions.",         'categorie': 'Général',   'ordre': 6},
    {'question': "Le thé est-il efficace contre les maladies chroniques ?",        'reponse': "Le Thé Pio Pio est un complément naturel qui favorise la circulation sanguine, le sommeil et le bien-être général. Il ne remplace pas un traitement médical prescrit.", 'categorie': 'Santé',     'ordre': 7},
]
for f in faqs:
    FAQ.objects.create(**f, actif=True)
print(f"   → {len(faqs)} FAQ créées")

# ─── 8. Articles Blog ─────────────────────────────────────────────────────────
print("✅ Articles de blog...")
ArticleBlog.objects.all().delete()
from datetime import date
articles = [
    {
        'titre':            "Qu'est-ce que la verveine blanche ? La plante qui révolutionne votre bien-être",
        'slug':             'verveine-blanche-bienfaits',
        'categorie':        'Santé naturelle',
        'extrait':          "Vous avez entendu parler de la verveine, mais savez-vous vraiment ce que la verveine blanche citronnée peut faire pour votre corps ? Découvrez ses vertus exceptionnelles.",
        'contenu':          "La verveine blanche citronnée est une plante ancestrale cultivée depuis des siècles dans les cours royales d'Égypte. Elle est reconnue pour ses propriétés relaxantes, sa capacité à améliorer la circulation sanguine et à favoriser un sommeil de qualité. Riche en vitamine K et en antioxydants, elle constitue un allié naturel exceptionnel pour toute la famille.",
        'temps_lecture':    '3 min',
        'publie':           True,
        'date_publication': date(2026, 4, 1),
    },
    {
        'titre':            "Thé naturel pour toute la famille : à partir de quel âge et comment ?",
        'slug':             'the-famille-enfants',
        'categorie':        'Famille & Bien-être',
        'extrait':          "Le Thé Pio Pio est recommandé dès 2 ans. Mais comment le préparer pour un enfant ? Quelles précautions prendre ? On vous explique tout en détail.",
        'contenu':          "Pour les enfants de 2 à 10 ans, utilisez un demi-sachet infusé dans 150ml d'eau tiède. Pour les adolescents et adultes, un sachet entier dans 250ml d'eau chaude. Vous pouvez ajouter du miel naturel pour adoucir. Pour les personnes âgées, le thé est particulièrement recommandé le soir pour favoriser un sommeil réparateur.",
        'temps_lecture':    '4 min',
        'publie':           True,
        'date_publication': date(2026, 4, 5),
    },
    {
        'titre':            "Pourquoi distribuer le Thé Pio Pio ? Une opportunité business à saisir au Bénin",
        'slug':             'distributeur-the-piopio',
        'categorie':        'Business & Distribution',
        'extrait':          "Le marché du bien-être naturel est en pleine explosion en Afrique. Le Thé Pio Pio représente une opportunité sérieuse pour tout revendeur.",
        'contenu':          "Avec plus de 500 familles béninoises satisfaites et une demande croissante, le Thé Pio Pio est un produit qui se vend naturellement. Nos revendeurs bénéficient de marges attractives, d'un support commercial et de formations sur le produit. Contactez-nous pour rejoindre notre réseau de distribution.",
        'temps_lecture':    '3 min',
        'publie':           True,
        'date_publication': date(2026, 4, 10),
    },
]
for a in articles:
    ArticleBlog.objects.create(**a)
print(f"   → {len(articles)} articles créés")

# ─── 9. SiteContentConfig (textes éditoriaux) ─────────────────────────────────
print("✅ Contenu éditorial du site...")
SiteContentConfig.objects.all().delete()
SiteContentConfig.objects.create(
    pk=1,
    donnees={
        # Hero
        "hero_badge":         "🌿 100% Bio · Porto-Novo, Bénin",
        "hero_titre":         "La nature africaine",
        "hero_titre_em":      "dans votre tasse",
        "hero_sous_titre":    "Apaise ton stress, naturellement ",
        "hero_sous_titre_em": "| Mị sẹ sīn Bōwā sīn",
        "hero_btn1":          "Commander dès 1 000 FCFA",
        "hero_btn2":          "Notre histoire",
        # Plante
        "plante_label":    "Notre ingrédient phare",
        "plante_titre":    "La verveine blanche",
        "plante_titre_em": "citronnée",
        "plante_texte":    "Cultivée depuis des siècles dans les cours royales d'Égypte, cette plante ancestrale pousse naturellement sur nos terres béninoises sans aucun engrais ni herbicide. Sa saveur délicate, fraîche et citronnée cache des vertus thérapeutiques exceptionnelles.",
        # Tasse
        "tasse_label":       "Un moment rien que pour vous",
        "tasse_citation":    "\"Redécouvrez le plaisir d'un",
        "tasse_citation_em": "moment de calme\"",
        "tasse_btn":         "Commander maintenant",
        # Fondateur
        "fondateur_label":    "Notre fondateur",
        "fondateur_titre":    "De la science à la nature",
        "fondateur_citation": "\"Le plus grand laboratoire, c'est notre propre corps. Notre mission est de lui donner ce dont il a besoin pour fonctionner parfaitement.\"",
        "fondateur_nom":      "Felicien Prosper DURAND",
        "fondateur_sous":     "Fondateur · Vétérinaire diplômé · Spécialiste en biologie cellulaire, Cuba",
        "fondateur_btn":      "Lire notre histoire",
        # Bienfaits
        "bienfaits_label": "Bienfaits prouvés",
        "bienfaits_titre": "Ce que notre thé fait pour vous",
        # Stats
        "stats_bandeau": "🌿 Cultivé à Porto-Novo · Formulé par un vétérinaire · Livraison nationale au Bénin",
        # Localisation
        "loc_titre":      "Cultivé & produit à",
        "loc_titre_em":   "Porto-Novo, Bénin",
        "loc_sous_titre": "Nos plantes poussent en plein cœur du Bénin. Livraison partout au pays sous 24h à 48h.",
        # Histoire
        "histoire_hero_label":    "Notre Histoire",
        "histoire_hero_titre":    "De la science à la nature —",
        "histoire_hero_titre_em": "une vocation née au cœur de l'Afrique",
        "histoire_citation":      "Le plus grand laboratoire, c'est notre propre corps. Notre mission est de lui donner ce dont il a besoin pour fonctionner parfaitement.",
        "histoire_fondateur_nom": "Felicien Prosper DURAND",
        "histoire_fondateur_sous": "Fondateur · Vétérinaire diplômé\nSpécialiste en biologie cellulaire, Cuba",
        # Annonces
        "annonces": [
            "🚚 Livraison gratuite à partir de 5 000 FCFA — partout au Bénin",
            "⚡ Commandez avant 18h, livré dès demain",
            "📞 Commande rapide par WhatsApp : +229 01 95 96 77 62",
        ],
        # Footer
        "footer_slogan":    "\"Un sang qui circule, une vie qui rayonne.\"",
        "footer_cta_pre":   "Prêt à prendre soin de vous ?",
        "footer_cta_titre": "Commandez votre Thé Pio Pio dès aujourd'hui.",
        "footer_cta_btn":   "🛒 Commander dès 2 500 FCFA",
        "footer_adresse":   "Oganla Gare Nord, Porto-Novo, Bénin",
        "footer_horaires":  "Lun – Sam : 8h00 – 18h00",
        "footer_copyright": "© 2026 tropicanapiopio.com — Tous droits réservés 🇧🇯",
        # Contact
        "contact_intro": "Notre équipe est disponible du lundi au samedi, de 8h à 18h. Nous répondons sous 24h.",
    }
)
print("   → Contenu éditorial créé")

print("\n🎉 Base de données peuplée avec succès !")
print("\n📋 Résumé :")
print(f"   Bienfaits     : {Bienfait.objects.count()}")
print(f"   Missions      : {Mission.objects.count()}")
print(f"   Chapitres     : {HistoireChapitre.objects.count()}")
print(f"   FAQ           : {FAQ.objects.count()}")
print(f"   Articles blog : {ArticleBlog.objects.count()}")
print(f"   Config site   : {ConfigSite.objects.count()}")
print(f"   Config accueil: {ConfigAccueil.objects.count()}")
print(f"   Fondateur     : {FondateurConfig.objects.count()}")
print(f"   Contenu édit. : {SiteContentConfig.objects.count()}")
print("\n⚠️  N'oublie pas d'ajouter manuellement :")
print("   - Les PRODUITS (avec photos) → admin/api/produit/")
print("   - Les PARTENAIRES (avec logos) → admin/api/partenaire/")
print("   - Les SLIDERS (avec images) → admin/api/slider/")
