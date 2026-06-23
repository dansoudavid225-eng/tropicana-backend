from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    # Auth
    InscriptionView, ConnexionView, DeconnexionView, GoogleAuthView,
    ProfilView, ModifierMotDePasseView,
    # Reset mot de passe
    DemandeResetMotDePasseView, ConfirmerResetMotDePasseView, VerifierTokenResetView,
    # Panier persistant
    PanierView,
    # Logs sécurité
    AdminLogsConnexionView,
    # Public
    ProduitsListView, ProduitDetailView,
    CommandeCreerView, MesCommandesView, CommandeDetailView, FedapayWebhookView,
    SuiviCommandeView, StatutPaiementPublicView,
    TemoignagesListView, ContactView,
    # Newsletter
    NewsletterInscriptionView, NewsletterDesabonnementView, AdminNewsletterView,
    # Code promo
    ValiderCodePromoView, AdminCodePromoView, AdminCodePromoDetailView,
    # Stats admin
    AdminStatsView,
    # Admin classique
    AdminCommandesView, AdminCommandeDetailView,
    AdminMessagesView, AdminMessageDetailView,
    AdminSiteConfigView, SiteContentPublicView,
    AdminProduitsView, AdminProduitDetailView,
    AdminTemoignagesView, AdminTemoignageDetailView,
    AdminUtilisateursView,
    # Public nouveaux modèles
    SlidersPublicView,
    ZonesLivraisonPublicView, BienfaitsPublicView, PartenairesPublicView,
    HistoirePublicView, BlogPublicView, BlogDetailPublicView,
    MissionsPublicView, FondateurPublicView,
    # Admin nouveaux modèles
    AdminSlidersView, AdminSliderDetailView,
    AdminBienfaitsView, AdminBienfaitDetailView,
    AdminPartenairesView, AdminPartenaireDetailView,
    AdminHistoireView, AdminHistoireDetailView,
    AdminBlogView, AdminBlogDetailView,
    AdminMissionsView, AdminMissionDetailView,
    AdminFondateurView,
    ConfigAccueilPublicView, AdminConfigAccueilView,
    ConfigSitePublicView, AdminConfigSiteView,
    FAQPublicView, AdminFAQView, AdminFAQDetailView,
    # Zones de livraison
    AdminZonesLivraisonView, AdminZoneLivraisonDetailView,
    # Blacklist
    AdminBlacklistView, AdminBlacklistDetailView,
    # Alertes stock
    AdminAlertesStockView,
    # Remboursement, bon de commande, rapport PDF, historique, recherche, reponse avis
    AdminRemboursementView, AdminBonCommandeView, AdminRapportPDFView,
    AdminHistoriqueCommandeView, AdminRechercheGlobaleView, AdminReponseAvisView,
)

