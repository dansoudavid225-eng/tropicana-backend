# 🧹 Maintenance automatique — Tropicana Pio Pio

## Commande de nettoyage

Lance cette commande chaque nuit pour nettoyer les données expirées :

```bash
python manage.py nettoyer_donnees
```

### Ce que fait cette commande :
- ✅ Supprime les tokens de réinitialisation de mot de passe expirés
- ✅ Vide les paniers inactifs depuis plus de 30 jours
- ✅ Supprime les logs de connexion de plus de 90 jours
- ✅ Envoie un rappel au client si sa commande est en attente depuis +24h
- ✅ Alerte l'admin par email si le stock d'un produit est faible (≤ 5)

---

## Configuration Cron (Linux/VPS)

```bash
# Éditer le crontab
crontab -e

# Ajouter cette ligne (exécution chaque nuit à minuit)
0 0 * * * cd /chemin/vers/tropicana_v10/backend && python manage.py nettoyer_donnees >> logs/maintenance.log 2>&1
```

## Configuration sur Render / Railway

Ajouter un **Cron Job** avec :
- **Command** : `python manage.py nettoyer_donnees`
- **Schedule** : `0 0 * * *` (minuit chaque jour)

---

## Migrations à appliquer

Après déploiement, lancer dans l'ordre :

```bash
python manage.py migrate
```

### Nouvelles migrations :
- `0020_resetpasswordtoken` — Réinitialisation mot de passe
- `0021_paniersauvegarde` — Panier persistant
- `0022_supprimer_autres_produits` — Garde uniquement le sachet 1000 FCFA
- `0023_stock_logconnexion` — Champ stock + logs de connexion

---

## Variables d'environnement requises

Voir `.env.production.exemple` pour la liste complète.

Variable importante pour la commande de nettoyage :
```
DEFAULT_FROM_EMAIL=tropicanapiopio.officiel@gmail.com
FRONTEND_URL=https://tropicanapiopio.com
```
