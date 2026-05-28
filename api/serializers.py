from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Utilisateur, Produit, Commande, LigneCommande, Temoignage, MessageContact


# ─── Authentification ────────────────────────────────────────────────────────

class InscriptionSerializer(serializers.ModelSerializer):
    mot_de_passe = serializers.CharField(write_only=True, min_length=6)
    confirmation = serializers.CharField(write_only=True)

    class Meta:
        model  = Utilisateur
        fields = ['prenom', 'nom', 'email', 'telephone', 'ville',
                  'mot_de_passe', 'confirmation']

    def validate_telephone(self, value):
        import re
        cleaned = re.sub(r'[\s\-\.]', '', value)
        if not re.match(r'^(\+229)?[0-9]{8,12}$', cleaned):
            raise serializers.ValidationError(
                'Numéro invalide. Format attendu : +229XXXXXXXX ou 8 à 12 chiffres.'
            )
        return cleaned  # stocker la version normalisée

    def validate(self, data):
        if data['mot_de_passe'] != data.pop('confirmation'):
            raise serializers.ValidationError(
                {'confirmation': 'Les mots de passe ne correspondent pas.'})
        try:
            validate_password(data['mot_de_passe'])
        except Exception as e:
            raise serializers.ValidationError({'mot_de_passe': list(e.messages)})
        return data

    def create(self, validated_data):
        mot_de_passe = validated_data.pop('mot_de_passe')
        user = Utilisateur(**validated_data)
        user.set_password(mot_de_passe)
        user.save()
        return user


class UtilisateurSerializer(serializers.ModelSerializer):
    nom_complet = serializers.ReadOnlyField()

    class Meta:
        model  = Utilisateur
        fields = ['id', 'prenom', 'nom', 'nom_complet', 'email',
                  'telephone', 'ville', 'date_inscription',
                  'photo_url', 'google_id', 'is_staff']
        read_only_fields = ['id', 'email', 'date_inscription', 'google_id', 'is_staff']


class ModifierProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Utilisateur
        fields = ['prenom', 'nom', 'telephone', 'ville']


class ModifierMotDePasseSerializer(serializers.Serializer):
    ancien_mot_de_passe  = serializers.CharField(write_only=True)
    nouveau_mot_de_passe = serializers.CharField(write_only=True, min_length=6)
    confirmation         = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['nouveau_mot_de_passe'] != data['confirmation']:
            raise serializers.ValidationError(
                {'confirmation': 'Les mots de passe ne correspondent pas.'})
        return data


# ─── Google OAuth ─────────────────────────────────────────────────────────────

class GoogleAuthSerializer(serializers.Serializer):
    credential = serializers.CharField()
    google_id  = serializers.CharField()
    email      = serializers.EmailField()
    prenom     = serializers.CharField()
    nom        = serializers.CharField()
    photo_url  = serializers.URLField(required=False, allow_blank=True)


# ─── Produit ─────────────────────────────────────────────────────────────────

class ProduitSerializer(serializers.ModelSerializer):
    image    = serializers.SerializerMethodField()
    en_stock = serializers.SerializerMethodField()

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

    def get_en_stock(self, obj):
        """True si le produit est disponible (stock=0 = illimité)."""
        return obj.disponible and (obj.stock == 0 or obj.stock > 0)

    class Meta:
        model  = Produit
        fields = ['id', 'nom', 'slug', 'description', 'prix',
                  'unite', 'badge', 'image', 'disponible', 'stock', 'en_stock',
                  'quantite_min']


# ─── Commande ✅ CORRIGÉE : multi-produits ────────────────────────────────────

class LigneCommandeInputSerializer(serializers.Serializer):
    """Ligne envoyée par le frontend lors de la création."""
    produit_id = serializers.IntegerField()
    quantite   = serializers.IntegerField(min_value=1)

    def validate_produit_id(self, value):
        if not Produit.objects.filter(pk=value, disponible=True).exists():
            raise serializers.ValidationError(
                f"Le produit #{value} est introuvable ou indisponible.")
        return value


class LigneCommandeSerializer(serializers.ModelSerializer):
    """Sérialisation en lecture d'une ligne de commande."""
    produit_nom = serializers.CharField(source='produit.nom', read_only=True)
    sous_total  = serializers.ReadOnlyField()

    class Meta:
        model  = LigneCommande
        fields = ['id', 'produit', 'produit_nom', 'quantite', 'prix_unitaire', 'sous_total']