urlpatterns = [
    # ── Auth ──────────────────────────────────────────────────────────────
    path('auth/inscription/',                  InscriptionView.as_view(),                name='inscription'),
    path('auth/connexion/',                    ConnexionView.as_view(),                  name='connexion'),
    path('auth/deconnexion/',                  DeconnexionView.as_view(),                name='deconnexion'),
    path('auth/google/',                       GoogleAuthView.as_view(),                 name='google-auth'),
    path('auth/token/refresh/',                TokenRefreshView.as_view(),               name='token-refresh'),
    path('auth/profil/',                       ProfilView.as_view(),                     name='profil'),
    path('auth/mot-de-passe/',                 ModifierMotDePasseView.as_view(),         name='mot-de-passe'),
    path('auth/reset-mot-de-passe/',           DemandeResetMotDePasseView.as_view(),     name='reset-mdp-demande'),
    path('auth/reset-mot-de-passe/confirmer/', ConfirmerResetMotDePasseView.as_view(),   name='reset-mdp-confirmer'),
    path('auth/reset-mot-de-passe/verifier/',  VerifierTokenResetView.as_view(),         name='reset-mdp-verifier'),
    path('auth/panier/',                       PanierView.as_view(),                     name='panier'),
    path('admin/logs/connexions/',             AdminLogsConnexionView.as_view(),         name='admin-logs-connexions'),

    # ── Produits (public) ─────────────────────────────────────────────────
    path('produits/',             ProduitsListView.as_view(),   name='produits-list'),
    path('produits/<slug:slug>/', ProduitDetailView.as_view(),  name='produit-detail'),

    # ── Commandes ─────────────────────────────────────────────────────────
    path('commandes/',                 CommandeCreerView.as_view(),    name='commande-creer'),
    path('commandes/mes/',             MesCommandesView.as_view(),     name='mes-commandes'),
    path('commandes/suivi/',           SuiviCommandeView.as_view(),    name='commande-suivi'),
    path('commandes/<int:pk>/statut-paiement/', StatutPaiementPublicView.as_view(), name='commande-statut-paiement'),
    path('commandes/<int:pk>/',        CommandeDetailView.as_view(),   name='commande-detail'),
    path('paiement/webhook/fedapay/',  FedapayWebhookView.as_view(),   name='fedapay-webhook'),

    # ── Témoignages (public) ──────────────────────────────────────────────
    path('temoignages/', TemoignagesListView.as_view(), name='temoignages'),

    # ── Contact (public) ──────────────────────────────────────────────────
    path('contact/', ContactView.as_view(), name='contact'),

    # ── Code Promo ────────────────────────────────────────────────────────
    path('promo/valider/',         ValiderCodePromoView.as_view(),      name='promo-valider'),
    path('admin/promo/',           AdminCodePromoView.as_view(),        name='admin-promo'),
    path('admin/promo/<int:pk>/',  AdminCodePromoDetailView.as_view(),  name='admin-promo-detail'),

    # ── Stats analytiques admin ───────────────────────────────────────────
    path('admin/stats/', AdminStatsView.as_view(), name='admin-stats'),

    # ── PUBLIC — contenu dynamique ────────────────────────────────────────
    path('sliders/',            SlidersPublicView.as_view(),    name='sliders-public'),
    path('bienfaits/',          BienfaitsPublicView.as_view(),  name='bienfaits-public'),
    path('partenaires/',        PartenairesPublicView.as_view(),name='partenaires-public'),
    path('histoire/',           HistoirePublicView.as_view(),   name='histoire-public'),
    path('blog/',               BlogPublicView.as_view(),       name='blog-public'),
    path('blog/<slug:slug>/',   BlogDetailPublicView.as_view(), name='blog-detail-public'),
    path('missions/',           MissionsPublicView.as_view(),   name='missions-public'),
    path('fondateur/',          FondateurPublicView.as_view(),  name='fondateur-public'),
    path('config-accueil/',     ConfigAccueilPublicView.as_view(), name='config-accueil-public'),
    path('zones-livraison/',    ZonesLivraisonPublicView.as_view(), name='zones-livraison-public'),
    path('config-site/',        ConfigSitePublicView.as_view(),    name='config-site-public'),
    path('content-site/',       SiteContentPublicView.as_view(),   name='content-site-public'),
    path('faq/',                FAQPublicView.as_view(),            name='faq-public'),

    # ── ADMIN ─────────────────────────────────────────────────────────────
    path('admin/commandes/',              AdminCommandesView.as_view(),        name='admin-commandes'),
    path('admin/commandes/<int:pk>/',     AdminCommandeDetailView.as_view(),   name='admin-commande-detail'),
    path('admin/messages/',               AdminMessagesView.as_view(),         name='admin-messages'),
    path('admin/messages/<int:pk>/',      AdminMessageDetailView.as_view(),    name='admin-message-detail'),
    path('admin/config/',                 AdminSiteConfigView.as_view(),       name='admin-config'),
    path('admin/produits/',               AdminProduitsView.as_view(),         name='admin-produits'),
    path('admin/produits/<int:pk>/',      AdminProduitDetailView.as_view(),    name='admin-produit-detail'),
    path('admin/temoignages/',            AdminTemoignagesView.as_view(),      name='admin-temoignages'),
    path('admin/temoignages/<int:pk>/',   AdminTemoignageDetailView.as_view(), name='admin-temoignage-detail'),
    path('admin/utilisateurs/',           AdminUtilisateursView.as_view(),     name='admin-utilisateurs'),
    path('admin/sliders/',                AdminSlidersView.as_view(),          name='admin-sliders'),
    path('admin/sliders/<int:pk>/',       AdminSliderDetailView.as_view(),     name='admin-slider-detail'),
    path('admin/bienfaits/',              AdminBienfaitsView.as_view(),        name='admin-bienfaits'),
    path('admin/bienfaits/<int:pk>/',     AdminBienfaitDetailView.as_view(),   name='admin-bienfait-detail'),
    path('admin/partenaires/',            AdminPartenairesView.as_view(),      name='admin-partenaires'),
    path('admin/partenaires/<int:pk>/',   AdminPartenaireDetailView.as_view(), name='admin-partenaire-detail'),
    path('admin/histoire/',               AdminHistoireView.as_view(),         name='admin-histoire'),
    path('admin/histoire/<int:pk>/',      AdminHistoireDetailView.as_view(),   name='admin-histoire-detail'),
    path('admin/blog/',                   AdminBlogView.as_view(),             name='admin-blog'),
    path('admin/blog/<int:pk>/',          AdminBlogDetailView.as_view(),       name='admin-blog-detail'),
    path('admin/missions/',               AdminMissionsView.as_view(),         name='admin-missions'),
    path('admin/missions/<int:pk>/',      AdminMissionDetailView.as_view(),    name='admin-mission-detail'),
    path('admin/fondateur/',              AdminFondateurView.as_view(),        name='admin-fondateur'),
    path('admin/config-accueil/',         AdminConfigAccueilView.as_view(),    name='admin-config-accueil'),
    path('admin/config-site/',            AdminConfigSiteView.as_view(),       name='admin-config-site'),
    path('admin/faq/',                    AdminFAQView.as_view(),              name='admin-faq'),
    path('admin/faq/<int:pk>/',           AdminFAQDetailView.as_view(),        name='admin-faq-detail'),

    # ── Zones de livraison (admin) ────────────────────────────────────────
    path('admin/zones-livraison/',           AdminZonesLivraisonView.as_view(),      name='admin-zones-livraison'),
    path('admin/zones-livraison/<int:pk>/',  AdminZoneLivraisonDetailView.as_view(), name='admin-zone-livraison-detail'),

    # ── Blacklist (admin) ─────────────────────────────────────────────────
    path('admin/blacklist/',          AdminBlacklistView.as_view(),       name='admin-blacklist'),
    path('admin/blacklist/<int:pk>/', AdminBlacklistDetailView.as_view(), name='admin-blacklist-detail'),

    # ── Alertes stock (admin) ─────────────────────────────────────────────
    path('admin/alertes-stock/', AdminAlertesStockView.as_view(), name='admin-alertes-stock'),

    # ── Commandes — bon de commande, remboursement, historique (admin) ───
    path('admin/commandes/<int:pk>/bon/',         AdminBonCommandeView.as_view(),       name='admin-commande-bon'),
    path('admin/commandes/<int:pk>/rembourser/',  AdminRemboursementView.as_view(),     name='admin-commande-rembourser'),
    path('admin/commandes/<int:pk>/historique/',  AdminHistoriqueCommandeView.as_view(),name='admin-commande-historique'),

    # ── Rapport PDF mensuel (admin) ───────────────────────────────────────
    path('admin/rapport-pdf/', AdminRapportPDFView.as_view(), name='admin-rapport-pdf'),

    # ── Recherche globale (admin) ─────────────────────────────────────────
    path('admin/recherche/', AdminRechercheGlobaleView.as_view(), name='admin-recherche'),

    # ── Réponse aux avis (admin) ──────────────────────────────────────────
    path('admin/temoignages/<int:pk>/reponse/', AdminReponseAvisView.as_view(), name='admin-temoignage-reponse'),

    # ── Newsletter ────────────────────────────────────────────────────────
    path('newsletter/inscription/',   NewsletterInscriptionView.as_view(),   name='newsletter-inscription'),
    path('newsletter/desabonnement/', NewsletterDesabonnementView.as_view(), name='newsletter-desabonnement'),
    path('admin/newsletter/',         AdminNewsletterView.as_view(),         name='admin-newsletter'),
]