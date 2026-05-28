from django.db import migrations
from django.utils.text import slugify


def inserer(apps, schema_editor):
    FAQ    = apps.get_model('api', 'FAQ')
    Produit = apps.get_model('api', 'Produit')

    # ── FAQ ────────────────────────────────────────────────────────────────
    faqs = [
        ('Produit',  "Qu'est-ce que le Thé Pio Pio ?",
         "Le Thé Pio Pio est une infusion 100% naturelle à base de verveine blanche citronnée, cultivée sans engrais ni herbicides à Porto-Novo, Bénin. Formulé par un vétérinaire spécialiste en biologie cellulaire.", 0),
        ('Produit',  "Le thé est-il vraiment 100% naturel ?",
         "Oui. Aucun additif, colorant, arôme artificiel ou conservateur. Uniquement des plantes médicinales séchées et triées à la main.", 1),
        ('Santé',    "À partir de quel âge peut-on consommer le Thé Pio Pio ?",
         "Dès 2 ans pour les enfants. Il est recommandé pour toute la famille : enfants, adultes et personnes du troisième âge.", 2),
        ('Santé',    "Combien de tasses par jour recommandez-vous ?",
         "1 à 2 tasses par jour suffisent. Le soir avant de dormir pour un effet relaxant, ou le matin à jeun pour la digestion.", 3),
        ('Santé',    "Le thé a-t-il des effets secondaires ?",
         "Non, aucun effet secondaire connu. C'est une plante douce et naturelle. En cas de traitement médical en cours, consultez votre médecin.", 4),
        ('Livraison',"Livrez-vous partout au Bénin ?",
         "Oui, nous livrons dans toutes les villes du Bénin sous 24 à 72 heures après confirmation de la commande.", 5),
        ('Livraison',"Quel est le délai de livraison ?",
         "24 à 48 heures pour Cotonou et Porto-Novo. 48 à 72 heures pour les autres villes. Nous vous contactons dès l'expédition.", 6),
        ('Paiement', "Quels modes de paiement acceptez-vous ?",
         "MTN Money, Moov Money, Wave et Orange Money. Paiement à la livraison également disponible selon votre localisation.", 7),
        ('Paiement', "Comment se passe le paiement Mobile Money ?",
         "Après confirmation de votre commande, vous recevrez un numéro de transfert. Effectuez le paiement et envoyez la capture d'écran par WhatsApp.", 8),
        ('Commande', "Comment passer une commande ?",
         "Ajoutez les produits au panier sur notre boutique, remplissez le formulaire de commande avec vos informations, choisissez le mode de paiement et confirmez.", 9),
        ('Commande', "Puis-je annuler ou modifier ma commande ?",
         "Oui, dans les 2 heures suivant la commande. Contactez-nous par WhatsApp au +229 01 95 96 77 62.", 10),
        ('Commande', "Comment devenir distributeur ?",
         "Contactez-nous par WhatsApp ou email. Nous offrons des conditions avantageuses pour les revendeurs et boutiques partenaires.", 11),
    ]
    for cat, question, reponse, ordre in faqs:
        FAQ.objects.get_or_create(
            question=question,
            defaults=dict(reponse=reponse, categorie=cat, ordre=ordre, actif=True)
        )

    # ── Produit initial ────────────────────────────────────────────────────
    produits = [
        {
            'nom': 'Thé Pio Pio — Sachet 50g',
            'slug': 'the-pio-pio-50g',
            'description': 'Infusion de verveine blanche citronnée 100% naturelle et bio. Cultivée à Porto-Novo, Bénin, sans engrais ni herbicides. 1 sachet = environ 25 tasses. Idéal pour débuter.',
            'prix': 2500,
            'unite': 'sachet',
            'badge': '⭐ Populaire',
            'disponible': True,
        },
        {
            'nom': 'Thé Pio Pio — Sachet 100g',
            'slug': 'the-pio-pio-100g',
            'description': 'Format économique. Infusion de verveine blanche citronnée 100% naturelle. Environ 50 tasses. Idéal pour une consommation régulière en famille.',
            'prix': 4500,
            'unite': 'sachet',
            'badge': '💰 Économique',
            'disponible': True,
        },
        {
            'nom': 'Thé Pio Pio — Pack Famille 3×100g',
            'slug': 'the-pio-pio-pack-famille',
            'description': 'Pack de 3 sachets de 100g. Le meilleur rapport qualité/prix pour toute la famille. Environ 150 tasses. Livraison gratuite incluse.',
            'prix': 12000,
            'unite': 'pack',
            'badge': '🎁 Meilleur deal',
            'disponible': True,
        },
    ]
    for p in produits:
        Produit.objects.get_or_create(
            slug=p['slug'],
            defaults=p
        )


def supprimer(apps, schema_editor):
    FAQ = apps.get_model('api', 'FAQ')
    FAQ.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [('api', '0018_faq')]
    operations = [migrations.RunPython(inserer, supprimer)]
