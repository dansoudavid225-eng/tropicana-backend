from django.db import models
import os
from io import BytesIO
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


def compresser_image(image_field, max_width=1200, qualite=80):
    """Compresse et redimensionne une image uploadée avec Pillow."""
    try:
        from PIL import Image
        img = Image.open(image_field)
        # Convertir en RGB si nécessaire (ex: PNG avec transparence)
        if img.mode in ('RGBA', 'P', 'LA'):
            fond = Image.new('RGB', img.size, (255, 255, 255))
            fond.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = fond
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        # Redimensionner si trop large
        if img.width > max_width:
            ratio  = max_width / img.width
            height = int(img.height * ratio)
            img    = img.resize((max_width, height), Image.LANCZOS)
        # Sauvegarder compressé
        output = BytesIO()
        img.save(output, format='JPEG', quality=qualite, optimize=True)
        output.seek(0)
        nom_base = os.path.splitext(os.path.basename(image_field.name))[0]
        return ContentFile(output.read(), name=f'{nom_base}.jpg')
    except Exception:
        return None  # En cas d'erreur, garder l'original


class UtilisateurManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    email            = models.EmailField(unique=True)
    prenom           = models.CharField(max_length=100)
    nom              = models.CharField(max_length=100)
    telephone        = models.CharField(max_length=30, blank=True)
    ville            = models.CharField(max_length=100, blank=True)
    is_active        = models.BooleanField(default=True)
    is_staff         = models.BooleanField(default=False)
    date_inscription = models.DateTimeField(default=timezone.now)
    google_id        = models.CharField(max_length=100, blank=True, null=True, unique=True)
    photo_url        = models.URLField(blank=True, null=True)

    objects = UtilisateurManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['prenom', 'nom']

    class Meta:
        verbose_name        = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return f"{self.prenom} {self.nom} <{self.email}>"

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"


class Produit(models.Model):
    nom           = models.CharField(max_length=200)
    slug          = models.SlugField(unique=True)
    description   = models.TextField()
    prix          = models.DecimalField(max_digits=10, decimal_places=0)
    unite         = models.CharField(max_length=50, default='boite')
    badge         = models.CharField(max_length=100, blank=True)
    image         = models.ImageField(upload_to='produits/', blank=True, null=True)
    disponible    = models.BooleanField(default=True)
    stock         = models.PositiveIntegerField(default=0, help_text='0 = stock illimité')
    quantite_min  = models.PositiveIntegerField(default=1, help_text='Quantité minimale de commande')
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Produit'

    def __str__(self):
        return self.nom

    @property
    def en_stock(self):
        """Retourne True si le produit est disponible (stock illimité si stock=0)."""
        return self.disponible and (self.stock == 0 or self.stock > 0)


    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image, 'file'):
            compressed = compresser_image(self.image)
            if compressed:
                self.image.save(compressed.name, compressed, save=False)
        super().save(*args, **kwargs)

class Commande(models.Model):
    STATUT_CHOICES = [
        ('en_attente',   'En attente'),
        ('confirmee',    'Confirmee'),
        ('en_livraison', 'En livraison'),
        ('livree',       'Livree'),
        ('annulee',      'Annulee'),
    ]
    PAIEMENT_CHOICES = [
        ('mtn_money',    'MTN Money'),
        ('moov_money',   'Moov Money'),
        ('wave',         'Wave'),
        ('orange_money', 'Orange Money'),
        ('fedapay',      'Fedapay (carte / mobile)'),
        ('virement',     'Virement bancaire'),
        ('livraison',    'Paiement a la livraison'),
    ]

    utilisateur       = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True, related_name='commandes')
    nom_client        = models.CharField(max_length=200)
    email_client      = models.EmailField()
    telephone_client  = models.CharField(max_length=30)
    ville_livraison   = models.CharField(max_length=100)
    adresse_livraison = models.TextField(blank=True)
    mode_paiement     = models.CharField(max_length=30, choices=PAIEMENT_CHOICES, default='livraison')
    statut            = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    notes             = models.TextField(blank=True)
    total             = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    fedapay_ref       = models.CharField(max_length=100, blank=True, help_text='ID transaction Fedapay')
    payee             = models.BooleanField(default=False, help_text='True quand Fedapay confirme le paiement')
    code_promo        = models.CharField(max_length=50, blank=True, help_text='Code promo utilisé')
    date_commande     = models.DateTimeField(auto_now_add=True)
    date_mise_a_jour  = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Commande'
        ordering     = ['-date_commande']

    def __str__(self):
        return f"Commande #{self.pk} - {self.nom_client}"

    def recalculer_total(self):
        self.total = sum(l.sous_total for l in self.lignes.all())
        self.save(update_fields=['total'])


