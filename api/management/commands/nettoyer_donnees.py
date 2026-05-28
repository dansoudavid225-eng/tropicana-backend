"""
Management command de maintenance — à lancer via cron ou scheduler :

  # Nettoyer chaque nuit à minuit
  0 0 * * * python manage.py nettoyer_donnees

  # Ou via Render/Railway : ajouter un Cron Job avec cette commande
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
import datetime


class Command(BaseCommand):
    help = 'Nettoie les données expirées et envoie des rappels de commandes en attente'

    def handle(self, *args, **options):
        maintenant = timezone.now()
        total_nettoye = 0

        # ── 1. Supprimer les tokens de reset expirés ──────────────────────────
        from api.models import ResetPasswordToken
        tokens_expires = ResetPasswordToken.objects.filter(
            expire_le__lt=maintenant
        )
        nb_tokens = tokens_expires.count()
        tokens_expires.delete()
        total_nettoye += nb_tokens
        self.stdout.write(f'✅ {nb_tokens} token(s) reset expirés supprimés')

        # ── 2. Nettoyer les paniers inactifs depuis plus de 30 jours ──────────
        from api.models import PanierSauvegarde
        limite_panier = maintenant - datetime.timedelta(days=30)
        paniers_vieux = PanierSauvegarde.objects.filter(
            mis_a_jour__lt=limite_panier
        )
        nb_paniers = paniers_vieux.count()
        paniers_vieux.update(donnees={'lignes': []})
        total_nettoye += nb_paniers
        self.stdout.write(f'✅ {nb_paniers} panier(s) inactifs vidés')

        # ── 3. Nettoyer les vieux logs de connexion (> 90 jours) ──────────────
        from api.models import LogConnexion
        limite_logs = maintenant - datetime.timedelta(days=90)
        nb_logs = LogConnexion.objects.filter(date__lt=limite_logs).count()
        LogConnexion.objects.filter(date__lt=limite_logs).delete()
        total_nettoye += nb_logs
        self.stdout.write(f'✅ {nb_logs} log(s) anciens supprimés')

        # ── 4. Rappel commandes en attente depuis plus de 24h ─────────────────
        from api.models import Commande
        limite_attente = maintenant - datetime.timedelta(hours=24)
        commandes_en_attente = Commande.objects.filter(
            statut='en_attente',
            date_commande__lt=limite_attente,
            date_commande__gt=limite_attente - datetime.timedelta(hours=1),  # évite les doublons
        )

        for commande in commandes_en_attente:
            # Email au client
            if commande.email_client:
                send_mail(
                    subject=f"[Tropicana Pio Pio] Votre commande #{commande.id} est en cours de traitement",
                    message=(
                        f"Bonjour {commande.nom_client},\n\n"
                        f"Votre commande #{commande.id} passée hier est bien reçue et en cours de traitement.\n"
                        f"Notre équipe vous contactera très prochainement.\n\n"
                        f"Pour toute urgence :\n"
                        f"📞 +229 01 95 96 77 62\n"
                        f"💬 WhatsApp : wa.me/2290195967762\n\n"
                        f"— L'équipe Tropicana Pio Pio"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[commande.email_client],
                    fail_silently=True,
                )

            # Alerte à l'admin
            send_mail(
                subject=f"⚠️ Commande #{commande.id} en attente depuis +24h",
                message=(
                    f"La commande #{commande.id} de {commande.nom_client} ({commande.telephone_client})\n"
                    f"est en attente depuis plus de 24h.\n\n"
                    f"Total : {commande.total} FCFA — Ville : {commande.ville_livraison}\n\n"
                    f"Pensez à la traiter !"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )

        nb_rappels = commandes_en_attente.count()
        self.stdout.write(f'✅ {nb_rappels} rappel(s) commandes envoyés')

        # ── 5. Alerte stock faible (stock <= 5 et > 0) ────────────────────────
        from api.models import Produit
        produits_faibles = Produit.objects.filter(stock__gt=0, stock__lte=5)
        if produits_faibles.exists():
            liste = '\n'.join([f"- {p.nom} : {p.stock} restant(s)" for p in produits_faibles])
            send_mail(
                subject="⚠️ [Tropicana] Stock faible sur certains produits",
                message=f"Les produits suivants ont un stock faible :\n\n{liste}\n\nPensez à réapprovisionner.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=True,
            )
            self.stdout.write(f'⚠️ Alerte stock faible : {produits_faibles.count()} produit(s)')

        self.stdout.write(
            self.style.SUCCESS(f'\n🧹 Nettoyage terminé — {total_nettoye} éléments traités')
        )
