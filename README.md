# Backend Django — Tropicana Pio Pio

Backend REST API pour le site Tropicana Pio Pio, conçu pour s'intégrer avec le frontend Next.js.

## Stack technique

- **Django 5** + **Django REST Framework**
- **JWT** (Simple JWT) pour l'authentification
- **CORS** configuré pour le frontend Next.js (localhost:3000)
- **SQLite** en développement (facilement remplaçable par PostgreSQL en production)

---

## Installation

```bash
# 1. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 2. Installer les dépendances
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers Pillow

# 3. Appliquer les migrations
python manage.py migrate

# 4. Charger les données initiales (produit + témoignages)
python manage.py loaddata_initiale   # ou relancer le script shell

# 5. Créer un compte admin
python manage.py createsuperuser

# 6. Lancer le serveur
python manage.py runserver
```

---

## Endpoints API

### Authentification

| Méthode | URL | Description |
|---------|-----|-------------|
| POST | `/api/auth/inscription/` | Créer un compte |
| POST | `/api/auth/connexion/` | Se connecter (retourne JWT) |
| POST | `/api/auth/deconnexion/` | Se déconnecter |
| POST | `/api/auth/refresh/` | Rafraîchir le token JWT |

**Corps inscription :**
```json
{
  "prenom": "Marie",
  "nom": "Dupont",
  "email": "marie@example.com",
  "telephone": "+229 95 00 00 00",
  "ville": "Cotonou",
  "mot_de_passe": "monmotdepasse",
  "confirmation": "monmotdepasse"
}
```

**Corps connexion :**
```json
{
  "email": "marie@example.com",
  "mot_de_passe": "monmotdepasse"
}
```

**Réponse connexion/inscription :**
```json
{
  "message": "Connexion réussie !",
  "utilisateur": { "id": 1, "prenom": "Marie", "nom": "Dupont", ... },
  "access": "<JWT access token>",
  "refresh": "<JWT refresh token>"
}
```

---

### Profil (authentification requise)

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/profil/` | Voir son profil |
| PATCH | `/api/profil/` | Modifier ses infos |
| POST | `/api/profil/mot-de-passe/` | Changer son mot de passe |

**Header requis :** `Authorization: Bearer <access_token>`

---

### Produits

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/produits/` | Liste des produits disponibles |
| GET | `/api/produits/the-pio-pio/` | Détail d'un produit |

---

### Commandes

| Méthode | URL | Description |
|---------|-----|-------------|
| POST | `/api/commandes/` | Passer une commande |
| GET | `/api/commandes/mes-commandes/` | Mes commandes (auth requise) |
| GET | `/api/commandes/<id>/` | Détail d'une commande |

**Corps commande :**
```json
{
  "nom_client": "Marie Dupont",
  "email_client": "marie@example.com",
  "telephone_client": "+229 95 00 00 00",
  "ville_livraison": "Cotonou",
  "adresse_livraison": "Quartier Fidjrossè",
  "produit": 1,
  "quantite": 2,
  "mode_paiement": "mtn_money",
  "notes": "Sonner au portail bleu"
}
```

**Modes de paiement :** `mtn_money`, `moov_money`, `wave`, `orange_money`, `livraison`

---

### Témoignages

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/temoignages/` | Liste des témoignages approuvés |
| POST | `/api/temoignages/` | Publier un témoignage |

**Corps témoignage :**
```json
{
  "nom": "Agnès M.",
  "ville": "Cotonou",
  "note": 5,
  "texte": "Excellent produit, je recommande !"
}
```

---

### Contact

| Méthode | URL | Description |
|---------|-----|-------------|
| POST | `/api/contact/` | Envoyer un message |

**Corps contact :**
```json
{
  "nom": "Jean Dupont",
  "email": "jean@example.com",
  "telephone": "+229 95 00 00 00",
  "objet": "commande",
  "message": "Je souhaite commander en gros."
}
```

---

## Interface Admin

Accessible sur `/admin/` avec le compte superuser.

Fonctionnalités admin :
- **Utilisateurs** : voir, modifier, désactiver les comptes
- **Commandes** : voir toutes les commandes, modifier le statut (en_attente → confirmée → en_livraison → livrée)
- **Témoignages** : approuver ou masquer les témoignages
- **Messages contact** : marquer comme lu/non lu
- **Produits** : ajouter, modifier, désactiver des produits

---

## Intégration Frontend Next.js

Remplacer dans `context/AuthContext.tsx` les appels localStorage par des appels API :

```typescript
// Inscription
const res = await fetch('http://localhost:8000/api/auth/inscription/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ prenom, nom, email, telephone, ville, mot_de_passe, confirmation }),
})
const data = await res.json()
// Stocker data.access et data.refresh dans localStorage ou cookie httpOnly

// Connexion
const res = await fetch('http://localhost:8000/api/auth/connexion/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, mot_de_passe }),
})
```

---

## Production (déploiement)

1. Remplacer `SECRET_KEY` par une vraie clé secrète
2. Passer `DEBUG = False`
3. Configurer `ALLOWED_HOSTS` avec votre domaine
4. Remplacer SQLite par PostgreSQL
5. Configurer l'envoi d'emails (SMTP Gmail ou Mailgun)
6. Ajouter votre domaine frontend dans `CORS_ALLOWED_ORIGINS`