class LigneCommande(models.Model):
    commande      = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='lignes')
    produit       = models.ForeignKey(Produit, on_delete=models.PROTECT)
    quantite      = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        verbose_name = 'Ligne de commande'

    def __str__(self):
        return f"{self.quantite}x {self.produit.nom}"

    @property
    def sous_total(self):
        return self.prix_unitaire * self.quantite


class Temoignage(models.Model):
    TYPE_VIDEO_CHOICES = [
        ('aucune', 'Pas de video'),
        ('upload', 'Fichier video uploade'),
        ('lien',   'Lien externe (YouTube / TikTok...)'),
    ]

    utilisateur     = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True, related_name='temoignages')
    nom             = models.CharField(max_length=100)
    ville           = models.CharField(max_length=100)
    note            = models.PositiveSmallIntegerField(default=5)
    texte           = models.TextField(blank=True)
    type_video      = models.CharField(max_length=10, choices=TYPE_VIDEO_CHOICES, default='aucune')
    video_fichier   = models.FileField(upload_to='temoignages/videos/', blank=True, null=True)
    video_lien      = models.URLField(blank=True, null=True)
    video_thumbnail = models.ImageField(upload_to='temoignages/thumbnails/', blank=True, null=True)
    approuve        = models.BooleanField(default=False)
    date_creation   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Temoignage'
        ordering     = ['-date_creation']

    def __str__(self):
        return f"{self.nom} ({self.ville}) - {self.note} etoiles"

    @property
    def a_video(self):
        return self.type_video != 'aucune'

    @property
    def embed_url(self):
        if self.type_video != 'lien' or not self.video_lien:
            return None
        url = self.video_lien
        if 'youtube.com/watch' in url:
            vid = url.split('v=')[-1].split('&')[0]
            return f"https://www.youtube.com/embed/{vid}"
        if 'youtu.be/' in url:
            vid = url.split('youtu.be/')[-1].split('?')[0]
            return f"https://www.youtube.com/embed/{vid}"
        return url


class MessageContact(models.Model):
    OBJET_CHOICES = [
        ('commande',      'Commande'),
        ('partenariat',   'Partenariat / Distribution'),
        ('renseignement', 'Renseignement produit'),
        ('autre',         'Autre'),
    ]

    nom        = models.CharField(max_length=200)
    email      = models.EmailField()
    telephone  = models.CharField(max_length=30, blank=True)
    objet      = models.CharField(max_length=30, choices=OBJET_CHOICES, blank=True)
    message    = models.TextField()
    lu         = models.BooleanField(default=False)
    date_envoi = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Message de contact'
        ordering     = ['-date_envoi']

    def __str__(self):
        return f"{self.nom} - {self.objet or 'Sans objet'}"


