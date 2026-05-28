from django.template.response import TemplateResponse
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
import json


def custom_index(self, request, extra_context=None):
    from .models import (
        Commande, Utilisateur, Temoignage, MessageContact,
        NewsletterAbonne, Produit, ArticleBlog,
    )

    # ─── Action rapide : changer le statut d'une commande ─────────────────
    if request.method == 'POST' and request.POST.get('action_commande'):
        cmd_id     = request.POST.get('commande_id')
        new_statut = request.POST.get('new_statut')
        statuts_valides = ['en_attente', 'confirmee', 'en_livraison', 'livree', 'annulee']
        if cmd_id and new_statut in statuts_valides:
            Commande.objects.filter(pk=cmd_id).update(statut=new_statut)

    # ─── Stats principales ────────────────────────────────────────────────
    total_commandes       = Commande.objects.count()
    commandes_attente     = Commande.objects.filter(statut='en_attente').count()
    commandes_confirmees  = Commande.objects.filter(statut='confirmee').count()
    commandes_livraison   = Commande.objects.filter(statut='en_livraison').count()
    total_clients         = Utilisateur.objects.filter(is_staff=False).count()
    produits_dispo        = Produit.objects.filter(disponible=True).count()
    articles_publie       = ArticleBlog.objects.filter(publie=True).count()
    newsletter_abonnes    = NewsletterAbonne.objects.filter(actif=True).count()
    messages_non_lus      = MessageContact.objects.filter(lu=False).count()
    temoignages_attente_count = Temoignage.objects.filter(approuve=False).count()

    total_fcfa_raw   = Commande.objects.filter(statut='livree').aggregate(s=Sum('total'))['s'] or 0
    total_fcfa       = f'{int(total_fcfa_raw):,}'.replace(',', ' ')

    # ─── CA du mois en cours ──────────────────────────────────────────────
    now        = timezone.now()
    debut_mois = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    ca_mois_raw = Commande.objects.filter(
        statut='livree', date_commande__gte=debut_mois
    ).aggregate(s=Sum('total'))['s'] or 0
    ca_mois = f'{int(ca_mois_raw):,}'.replace(',', ' ')

    # ─── Graphique CA des 6 derniers mois ────────────────────────────────
    labels_mois = []
    valeurs_mois = []
    for i in range(5, -1, -1):
        d = now - timedelta(days=30 * i)
        debut = d.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if debut.month == 12:
            fin = debut.replace(year=debut.year + 1, month=1)
        else:
            fin = debut.replace(month=debut.month + 1)
        ca = Commande.objects.filter(
            statut='livree',
            date_commande__gte=debut,
            date_commande__lt=fin,
        ).aggregate(s=Sum('total'))['s'] or 0
        mois_fr = ['Jan','Fév','Mar','Avr','Mai','Jun','Jul','Aoû','Sep','Oct','Nov','Déc']
        labels_mois.append(mois_fr[debut.month - 1])
        valeurs_mois.append(int(ca))

    # ─── Listes récentes ──────────────────────────────────────────────────
    dernieres_commandes = Commande.objects.prefetch_related('lignes__produit').order_by('-date_commande')[:10]

    # Top 5 clients
    from django.db.models import Count, Sum as DSum
    top_clients = list(
        Commande.objects.filter(statut='livree')
        .values('nom_client', 'email_client')
        .annotate(nb_commandes=Count('id'), ca_total=DSum('total'))
        .order_by('-ca_total')[:5]
    )
    messages_non_lus_qs = MessageContact.objects.filter(lu=False).order_by('-date_envoi')[:10]
    temoignages_attente = Temoignage.objects.filter(approuve=False).order_by('-date_creation')[:10]

    context = {
        **self.each_context(request),
        'title': 'Tableau de bord',
        'stats': {
            'total_commandes':          total_commandes,
            'commandes_attente':        commandes_attente,
            'commandes_confirmees':     commandes_confirmees,
            'commandes_livraison':      commandes_livraison,
            'total_clients':            total_clients,
            'total_fcfa':               total_fcfa,
            'ca_mois':                  ca_mois,
            'messages_non_lus':         messages_non_lus,
            'temoignages_en_attente':   temoignages_attente_count,
            'produits_dispo':           produits_dispo,
            'articles_publie':          articles_publie,
            'newsletter_abonnes':       newsletter_abonnes,
            'mois_actuel':              now.month,
            'annee_actuelle':           now.year,
        },
        'dernieres_commandes':  dernieres_commandes,
        'messages_non_lus':     messages_non_lus_qs,
        'temoignages_attente':  temoignages_attente,
        'top_clients':          top_clients,
        'chart_labels':         json.dumps(labels_mois),
        'chart_valeurs':        json.dumps(valeurs_mois),
    }

    if extra_context:
        context.update(extra_context)

    return TemplateResponse(request, 'admin/index.html', context)
