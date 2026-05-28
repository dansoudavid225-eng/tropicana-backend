"""
Commande Django pour créer des données de test.
Usage : python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Crée des données de test pour le développement'

    def handle(self, *args, **options):
        from api.models import (
            Utilisateur, Produit, Commande, LigneCommande,
            Temoignage, MessageContact, NewsletterAbonne,
            CodePromo, ZoneLivraison,
        )

        self.stdout.write('🌱 Création des données de test...\n')

        # ── Utilisateurs ──────────────────────────────────────────────────────
        users_data = [
            {'email': 'client1@test.com', 'prenom': 'Kofi',   'nom': 'Mensah',   'telephone': '0122334455', 'ville': 'Cotonou'},
            {'email': 'client2@test.com', 'prenom': 'Amina',  'nom': 'Diallo',   'telephone': '0133445566', 'ville': 'Porto-Novo'},
            {'email': 'client3@test.com', 'prenom': 'Séraphin', 'nom': 'Agossou', 'telephone': '0144556677', 'ville': 'Parakou'},
        ]
        users = []
        for ud in users_data:
            u, created = Utilisateur.objects.get_or_create(
                email=ud['email'],
                defaults={**ud, 'is_active': True}
            )
            if created:
                u.set_password('test1234')
                u.save()
            users.append(u)
        self.stdout.write(f'  ✓ {len(users)} utilisateurs')

        # ── Commandes de test ─────────────────────────────────────────────────
        produits = list(Produit.objects.filter(disponible=True))
        statuts  = ['en_attente', 'confirmee', 'en_livraison', 'livree', 'annulee']
        modes    = ['livraison', 'mobile_money', 'fedapay']
        villes   = ['Cotonou', 'Porto-Novo', 'Parakou', 'Abomey-Calavi', 'Ouidah']

        nb_commandes = 0
        if produits:
            for i in range(15):
                user    = random.choice(users)
                produit = random.choice(produits)
                qte     = random.randint(1, 5)
                total   = int(produit.prix) * qte

                cmd = Commande.objects.create(
                    utilisateur=user,
                    nom_client=f'{user.prenom} {user.nom}',
                    email_client=user.email,
                    telephone_client=user.telephone,
                    ville_livraison=random.choice(villes),
                    adresse_livraison='Quartier test',
                    mode_paiement=random.choice(modes),
                    statut=random.choice(statuts),
                    total=total,
                    payee=random.choice([True, False]),
                )
                LigneCommande.objects.create(
                    commande=cmd,
                    produit=produit,
                    quantite=qte,
                    prix_unitaire=produit.prix,
                )
                nb_commandes += 1
        self.stdout.write(f'  ✓ {nb_commandes} commandes de test')

        # ── Témoignages ───────────────────────────────────────────────────────
        temos_data = [
            {'nom': 'Marie K.', 'note': 5, 'commentaire': 'Excellent thé, je le recommande vivement !', 'approuve': True},
            {'nom': 'Jean P.',  'note': 4, 'commentaire': 'Très bonne qualité, livraison rapide.', 'approuve': True},
            {'nom': 'Fatou S.', 'note': 5, 'commentaire': 'Le meilleur thé que j\'ai goûté au Bénin !', 'approuve': False},
        ]
        for t in temos_data:
            Temoignage.objects.get_or_create(nom=t['nom'], defaults=t)
        self.stdout.write(f'  ✓ {len(temos_data)} témoignages')

        # ── Messages contact ──────────────────────────────────────────────────
        msgs = [
            {'nom': 'Alice', 'email': 'alice@test.com', 'sujet': 'Question livraison', 'message': 'Livrez-vous à Natitingou ?', 'lu': False},
            {'nom': 'Bob',   'email': 'bob@test.com',   'sujet': 'Commande en gros',   'message': 'Je voudrais commander 100 boîtes.', 'lu': True},
        ]
        for m in msgs:
            MessageContact.objects.get_or_create(email=m['email'], sujet=m['sujet'], defaults=m)
        self.stdout.write(f'  ✓ {len(msgs)} messages contact')

        # ── Newsletter ────────────────────────────────────────────────────────
        emails_news = ['news1@test.com', 'news2@test.com', 'news3@test.com']
        for e in emails_news:
            NewsletterAbonne.objects.get_or_create(email=e, defaults={'actif': True})
        self.stdout.write(f'  ✓ {len(emails_news)} abonnés newsletter')

        # ── Codes promo ───────────────────────────────────────────────────────
        promos = [
            {'code': 'BIENVENUE10', 'type_reduction': 'pourcentage', 'valeur': 10},
            {'code': 'PROMO500',    'type_reduction': 'fixe',        'valeur': 500},
            {'code': 'FETE20',      'type_reduction': 'pourcentage', 'valeur': 20, 'limite_utilisations': 50},
        ]
        for p in promos:
            CodePromo.objects.get_or_create(code=p['code'], defaults=p)
        self.stdout.write(f'  ✓ {len(promos)} codes promo')

        self.stdout.write(self.style.SUCCESS('\n✅ Données de test créées avec succès !'))
        self.stdout.write('   Compte test : client1@test.com / test1234\n')