class NewsletterAbonne(models.Model):
    email            = models.EmailField(unique=True)
    actif            = models.BooleanField(default=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Abonne Newsletter'
        verbose_name_plural = 'Abonnes Newsletter'
        ordering            = ['-date_inscription']

    def __str__(self):
        return self.email


class ResetPasswordToken(models.Model):
    """Token temporaire pour la réinitialisation du mot de passe."""
    utilisateur  = models.ForeignKey('Utilisateur', on_delete=models.CASCADE, related_name='reset_tokens')
    token        = models.CharField(max_length=64, unique=True)
    expire_le    = models.DateTimeField()
    utilise      = models.BooleanField(default=False)
    cree_le      = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Token réinitialisation mot de passe'
        ordering     = ['-cree_le']

    def est_valide(self):
        from django.utils import timezone
        return not self.utilise and self.expire_le > timezone.now()

    def __str__(self):
        return f"Reset token pour {self.utilisateur.email}"


class PanierSauvegarde(models.Model):
    """Panier persistant sauvegardé côté serveur pour chaque utilisateur connecté."""
    utilisateur  = models.OneToOneField('Utilisateur', on_delete=models.CASCADE, related_name='panier_sauvegarde')
    donnees      = models.JSONField(default=dict)   # { lignes: [{produit_id, quantite}] }
    mis_a_jour   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Panier sauvegardé'

    def __str__(self):
        return f"Panier de {self.utilisateur.email}"


class LogConnexion(models.Model):
    """Log des tentatives de connexion pour détecter les attaques brute-force."""
    RESULTAT_CHOICES = [
        ('succes',  'Succès'),
        ('echec',   'Échec'),
        ('bloque',  'Bloqué (throttle)'),
    ]
    email      = models.EmailField(db_index=True)
    ip         = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    resultat   = models.CharField(max_length=10, choices=RESULTAT_CHOICES)
    date       = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Log connexion'
        verbose_name_plural = 'Logs connexions'
        ordering            = ['-date']
        indexes             = [models.Index(fields=['email', 'date'])]

    def __str__(self):
        return f"[{self.resultat}] {self.email} — {self.date:%d/%m/%Y %H:%M}"


# ─── NOUVEAUX MODELES ─────────────────────────────────────────────────────────

class Slider(models.Model):
    titre        = models.CharField(max_length=200)
    sous_titre   = models.TextField(blank=True)
    image        = models.ImageField(upload_to='sliders/', help_text='Taille recommandee : 1920x800px')
    lien         = models.CharField(max_length=200, blank=True, help_text='Ex: /boutique')
    texte_bouton = models.CharField(max_length=100, blank=True, default='Voir plus')
    actif        = models.BooleanField(default=True)
    ordre        = models.PositiveIntegerField(default=0)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Slider / Banniere'
        verbose_name_plural = 'Sliders / Bannieres'
        ordering            = ['ordre']

    def __str__(self):
        return self.titre


    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image, 'file'):
            compressed = compresser_image(self.image)
            if compressed:
                self.image.save(compressed.name, compressed, save=False)
        super().save(*args, **kwargs)

class Bienfait(models.Model):
    icone       = models.CharField(max_length=10, blank=True, help_text='Emoji (copiez-collez un emoji)')
    titre       = models.CharField(max_length=150)
    description = models.TextField()
    ordre       = models.PositiveIntegerField(default=0)
    actif       = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Bienfait'
        verbose_name_plural = 'Bienfaits'
        ordering            = ['ordre']

    def __str__(self):
        return self.titre


class Partenaire(models.Model):
    nom   = models.CharField(max_length=200)
    logo  = models.ImageField(upload_to='partenaires/', help_text='Logo PNG fond transparent recommande')
    lien  = models.URLField(blank=True)
    tag   = models.CharField(max_length=100, blank=True, default='Partenaire')
    actif = models.BooleanField(default=True)
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name        = 'Partenaire'
        verbose_name_plural = 'Partenaires'
        ordering            = ['ordre']

    def __str__(self):
        return self.nom


class HistoireChapitre(models.Model):
    numero     = models.CharField(max_length=10, default='01')
    titre      = models.CharField(max_length=200)
    texte      = models.TextField()
    image      = models.ImageField(upload_to='histoire/', blank=True, null=True)
    ordre      = models.PositiveIntegerField(default=0)
    actif      = models.BooleanField(default=True)
    date_modif = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Chapitre de l'histoire"
        verbose_name_plural = "Chapitres de l'histoire"
        ordering            = ['ordre']

    def __str__(self):
        return f"{self.numero} - {self.titre}"


class ArticleBlog(models.Model):
    titre            = models.CharField(max_length=300)
    slug             = models.SlugField(unique=True)
    categorie        = models.CharField(max_length=100, blank=True, default='Sante naturelle')
    image            = models.ImageField(upload_to='blog/', blank=True, null=True)
    extrait          = models.TextField(help_text='Resume court (2-3 phrases)')
    contenu          = models.TextField(help_text='Contenu complet de l article')
    temps_lecture    = models.CharField(max_length=20, default='3 min')
    publie           = models.BooleanField(default=True)
    date_publication = models.DateField()
    date_creation    = models.DateTimeField(auto_now_add=True)
    date_modif       = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Article de blog'
        verbose_name_plural = 'Articles de blog'
        ordering            = ['-date_publication']

    def __str__(self):
        return self.titre


