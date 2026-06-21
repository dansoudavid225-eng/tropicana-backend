from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.http import HttpResponse
import csv

from .models import (
    CodePromo,
    HistoriqueCommande, ZoneLivraison, Blacklist, ReponseAvis, AlerteStock,
    Utilisateur, Produit, Commande, LigneCommande,
    Temoignage, MessageContact, NewsletterAbonne,
    Slider, Bienfait, Partenaire, HistoireChapitre, ArticleBlog,
    LogConnexion, PanierSauvegarde,
)

admin.site.site_header = "Tropicana Pio Pio — Administration"
admin.site.site_title  = "Admin Tropicana"
admin.site.index_title = "Tableau de bord"


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display    = ['email', 'nom_complet', 'telephone', 'ville', 'badge_role', 'is_active', 'date_inscription']
    list_filter     = ['is_active', 'is_staff', 'is_superuser']
    search_fields   = ['email', 'prenom', 'nom', 'telephone']
    ordering        = ['-date_inscription']
    list_per_page   = 25
    actions         = ['promouvoir_admin', 'retirer_admin', 'desactiver_comptes']
    readonly_fields = ['date_inscription', 'last_login']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('prenom', 'nom', 'telephone', 'ville')}),
        ('Google OAuth', {'fields': ('google_id', 'photo_url'), 'classes': ('collapse',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('date_inscription', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'prenom', 'nom', 'telephone', 'ville', 'password1', 'password2', 'is_staff'),
        }),
    )

    def badge_role(self, obj):
        if obj.is_superuser:
            return format_html('<span style="background:#7C3AED;color:#fff;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Super Admin</span>')
        if obj.is_staff:
            return format_html('<span style="background:#C9973A;color:#fff;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Admin</span>')
        return format_html('<span style="background:#E2E8F0;color:#64748B;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Client</span>')
    badge_role.short_description = 'Role'

    def promouvoir_admin(self, request, queryset):
        queryset.update(is_staff=True)
        self.message_user(request, "Utilisateurs promus administrateurs.")
    promouvoir_admin.short_description = "Promouvoir en administrateur"

    def retirer_admin(self, request, queryset):
        queryset.filter(is_superuser=False).update(is_staff=False)
        self.message_user(request, "Droits admin retires.")
    retirer_admin.short_description = "Retirer les droits admin"

    def desactiver_comptes(self, request, queryset):
        queryset.filter(is_superuser=False).update(is_active=False)
        self.message_user(request, "Comptes desactives.")
    desactiver_comptes.short_description = "Desactiver les comptes"


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display        = ['apercu_image', 'nom', 'prix_fcfa', 'unite', 'badge', 'badge_dispo', 'disponible', 'stock', 'date_creation']
    list_filter         = ['disponible']
    search_fields       = ['nom', 'description']
    prepopulated_fields = {'slug': ['nom']}
    list_editable       = ['disponible', 'stock']
    list_per_page       = 20
    readonly_fields     = ['apercu_image_grande', 'date_creation']
    actions             = ['activer', 'desactiver']

    fieldsets = (
        ('Informations', {'fields': ('nom', 'slug', 'description', 'badge')}),
        ('Prix et stock', {'fields': ('prix', 'unite', 'disponible', 'stock')}),
        ('Photo', {
            'fields': ('image', 'apercu_image_grande'),
            'description': 'JPG, PNG ou WEBP. Taille recommandee : 800x800px.'
        }),
        ('Dates', {'fields': ('date_creation',), 'classes': ('collapse',)}),
    )

    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:8px;" />', obj.image.url)
        return format_html('<span style="color:#94A3B8;font-size:11px;">Pas de photo</span>')
    apercu_image.short_description = 'Photo'

    def apercu_image_grande(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:300px;border-radius:12px;margin-top:8px;" />', obj.image.url)
        return format_html('<span style="color:#94A3B8;">Aucune image</span>')
    apercu_image_grande.short_description = 'Apercu'

    def prix_fcfa(self, obj):
        return format_html('<strong style="color:#C9973A;">{} FCFA</strong>', f"{int(obj.prix):,}".replace(',', ' '))
    prix_fcfa.short_description = 'Prix'

    def badge_dispo(self, obj):
        if obj.disponible:
            return format_html('<span style="background:#D1FAE5;color:#065F46;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">En vente</span>')
        return format_html('<span style="background:#FEE2E2;color:#991B1B;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Hors stock</span>')
    badge_dispo.short_description = 'Disponible'

    def activer(self, request, queryset):
        queryset.update(disponible=True)
        self.message_user(request, "Produits mis en vente.")
    activer.short_description = "Mettre en vente"

    def desactiver(self, request, queryset):
        queryset.update(disponible=False)
        self.message_user(request, "Produits mis hors stock.")
    desactiver.short_description = "Mettre hors stock"


class LigneCommandeInline(admin.TabularInline):
    model           = LigneCommande
    extra           = 0
    readonly_fields = ['sous_total_affiche']
    fields          = ['produit', 'quantite', 'prix_unitaire', 'sous_total_affiche']
    can_delete      = False

    def sous_total_affiche(self, obj):
        if obj.pk:
            return format_html('<strong>{} FCFA</strong>', f"{int(obj.sous_total):,}".replace(',', ' '))
        return '-'
    sous_total_affiche.short_description = 'Sous-total'


@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display    = ['numero', 'nom_client', 'telephone_client', 'ville_livraison', 'badge_paiement', 'badge_statut', 'statut', 'total_affiche', 'date_commande']
    list_filter     = ['statut', 'mode_paiement', 'ville_livraison']
    search_fields   = ['nom_client', 'email_client', 'telephone_client']
    list_editable   = ['statut']
    readonly_fields = ['total', 'date_commande', 'date_mise_a_jour', 'detail_commande']
    inlines         = [LigneCommandeInline]
    list_per_page   = 25
    date_hierarchy  = 'date_commande'
    actions         = ['confirmer', 'en_livraison', 'livrer', 'annuler', 'exporter_csv']

    fieldsets = (
        ('Client', {'fields': ('nom_client', 'email_client', 'telephone_client', 'ville_livraison', 'adresse_livraison')}),
        ('Commande', {'fields': ('statut', 'mode_paiement', 'total', 'notes', 'detail_commande')}),
        ('Dates', {'fields': ('date_commande', 'date_mise_a_jour'), 'classes': ('collapse',)}),
    )

    def numero(self, obj):
        return format_html('<strong style="color:#2D6A4F;">#{}</strong>', obj.pk)
    numero.short_description = 'N°'

    def total_affiche(self, obj):
        return format_html('<strong style="color:#C9973A;">{} FCFA</strong>', f"{int(obj.total):,}".replace(',', ' '))
    total_affiche.short_description = 'Total'

    def badge_statut(self, obj):
        c = {'en_attente': ('FFF7ED','C2410C','En attente'), 'confirmee': ('F0FDF4','15803D','Confirmee'), 'en_livraison': ('EFF6FF','1D4ED8','En livraison'), 'livree': ('F0FDF4','166534','Livree'), 'annulee': ('FFF1F2','BE123C','Annulee')}
        bg, col, label = c.get(obj.statut, ('F3F4F6','374151', obj.statut))
        return format_html('<span style="background:#{};color:#{};padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">{}</span>', bg, col, label)
    badge_statut.short_description = 'Statut'

    def badge_paiement(self, obj):
        labels = {'mtn_money': 'MTN', 'moov_money': 'Moov', 'wave': 'Wave', 'orange_money': 'Orange', 'livraison': 'Livraison'}
        return labels.get(obj.mode_paiement, obj.mode_paiement)
    badge_paiement.short_description = 'Paiement'

    def detail_commande(self, obj):
        lignes = obj.lignes.all()
        if not lignes:
            return '-'
        rows = ''
        for l in lignes:
            nom = l.produit.nom if l.produit else 'Produit supprime'
            rows += f'<tr><td style="padding:8px;">{nom}</td><td style="padding:8px;text-align:center;">x{l.quantite}</td><td style="padding:8px;text-align:right;">{int(l.prix_unitaire):,} FCFA</td><td style="padding:8px;text-align:right;font-weight:700;">{int(l.sous_total):,} FCFA</td></tr>'
        return mark_safe(f'<table style="width:100%;border-collapse:collapse;margin-top:8px;"><tr style="background:#F8FAFC;"><th style="padding:8px;text-align:left;">Produit</th><th style="padding:8px;">Qte</th><th style="padding:8px;text-align:right;">Prix</th><th style="padding:8px;text-align:right;">S-total</th></tr>{rows}<tr style="border-top:2px solid #2D6A4F;"><td colspan="3" style="padding:8px;font-weight:700;text-align:right;">TOTAL</td><td style="padding:8px;font-weight:700;color:#C9973A;text-align:right;">{int(obj.total):,} FCFA</td></tr></table>')
    detail_commande.short_description = 'Detail'

    def confirmer(self, request, qs):
        qs.update(statut='confirmee')
        self.message_user(request, "Commandes confirmees.")
    confirmer.short_description = "Marquer : Confirmee"

    def en_livraison(self, request, qs):
        qs.update(statut='en_livraison')
        self.message_user(request, "Commandes en livraison.")
    en_livraison.short_description = "Marquer : En livraison"

    def livrer(self, request, qs):
        qs.update(statut='livree')
        self.message_user(request, "Commandes livrees.")
    livrer.short_description = "Marquer : Livree"

    def annuler(self, request, qs):
        qs.update(statut='annulee')
        self.message_user(request, "Commandes annulees.")
    annuler.short_description = "Marquer : Annulee"

    def exporter_csv(self, request, qs):
        r = HttpResponse(content_type='text/csv; charset=utf-8')
        r['Content-Disposition'] = 'attachment; filename="commandes.csv"'
        r.write('\ufeff')
        w = csv.writer(r)
        w.writerow(['N°', 'Client', 'Email', 'Telephone', 'Ville', 'Total FCFA', 'Paiement', 'Statut', 'Date'])
        for c in qs:
            w.writerow([c.pk, c.nom_client, c.email_client, c.telephone_client, c.ville_livraison, int(c.total), c.mode_paiement, c.statut, c.date_commande.strftime('%d/%m/%Y %H:%M')])
        return r
    exporter_csv.short_description = "Exporter CSV"


@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display    = ['nom', 'ville', 'note_etoiles', 'extrait', 'badge_approuve', 'approuve', 'date_creation']
    list_filter     = ['approuve', 'note', 'type_video']
    search_fields   = ['nom', 'ville', 'texte']
    list_editable   = ['approuve']
    readonly_fields = ['embed_url', 'a_video', 'date_creation', 'apercu_video']
    list_per_page   = 20
    actions         = ['approuver', 'masquer']

    fieldsets = (
        ('Client', {'fields': ('nom', 'ville', 'note')}),
        ('Avis', {'fields': ('texte', 'approuve')}),
        ('Video', {'fields': ('type_video', 'video_fichier', 'video_lien', 'embed_url', 'apercu_video'), 'classes': ('collapse',)}),
        ('Dates', {'fields': ('date_creation',), 'classes': ('collapse',)}),
    )

    def note_etoiles(self, obj):
        return format_html('<span style="color:#F59E0B;font-size:16px;">{}</span>', '★' * obj.note + '☆' * (5 - obj.note))
    note_etoiles.short_description = 'Note'

    def extrait(self, obj):
        return obj.texte[:60] + '...' if len(obj.texte) > 60 else obj.texte
    extrait.short_description = 'Avis'

    def badge_approuve(self, obj):
        if obj.approuve:
            return format_html('<span style="background:#D1FAE5;color:#065F46;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Publie</span>')
        return format_html('<span style="background:#FEF3C7;color:#92400E;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">En attente</span>')
    badge_approuve.short_description = 'Statut'

    def apercu_video(self, obj):
        if obj.type_video == 'lien' and obj.embed_url:
            return format_html('<iframe src="{}" width="400" height="225" frameborder="0" allowfullscreen style="border-radius:8px;margin-top:8px;"></iframe>', obj.embed_url)
        if obj.type_video == 'upload' and obj.video_fichier:
            return format_html('<video src="{}" controls width="400" style="border-radius:8px;"></video>', obj.video_fichier.url)
        return '-'
    apercu_video.short_description = 'Apercu video'

    def approuver(self, request, qs):
        qs.update(approuve=True)
        self.message_user(request, "Temoignages publies.")
    approuver.short_description = "Publier"

    def masquer(self, request, qs):
        qs.update(approuve=False)
        self.message_user(request, "Temoignages masques.")
    masquer.short_description = "Masquer"


@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display    = ['badge_lu', 'lu', 'nom', 'email', 'telephone', 'objet', 'extrait', 'date_envoi']
    list_filter     = ['lu', 'objet']
    search_fields   = ['nom', 'email', 'message']
    list_editable   = ['lu']
    readonly_fields = ['date_envoi', 'btn_repondre']
    list_per_page   = 25
    actions         = ['marquer_lu', 'marquer_non_lu']

    fieldsets = (
        ('Expediteur', {'fields': ('nom', 'email', 'telephone', 'objet')}),
        ('Message', {'fields': ('message', 'lu', 'btn_repondre')}),
        ('Date', {'fields': ('date_envoi',), 'classes': ('collapse',)}),
    )

    def badge_lu(self, obj):
        color = '#94A3B8' if obj.lu else '#2563EB'
        return format_html('<span style="color:{};font-size:20px;">&#9679;</span>', color)
    badge_lu.short_description = ''

    def extrait(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    extrait.short_description = 'Message'

    def btn_repondre(self, obj):
        return format_html(
            '<a href="mailto:{}?subject=Re: {} - Tropicana Pio Pio" style="background:#2D6A4F;color:#fff;padding:8px 16px;border-radius:8px;text-decoration:none;font-weight:700;">Repondre par email</a>',
            obj.email, obj.objet or 'Votre message'
        )
    btn_repondre.short_description = 'Repondre'

    def marquer_lu(self, request, qs):
        qs.update(lu=True)
        self.message_user(request, "Messages marques comme lus.")
    marquer_lu.short_description = "Marquer comme lu"

    def marquer_non_lu(self, request, qs):
        qs.update(lu=False)
        self.message_user(request, "Messages marques comme non lus.")
    marquer_non_lu.short_description = "Marquer comme non lu"

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('lu', '-date_envoi')


@admin.register(NewsletterAbonne)
class NewsletterAbonneAdmin(admin.ModelAdmin):
    list_display    = ['email', 'badge_actif', 'actif', 'date_inscription']
    list_filter     = ['actif']
    search_fields   = ['email']
    readonly_fields = ['date_inscription']
    list_editable   = ['actif']
    list_per_page   = 50
    actions         = ['exporter_csv', 'activer', 'desactiver']

    def badge_actif(self, obj):
        if obj.actif:
            return format_html('<span style="background:#D1FAE5;color:#065F46;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Actif</span>')
        return format_html('<span style="background:#FEE2E2;color:#991B1B;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Desabonne</span>')
    badge_actif.short_description = 'Statut'

    def exporter_csv(self, request, qs):
        r = HttpResponse(content_type='text/csv; charset=utf-8')
        r['Content-Disposition'] = 'attachment; filename="newsletter.csv"'
        r.write('\ufeff')
        w = csv.writer(r)
        w.writerow(['Email', 'Statut', 'Date'])
        for a in qs:
            w.writerow([a.email, 'Actif' if a.actif else 'Desabonne', a.date_inscription.strftime('%d/%m/%Y')])
        return r
    exporter_csv.short_description = "Exporter CSV"

    def activer(self, request, qs):
        qs.update(actif=True)
        self.message_user(request, "Abonnes actives.")
    activer.short_description = "Activer"

    def desactiver(self, request, qs):
        qs.update(actif=False)
        self.message_user(request, "Abonnes desactives.")
    desactiver.short_description = "Desactiver"


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display    = ['apercu', 'titre', 'texte_bouton', 'lien', 'badge_actif', 'actif', 'ordre']
    list_editable   = ['actif', 'ordre']
    list_filter     = ['actif']
    search_fields   = ['titre']
    readonly_fields = ['apercu_grande']
    list_per_page   = 20

    fieldsets = (
        ('Contenu', {'fields': ('titre', 'sous_titre', 'texte_bouton', 'lien')}),
        ('Image de fond', {
            'fields': ('image', 'apercu_grande'),
            'description': 'Taille recommandee : 1920x800px. JPG, PNG, WEBP.'
        }),
        ('Affichage', {'fields': ('actif', 'ordre')}),
    )

    def apercu(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:90px;height:50px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        return '-'
    apercu.short_description = 'Apercu'

    def apercu_grande(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:500px;border-radius:8px;margin-top:8px;" />', obj.image.url)
        return 'Aucune image'
    apercu_grande.short_description = 'Apercu actuel'

    def badge_actif(self, obj):
        if obj.actif:
            return format_html('<span style="background:#D1FAE5;color:#065F46;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Affiche</span>')
        return format_html('<span style="background:#FEE2E2;color:#991B1B;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Cache</span>')
    badge_actif.short_description = 'Statut'


@admin.register(Bienfait)
class BienfaitAdmin(admin.ModelAdmin):
    list_display    = ['icone_affiche', 'titre', 'extrait_desc', 'badge_actif', 'actif', 'ordre']
    list_editable   = ['actif', 'ordre']
    list_filter     = ['actif']
    search_fields   = ['titre', 'description']
    list_per_page   = 20

    fieldsets = (
        ('Contenu', {
            'fields': ('icone', 'titre', 'description'),
            'description': 'Ces bienfaits apparaissent dans la section Bienfaits de la page accueil.'
        }),
        ('Affichage', {'fields': ('actif', 'ordre')}),
    )

    def icone_affiche(self, obj):
        return format_html('<span style="font-size:24px;">{}</span>', obj.icone or '-')
    icone_affiche.short_description = 'Icone'

    def extrait_desc(self, obj):
        return obj.description[:60] + '...' if len(obj.description) > 60 else obj.description
    extrait_desc.short_description = 'Description'

    def badge_actif(self, obj):
        if obj.actif:
            return format_html('<span style="background:#D1FAE5;color:#065F46;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Affiche</span>')
        return format_html('<span style="background:#FEE2E2;color:#991B1B;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Cache</span>')
    badge_actif.short_description = 'Statut'


@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display    = ['apercu_logo', 'nom', 'tag', 'lien_cliquable', 'badge_actif', 'actif', 'ordre']
    list_editable   = ['actif', 'ordre']
    list_filter     = ['actif']
    search_fields   = ['nom', 'tag']
    readonly_fields = ['apercu_logo_grande']
    list_per_page   = 20

    fieldsets = (
        ('Informations', {
            'fields': ('nom', 'tag', 'lien'),
            'description': 'Ces partenaires apparaissent dans la section Partenaires de la page accueil.'
        }),
        ('Logo', {
            'fields': ('logo', 'apercu_logo_grande'),
            'description': 'PNG fond transparent recommande. Taille : 300x150px minimum.'
        }),
        ('Affichage', {'fields': ('actif', 'ordre')}),
    )

    def apercu_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:40px;max-width:100px;object-fit:contain;" />', obj.logo.url)
        return '-'
    apercu_logo.short_description = 'Logo'

    def apercu_logo_grande(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height:150px;max-width:300px;object-fit:contain;margin-top:8px;border:1px solid #E2E8F0;padding:10px;border-radius:8px;" />', obj.logo.url)
        return 'Aucun logo'
    apercu_logo_grande.short_description = 'Apercu actuel'

    def lien_cliquable(self, obj):
        if obj.lien:
            return format_html('<a href="{}" target="_blank" style="color:#2D6A4F;">Voir le site</a>', obj.lien)
        return '-'
    lien_cliquable.short_description = 'Site web'

    def badge_actif(self, obj):
        if obj.actif:
            return format_html('<span style="background:#D1FAE5;color:#065F46;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Affiche</span>')
        return format_html('<span style="background:#FEE2E2;color:#991B1B;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Cache</span>')
    badge_actif.short_description = 'Statut'


@admin.register(HistoireChapitre)
class HistoireChapitreAdmin(admin.ModelAdmin):
    list_display    = ['numero', 'titre', 'apercu_image', 'badge_actif', 'actif', 'ordre', 'date_modif']
    list_editable   = ['actif', 'ordre']
    list_filter     = ['actif']
    search_fields   = ['titre', 'texte']
    readonly_fields = ['apercu_image_grande', 'date_modif']
    list_per_page   = 20

    fieldsets = (
        ('Chapitre', {
            'fields': ('numero', 'titre', 'texte'),
            'description': 'Ces chapitres apparaissent dans la page Notre Histoire.'
        }),
        ('Image du chapitre', {'fields': ('image', 'apercu_image_grande')}),
        ('Affichage', {'fields': ('actif', 'ordre')}),
        ('Dates', {'fields': ('date_modif',), 'classes': ('collapse',)}),
    )

    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:60px;height:40px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        return '-'
    apercu_image.short_description = 'Image'

    def apercu_image_grande(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:400px;border-radius:8px;margin-top:8px;" />', obj.image.url)
        return 'Aucune image'
    apercu_image_grande.short_description = 'Apercu actuel'

    def badge_actif(self, obj):
        if obj.actif:
            return format_html('<span style="background:#D1FAE5;color:#065F46;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Affiche</span>')
        return format_html('<span style="background:#FEE2E2;color:#991B1B;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Cache</span>')
    badge_actif.short_description = 'Statut'


@admin.register(ArticleBlog)
class ArticleBlogAdmin(admin.ModelAdmin):
    list_display        = ['apercu_image', 'titre', 'categorie', 'temps_lecture', 'badge_publie', 'publie', 'date_publication']
    list_editable       = ['publie']
    list_filter         = ['publie', 'categorie']
    search_fields       = ['titre', 'extrait', 'contenu']
    prepopulated_fields = {'slug': ['titre']}
    readonly_fields     = ['apercu_image_grande', 'date_creation', 'date_modif']
    list_per_page       = 20
    actions             = ['publier', 'depublier']

    fieldsets = (
        ('Informations', {'fields': ('titre', 'slug', 'categorie', 'temps_lecture', 'date_publication', 'publie')}),
        ('Image principale', {
            'fields': ('image', 'apercu_image_grande'),
            'description': 'Taille recommandee : 1200x630px.'
        }),
        ('Contenu', {
            'fields': ('extrait', 'contenu'),
            'description': 'L\'extrait est affiche dans la liste. Le contenu est la page complete de l\'article.'
        }),
        ('Dates', {'fields': ('date_creation', 'date_modif'), 'classes': ('collapse',)}),
    )

    def apercu_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:80px;height:50px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        return '-'
    apercu_image.short_description = 'Image'

    def apercu_image_grande(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:500px;border-radius:8px;margin-top:8px;" />', obj.image.url)
        return 'Aucune image'
    apercu_image_grande.short_description = 'Apercu actuel'

    def badge_publie(self, obj):
        if obj.publie:
            return format_html('<span style="background:#D1FAE5;color:#065F46;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Publie</span>')
        return format_html('<span style="background:#FEE2E2;color:#991B1B;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;">Brouillon</span>')
    badge_publie.short_description = 'Statut'

    def publier(self, request, qs):
        qs.update(publie=True)
        self.message_user(request, "Articles publies.")
    publier.short_description = "Publier"

    def depublier(self, request, qs):
        qs.update(publie=False)
        self.message_user(request, "Articles mis en brouillon.")
    depublier.short_description = "Mettre en brouillon"


from .models import CodePromo, Mission, FondateurConfig


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display  = ['icone_affiche', 'extrait', 'actif', 'ordre']
    list_editable = ['actif', 'ordre']
    list_per_page = 20

    fieldsets = (
        ('Contenu', {
            'fields': ('icone', 'texte'),
            'description': 'Ces missions apparaissent dans la section "Notre Mission" de la page Histoire.'
        }),
        ('Affichage', {'fields': ('actif', 'ordre')}),
    )

    def icone_affiche(self, obj):
        return format_html('<span style="font-size:24px;">{}</span>', obj.icone or '-')
    icone_affiche.short_description = 'Icone'

    def extrait(self, obj):
        return obj.texte[:80] + '...' if len(obj.texte) > 80 else obj.texte
    extrait.short_description = 'Texte'


@admin.register(FondateurConfig)
class FondateurConfigAdmin(admin.ModelAdmin):
    list_display = ['nom', 'apercu_photo']
    readonly_fields = ['apercu_photo_grande']

    fieldsets = (
        ('Photo', {
            'fields': ('photo', 'apercu_photo_grande'),
            'description': 'Photo du fondateur affichée sur la page Histoire. Taille recommandée : 600x800px.'
        }),
        ('Citation & Identité', {
            'fields': ('citation', 'nom', 'role'),
        }),
    )

    def apercu_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height:50px;border-radius:8px;" />', obj.photo.url)
        return '—'
    apercu_photo.short_description = 'Photo'

    def apercu_photo_grande(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-width:300px;border-radius:12px;margin-top:8px;" />', obj.photo.url)
        return 'Aucune photo'
    apercu_photo_grande.short_description = 'Aperçu actuel'

    def has_add_permission(self, request):
        # Empêche de créer plus d'un enregistrement
        return not FondateurConfig.objects.exists()


from .models import CodePromo, ConfigAccueil


@admin.register(ConfigAccueil)
class ConfigAccueilAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'cta_bouton', 'tasse_bouton']

    fieldsets = (
        ('🖼️ Section Tasse — "Moment de calme"', {
            'fields': ('tasse_image', 'apercu_tasse', 'tasse_label', 'tasse_citation', 'tasse_bouton', 'tasse_lien'),
            'description': 'Section avec image de fond tasse et citation au centre de la page d\'accueil.',
        }),
        ('🟡 Bandeau CTA doré (bas de page)', {
            'fields': ('cta_label', 'cta_texte', 'cta_bouton', 'cta_lien'),
            'description': 'Le bandeau doré "Prêt à prendre soin de vous ?" tout en bas avant le footer.',
        }),
        ('📝 Footer — Slogan & Horaires', {
            'fields': ('slogan', 'heures_ouverture'),
            'description': 'Textes affichés dans le bas de page.',
        }),
    )
    readonly_fields = ['apercu_tasse']

    def apercu_tasse(self, obj):
        if obj.tasse_image:
            return format_html('<img src="{}" style="max-width:400px;border-radius:8px;margin-top:8px;" />', obj.tasse_image.url)
        return 'Aucune image — utilise /images/tasse-dessus.jpg par défaut'
    apercu_tasse.short_description = 'Aperçu image actuelle'

    def has_add_permission(self, request):
        return not ConfigAccueil.objects.exists()


from .models import CodePromo, ConfigSite


@admin.register(ConfigSite)
class ConfigSiteAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'telephone', 'email']

    fieldsets = (
        ('📞 Contact', {
            'fields': ('telephone', 'telephone_raw', 'email', 'adresse'),
            'description': 'Informations de contact affichées dans le footer et la page Contact.',
        }),
        ('📝 Description Footer', {
            'fields': ('description_footer',),
        }),
        ('🔗 Réseaux Sociaux', {
            'fields': ('tiktok_url', 'facebook_url'),
        }),
        ('💳 Modes de Paiement', {
            'fields': ('paiements',),
            'description': 'Séparés par des virgules. Ex: MTN Money,Moov Money,Wave,Orange',
        }),
        ('💰 Prix', {
            'fields': ('prix_affiche', 'prix_mini'),
            'description': 'Prix affichés sur les boutons du site.',
        }),
        ('🏷️ 4 Arguments (strip sous le hero)', {
            'fields': (
                'argument1_icone', 'argument1_titre', 'argument1_sous',
                'argument2_icone', 'argument2_titre', 'argument2_sous',
                'argument3_icone', 'argument3_titre', 'argument3_sous',
                'argument4_icone', 'argument4_titre', 'argument4_sous',
            ),
        }),
        ('📊 Statistiques', {
            'fields': (
                'stat1_icone', 'stat1_num', 'stat1_label', 'stat1_desc',
                'stat2_icone', 'stat2_num', 'stat2_label', 'stat2_desc',
                'stat3_icone', 'stat3_num', 'stat3_label', 'stat3_desc',
                'stat4_icone', 'stat4_num', 'stat4_label', 'stat4_desc',
            ),
        }),
    )

    def has_add_permission(self, request):
        return not ConfigSite.objects.exists()


from .models import CodePromo, FAQ


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display  = ['question_courte', 'categorie', 'actif', 'ordre']
    list_editable = ['actif', 'ordre']
    list_filter   = ['categorie', 'actif']
    search_fields = ['question', 'reponse']

    fieldsets = (
        ('Contenu', {
            'fields': ('question', 'reponse'),
        }),
        ('Classement', {
            'fields': ('categorie', 'ordre', 'actif'),
        }),
    )

    def question_courte(self, obj):
        return obj.question[:80] + '…' if len(obj.question) > 80 else obj.question
    question_courte.short_description = 'Question'


@admin.register(LogConnexion)
class LogConnexionAdmin(admin.ModelAdmin):
    list_display  = ['email', 'ip', 'resultat', 'date']
    list_filter   = ['resultat', 'date']
    search_fields = ['email', 'ip']
    readonly_fields = ['email', 'ip', 'user_agent', 'resultat', 'date']
    ordering      = ['-date']

    def has_add_permission(self, request):
        return False  # Les logs ne se créent pas manuellement


@admin.register(PanierSauvegarde)
class PanierSauvegardeAdmin(admin.ModelAdmin):
    list_display  = ['utilisateur', 'mis_a_jour']
    readonly_fields = ['utilisateur', 'donnees', 'mis_a_jour']


@admin.register(CodePromo)
class CodePromoAdmin(admin.ModelAdmin):
    list_display  = ['code', 'type_reduction', 'valeur', 'nb_utilisations', 'limite_utilisations', 'date_expiration', 'actif']
    list_filter   = ['type_reduction', 'actif']
    search_fields = ['code']
    list_editable = ['actif']


@admin.register(ZoneLivraison)
class ZoneLivraisonAdmin(admin.ModelAdmin):
    list_display  = ['ville', 'prix', 'delai', 'disponible', 'ordre']
    list_editable = ['prix', 'delai', 'disponible', 'ordre']
    search_fields = ['ville']


@admin.register(HistoriqueCommande)
class HistoriqueCommandeAdmin(admin.ModelAdmin):
    list_display  = ['commande', 'ancien_statut', 'nouveau_statut', 'modifie_par', 'date']
    list_filter   = ['nouveau_statut']
    readonly_fields = ['commande', 'ancien_statut', 'nouveau_statut', 'date', 'modifie_par']


@admin.register(Blacklist)
class BlacklistAdmin(admin.ModelAdmin):
    list_display  = ['type_blacklist', 'valeur', 'raison', 'date_ajout']
    list_filter   = ['type_blacklist']
    search_fields = ['valeur', 'raison']


@admin.register(AlerteStock)
class AlerteStockAdmin(admin.ModelAdmin):
    list_display  = ['produit', 'seuil', 'email_alerte', 'derniere_alerte']
    search_fields = ['produit__nom']


@admin.register(ReponseAvis)
class ReponseAvisAdmin(admin.ModelAdmin):
    list_display  = ['temoignage', 'date', 'modifie_par']
    readonly_fields = ['date']


from .models import SiteContentConfig


@admin.register(SiteContentConfig)
class SiteContentConfigAdmin(admin.ModelAdmin):
    list_display    = ['__str__', 'date_maj']
    readonly_fields = ['date_maj']

    def has_add_permission(self, request):
        return not SiteContentConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