class CommandeCreerSerializer(serializers.Serializer):
    """Crée une commande avec une ou plusieurs lignes."""
    nom_client        = serializers.CharField(max_length=200)
    email_client      = serializers.EmailField()
    telephone_client  = serializers.CharField(max_length=30)
    ville_livraison   = serializers.CharField(max_length=100)
    adresse_livraison = serializers.CharField(required=False, allow_blank=True)
    mode_paiement     = serializers.ChoiceField(choices=Commande.PAIEMENT_CHOICES)
    notes             = serializers.CharField(required=False, allow_blank=True)
    lignes            = LigneCommandeInputSerializer(many=True)

    def validate_telephone_client(self, value):
        import re
        cleaned = re.sub(r'[\s\-\.]', '', value)
        if not re.match(r'^(\+229)?[0-9]{8,12}$', cleaned):
            raise serializers.ValidationError(
                "Numéro de téléphone invalide. Format attendu : +229XXXXXXXX ou 8 à 12 chiffres."
            )
        return value

    def validate_lignes(self, value):
        if not value:
            raise serializers.ValidationError(
                "La commande doit contenir au moins un produit.")
        return value

    def create(self, validated_data):
        lignes_data = validated_data.pop('lignes')

        commande = Commande.objects.create(**validated_data)

        total = 0
        for ligne in lignes_data:
            produit = Produit.objects.get(pk=ligne['produit_id'])
            quantite = ligne['quantite']
            LigneCommande.objects.create(
                commande=commande,
                produit=produit,
                quantite=quantite,
                prix_unitaire=produit.prix,
            )
            total += produit.prix * quantite

        commande.total = total
        commande.save(update_fields=['total'])
        return commande


class CommandeSerializer(serializers.ModelSerializer):
    lignes           = LigneCommandeSerializer(many=True, read_only=True)
    statut_affiche   = serializers.CharField(source='get_statut_display', read_only=True)
    paiement_affiche = serializers.CharField(source='get_mode_paiement_display', read_only=True)

    class Meta:
        model  = Commande
        fields = [
            'id', 'nom_client', 'email_client', 'telephone_client',
            'ville_livraison', 'adresse_livraison',
            'lignes', 'total',
            'mode_paiement', 'paiement_affiche',
            'statut', 'statut_affiche',
            'notes', 'date_commande',
        ]


# ─── Témoignage ──────────────────────────────────────────────────────────────

class TemoignageCreerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Temoignage
        fields = ['nom', 'ville', 'note', 'texte',
                  'type_video', 'video_fichier', 'video_lien', 'video_thumbnail']

    def validate_note(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError('La note doit être entre 1 et 5.')
        return value

    def validate_texte(self, value):
        if value and len(value.strip()) > 0 and len(value.strip()) < 20:
            raise serializers.ValidationError(
                'Le témoignage doit faire au moins 20 caractères.')
        return value

    def validate_video_thumbnail(self, value):
        """✅ Validation : seules les images sont acceptées comme thumbnail."""
        if value:
            TYPES_AUTORISES = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
            if hasattr(value, 'content_type') and value.content_type not in TYPES_AUTORISES:
                raise serializers.ValidationError(
                    'Format image non autorisé. Utilisez JPEG, PNG ou WebP.')
        return value

    def validate(self, data):
        type_video  = data.get('type_video', 'aucune')
        texte       = data.get('texte', '').strip()
        video_fichier = data.get('video_fichier')
        video_lien  = (data.get('video_lien') or '').strip()

        if not texte and type_video == 'aucune':
            raise serializers.ValidationError(
                'Veuillez rédiger un témoignage ou joindre une vidéo.')
        if type_video == 'upload' and not video_fichier:
            raise serializers.ValidationError(
                {'video_fichier': 'Veuillez sélectionner un fichier vidéo.'})
        if type_video == 'lien' and not video_lien:
            raise serializers.ValidationError(
                {'video_lien': 'Veuillez entrer un lien YouTube ou TikTok.'})
        return data


class TemoignageSerializer(serializers.ModelSerializer):
    date_formatee = serializers.SerializerMethodField()
    embed_url     = serializers.ReadOnlyField()
    a_video       = serializers.ReadOnlyField()

    class Meta:
        model  = Temoignage
        fields = [
            'id', 'nom', 'ville', 'note', 'texte',
            'type_video', 'video_fichier', 'video_lien', 'video_thumbnail',
            'embed_url', 'a_video',
            'date_creation', 'date_formatee',
        ]

    def get_date_formatee(self, obj):
        mois = ['', 'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
                'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
        return f"{mois[obj.date_creation.month]} {obj.date_creation.year}"


# ─── Message Contact ─────────────────────────────────────────────────────────

class MessageContactSerializer(serializers.ModelSerializer):
    class Meta:
        model  = MessageContact
        fields = ['id', 'nom', 'email', 'telephone', 'objet', 'message', 'lu', 'date_envoi']
        read_only_fields = ['id', 'date_envoi']

    def validate_message(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError('Le message est trop court.')
        return value


# ─── Newsletter ───────────────────────────────────────────────────────────────
from .models import NewsletterAbonne

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model  = NewsletterAbonne
        fields = ['email']


# ─── Slider ──────────────────────────────────────────────────────────────────
from .models import Slider, Bienfait, Partenaire, HistoireChapitre, ArticleBlog

class SliderSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

    class Meta:
        model  = Slider
        fields = ['id', 'titre', 'sous_titre', 'image', 'lien',
                  'texte_bouton', 'actif', 'ordre']


class BienfaitSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Bienfait
        fields = ['id', 'icone', 'titre', 'description', 'ordre', 'actif']


class PartenaireSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, obj):
        if not obj.logo:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.logo.url)
        return obj.logo.url

    class Meta:
        model  = Partenaire
        fields = ['id', 'nom', 'logo', 'lien', 'tag', 'actif', 'ordre']


class HistoireChapitreSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

    class Meta:
        model  = HistoireChapitre
        fields = ['id', 'numero', 'titre', 'texte', 'image', 'ordre', 'actif']


class ArticleBlogSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if not obj.image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url

    class Meta:
        model  = ArticleBlog
        fields = ['id', 'titre', 'slug', 'categorie', 'image', 'extrait',
                  'contenu', 'temps_lecture', 'publie',
                  'date_publication', 'date_creation']


from .models import Mission, FondateurConfig

class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Mission
        fields = ['id', 'icone', 'texte', 'ordre', 'actif']

class FondateurConfigSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    def get_photo(self, obj):
        if not obj.photo:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.photo.url)
        return obj.photo.url

    class Meta:
        model  = FondateurConfig
        fields = ['id', 'citation', 'nom', 'role', 'photo']