class Mission(models.Model):
    icone       = models.CharField(max_length=10, blank=True, help_text='Emoji ex: 🌱')
    texte       = models.TextField()
    ordre       = models.PositiveIntegerField(default=0)
    actif       = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Mission'
        verbose_name_plural = 'Missions'
        ordering = ['ordre']

    def __str__(self):
        return self.texte[:60]


class FondateurConfig(models.Model):
    """Configuration unique du bloc fondateur (singleton)."""
    citation    = models.TextField(default="Le plus grand laboratoire, c'est notre propre corps.")
    nom         = models.CharField(max_length=200, default='Felicien Prosper DURAND')
    role        = models.TextField(default='Fondateur · Vétérinaire diplômé\nSpécialiste en biologie cellulaire, Cuba')
    photo       = models.ImageField(upload_to='fondateur/', blank=True, null=True,
                                    help_text='Photo du fondateur. Taille recommandée : 600x800px.')

    class Meta:
        verbose_name = 'Configuration Fondateur'
        verbose_name_plural = 'Configuration Fondateur'

    def __str__(self):
        return f'Fondateur — {self.nom}'

    def save(self, *args, **kwargs):
        # Singleton : un seul enregistrement autorisé
        self.pk = 1
        super().save(*args, **kwargs)


class ConfigAccueil(models.Model):
    """Textes configurables de la page d'accueil (singleton)."""

    # Section tasse / citation
    tasse_label      = models.CharField(max_length=200, default='Un moment rien que pour vous')
    tasse_citation   = models.TextField(default='Redécouvrez le plaisir d\'un moment de calme')
    tasse_bouton     = models.CharField(max_length=100, default='Commander maintenant')
    tasse_lien       = models.CharField(max_length=200, default='/boutique')
    tasse_image      = models.ImageField(upload_to='accueil/', blank=True, null=True,
                                         help_text='Image de fond de la section tasse. Taille recommandée : 1920x600px.')

    # Section CTA doré (bas de page)
    cta_label        = models.CharField(max_length=200, default='Prêt à prendre soin de vous ?')
    cta_texte        = models.TextField(default='Commandez votre Thé Pio Pio dès aujourd\'hui.')
    cta_bouton       = models.CharField(max_length=100, default='Commander dès 2 500 FCFA')
    cta_lien         = models.CharField(max_length=200, default='/boutique')

    # Slogan footer
    slogan           = models.CharField(max_length=300,
                                        default='Un sang qui circule, une vie qui rayonne.',
                                        help_text='Slogan affiché en bas du footer sous le logo.')

    # Heures d'ouverture
    heures_ouverture = models.CharField(max_length=200,
                                        default='Lun – Sam : 8h00 – 18h00',
                                        help_text='Horaires affichés dans la colonne Contact du footer.')

    class Meta:
        verbose_name = "Configuration Page d'accueil"
        verbose_name_plural = "Configuration Page d'accueil"

    def __str__(self):
        return "Configuration Page d'accueil"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class ConfigSite(models.Model):
    """Configuration globale du site (singleton) — infos de contact, réseaux, stats, arguments, paiements."""

    # ── Contact ──────────────────────────────────────────────────────────
    telephone        = models.CharField(max_length=50,  default='+229 01 95 96 77 62')
    telephone_raw    = models.CharField(max_length=50,  default='+2290195967762',
                                        help_text='Sans espaces ni +, pour les liens tel: et WhatsApp')
    email            = models.EmailField(default='tropicanapiopio@gmail.com')
    adresse          = models.CharField(max_length=300, default='Oganla Gare Nord, Porto-Novo, Bénin')

    # ── Description footer ───────────────────────────────────────────────
    description_footer = models.TextField(
        default='Thé 100% naturel à base de verveine blanche citronnée. Cultivé et produit à Porto-Novo, Bénin.',
        help_text='Texte sous le logo dans le footer.'
    )

    # ── Réseaux sociaux ──────────────────────────────────────────────────
    tiktok_url    = models.URLField(blank=True, default='https://www.tiktok.com/@thepio08')
    facebook_url  = models.URLField(blank=True, default='https://facebook.com/profile.php?id=61569744814995')

    # ── Modes de paiement ────────────────────────────────────────────────
    paiements = models.CharField(
        max_length=500,
        default='MTN Money,Moov Money,Wave,Orange',
        help_text='Modes de paiement séparés par des virgules. Ex: MTN Money,Moov Money,Wave'
    )

    # ── Prix produit ─────────────────────────────────────────────────────
    prix_affiche      = models.CharField(max_length=100, default='dès 2 500 FCFA',
                                         help_text='Prix affiché sur les boutons CTA. Ex: dès 2 500 FCFA')
    prix_mini         = models.CharField(max_length=100, default='1 000 FCFA',
                                         help_text='Prix minimum affiché. Ex: 1 000 FCFA')

    # ── 4 Arguments (strip sous le hero) ─────────────────────────────────
    argument1_icone   = models.CharField(max_length=10, default='🌱')
    argument1_titre   = models.CharField(max_length=100, default='100 % Bio')
    argument1_sous    = models.CharField(max_length=200, default='Sans engrais ni herbicides')

    argument2_icone   = models.CharField(max_length=10, default='🔬')
    argument2_titre   = models.CharField(max_length=100, default='Fondé sur la science')
    argument2_sous    = models.CharField(max_length=200, default='Formulé par un vétérinaire')

    argument3_icone   = models.CharField(max_length=10, default='👨‍👩‍👧')
    argument3_titre   = models.CharField(max_length=100, default='Toute la famille')
    argument3_sous    = models.CharField(max_length=200, default='Recommandé dès 2 ans')

    argument4_icone   = models.CharField(max_length=10, default='🇧🇯')
    argument4_titre   = models.CharField(max_length=100, default='Made in Bénin')
    argument4_sous    = models.CharField(max_length=200, default='Livraison nationale')

    # ── Statistiques ─────────────────────────────────────────────────────
    stat1_num    = models.CharField(max_length=50,  default='500+')
    stat1_label  = models.CharField(max_length=200, default='Familles béninoises satisfaites')
    stat1_icone  = models.CharField(max_length=10,  default='👨‍👩‍👧‍👦')
    stat1_desc   = models.CharField(max_length=200, default='Partout au Bénin')

    stat2_num    = models.CharField(max_length=50,  default='100%')
    stat2_label  = models.CharField(max_length=200, default='Bio, zéro additif')
    stat2_icone  = models.CharField(max_length=10,  default='🌱')
    stat2_desc   = models.CharField(max_length=200, default='Sans engrais ni herbicide')

    stat3_num    = models.CharField(max_length=50,  default='Dès 2 ans')
    stat3_label  = models.CharField(max_length=200, default='Pour toute la famille')
    stat3_icone  = models.CharField(max_length=10,  default='👶')
    stat3_desc   = models.CharField(max_length=200, default='Enfants, adultes, seniors')

    stat4_num    = models.CharField(max_length=50,  default='24h')
    stat4_label  = models.CharField(max_length=200, default='Délai de livraison')
    stat4_icone  = models.CharField(max_length=10,  default='📦')
    stat4_desc   = models.CharField(max_length=200, default='Partout au Bénin')

    class Meta:
        verbose_name = 'Configuration Globale du Site'
        verbose_name_plural = 'Configuration Globale du Site'

    def __str__(self):
        return 'Configuration Globale du Site'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)


class FAQ(models.Model):
    question = models.CharField(max_length=400)
    reponse  = models.TextField()
    categorie = models.CharField(max_length=100, blank=True, default='Général',
                                  help_text='Ex: Produit, Livraison, Paiement, Santé')
    ordre    = models.PositiveIntegerField(default=0)
    actif    = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['ordre']

    def __str__(self):
        return self.question[:80]


# ─── Code Promo ───────────────────────────────────────────────────────────────

class CodePromo(models.Model):
    TYPE_CHOICES = [
        ('pourcentage', 'Pourcentage (%)'),
        ('fixe',        'Montant fixe (FCFA)'),
    ]

    code                = models.CharField(max_length=50, unique=True)
    type_reduction      = models.CharField(max_length=20, choices=TYPE_CHOICES, default='pourcentage')
    valeur              = models.DecimalField(max_digits=10, decimal_places=0, help_text='% ou FCFA selon le type')
    limite_utilisations = models.PositiveIntegerField(null=True, blank=True, help_text='Laisser vide = illimité')
    nb_utilisations     = models.PositiveIntegerField(default=0)
    date_expiration     = models.DateTimeField(null=True, blank=True)
    actif               = models.BooleanField(default=True)
    date_creation       = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Code Promo'
        verbose_name_plural = 'Codes Promo'
        ordering            = ['-date_creation']

    def __str__(self):
        return f'{self.code} ({self.valeur}{"%" if self.type_reduction == "pourcentage" else " FCFA"})'

    def est_valide(self):
        from django.utils import timezone
        if not self.actif:
            return False
        if self.date_expiration and self.date_expiration < timezone.now():
            return False
        if self.limite_utilisations and self.nb_utilisations >= self.limite_utilisations:
            return False
        return True

    def calculer_reduction(self, total):
        total = int(total)
        if self.type_reduction == 'pourcentage':
            return int(total * int(self.valeur) / 100)
        return min(int(self.valeur), total)