from .models import ConfigAccueil

class ConfigAccueilSerializer(serializers.ModelSerializer):
    tasse_image = serializers.SerializerMethodField()

    def get_tasse_image(self, obj):
        if not obj.tasse_image:
            return None
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.tasse_image.url)
        return obj.tasse_image.url

    class Meta:
        model  = ConfigAccueil
        fields = ['id', 'tasse_label', 'tasse_citation', 'tasse_bouton', 'tasse_lien',
                  'tasse_image', 'cta_label', 'cta_texte', 'cta_bouton', 'cta_lien',
                  'slogan', 'heures_ouverture']


from .models import ConfigSite

class ConfigSiteSerializer(serializers.ModelSerializer):
    paiements_liste = serializers.SerializerMethodField()
    arguments       = serializers.SerializerMethodField()
    stats           = serializers.SerializerMethodField()

    def get_paiements_liste(self, obj):
        return [p.strip() for p in obj.paiements.split(',') if p.strip()]

    def get_arguments(self, obj):
        return [
            {'icone': obj.argument1_icone, 'titre': obj.argument1_titre, 'sous': obj.argument1_sous},
            {'icone': obj.argument2_icone, 'titre': obj.argument2_titre, 'sous': obj.argument2_sous},
            {'icone': obj.argument3_icone, 'titre': obj.argument3_titre, 'sous': obj.argument3_sous},
            {'icone': obj.argument4_icone, 'titre': obj.argument4_titre, 'sous': obj.argument4_sous},
        ]

    def get_stats(self, obj):
        return [
            {'icone': obj.stat1_icone, 'num': obj.stat1_num, 'label': obj.stat1_label, 'desc': obj.stat1_desc},
            {'icone': obj.stat2_icone, 'num': obj.stat2_num, 'label': obj.stat2_label, 'desc': obj.stat2_desc},
            {'icone': obj.stat3_icone, 'num': obj.stat3_num, 'label': obj.stat3_label, 'desc': obj.stat3_desc},
            {'icone': obj.stat4_icone, 'num': obj.stat4_num, 'label': obj.stat4_label, 'desc': obj.stat4_desc},
        ]

    class Meta:
        model  = ConfigSite
        fields = [
            'id', 'telephone', 'telephone_raw', 'email', 'adresse',
            'description_footer', 'tiktok_url', 'facebook_url',
            'paiements', 'paiements_liste', 'prix_affiche', 'prix_mini',
            'arguments', 'stats',
        ]


from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model  = FAQ
        fields = ['id', 'question', 'reponse', 'categorie', 'ordre', 'actif']


# ─── Nouveaux sérializers ──────────────────────────────────────────────────────

from .models import ZoneLivraison, HistoriqueCommande, Blacklist, ReponseAvis, AlerteStock


class ZoneLivraisonSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ZoneLivraison
        fields = ['id', 'ville', 'prix', 'delai', 'disponible', 'ordre']


class HistoriqueCommandeSerializer(serializers.ModelSerializer):
    modifie_par_email = serializers.SerializerMethodField()

    class Meta:
        model  = HistoriqueCommande
        fields = ['id', 'ancien_statut', 'nouveau_statut', 'note', 'modifie_par_email', 'date']

    def get_modifie_par_email(self, obj):
        return obj.modifie_par.email if obj.modifie_par else 'Système'


class BlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Blacklist
        fields = ['id', 'type_blacklist', 'valeur', 'raison', 'date_ajout']


class ReponseAvisSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ReponseAvis
        fields = ['id', 'texte', 'date']


class AlerteStockSerializer(serializers.ModelSerializer):
    produit_nom  = serializers.CharField(source='produit.nom', read_only=True)
    stock_actuel = serializers.IntegerField(source='produit.stock', read_only=True)
    en_alerte    = serializers.SerializerMethodField()

    class Meta:
        model  = AlerteStock
        fields = ['id', 'produit', 'produit_nom', 'stock_actuel', 'seuil',
                  'email_alerte', 'derniere_alerte', 'en_alerte']

    def get_en_alerte(self, obj):
        return obj.produit.stock > 0 and obj.produit.stock <= obj.seuil