# ─── Historique statut commande ───────────────────────────────────────────────

class HistoriqueCommande(models.Model):
    commande       = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='historique')
    ancien_statut  = models.CharField(max_length=20, blank=True)
    nouveau_statut = models.CharField(max_length=20)
    note           = models.TextField(blank=True)
    modifie_par    = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True)
    date           = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = 'Historique commande'
        verbose_name_plural = 'Historiques commandes'
        ordering            = ['-date']

    def __str__(self):
        return f'Commande #{self.commande_id} : {self.ancien_statut} → {self.nouveau_statut}'


# ─── Zone de livraison ────────────────────────────────────────────────────────

class ZoneLivraison(models.Model):
    ville        = models.CharField(max_length=100, unique=True)
    prix         = models.DecimalField(max_digits=8, decimal_places=0, default=0, help_text='Prix livraison en FCFA')
    delai        = models.CharField(max_length=100, default='24-48h', help_text='Délai estimé ex: 24-48h')
    disponible   = models.BooleanField(default=True)
    ordre        = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name        = 'Zone de livraison'
        verbose_name_plural = 'Zones de livraison'
        ordering            = ['ordre', 'ville']

    def __str__(self):
        return f'{self.ville} — {self.prix} FCFA ({self.delai})'


# ─── Blacklist email/IP ───────────────────────────────────────────────────────

class Blacklist(models.Model):
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('ip',    'Adresse IP'),
    ]
    type_blacklist = models.CharField(max_length=10, choices=TYPE_CHOICES)
    valeur         = models.CharField(max_length=255, unique=True)
    raison         = models.CharField(max_length=255, blank=True)
    date_ajout     = models.DateTimeField(auto_now_add=True)
    ajoute_par     = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name        = 'Blacklist'
        verbose_name_plural = 'Blacklist'
        ordering            = ['-date_ajout']

    def __str__(self):
        return f'[{self.type_blacklist}] {self.valeur}'


# ─── Réponse aux avis ─────────────────────────────────────────────────────────

class ReponseAvis(models.Model):
    temoignage  = models.OneToOneField(Temoignage, on_delete=models.CASCADE, related_name='reponse')
    texte       = models.TextField()
    date        = models.DateTimeField(auto_now_add=True)
    modifie_par = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name        = 'Réponse avis'
        verbose_name_plural = 'Réponses avis'

    def __str__(self):
        return f'Réponse à avis #{self.temoignage_id}'


# ─── Config stock alertes ─────────────────────────────────────────────────────

class AlerteStock(models.Model):
    produit         = models.OneToOneField(Produit, on_delete=models.CASCADE, related_name='alerte_stock')
    seuil           = models.PositiveIntegerField(default=5, help_text='Envoyer alerte quand stock ≤ seuil')
    email_alerte    = models.EmailField(blank=True, help_text='Laisser vide = email admin par défaut')
    derniere_alerte = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name        = 'Alerte stock'
        verbose_name_plural = 'Alertes stock'

    def __str__(self):
        return f'Alerte stock — {self.produit.nom} (seuil: {self.seuil})'
