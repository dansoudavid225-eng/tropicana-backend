from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Surcharger l'admin index pour injecter les stats
        from django.contrib.admin import AdminSite
        from .admin_dashboard import custom_index
        AdminSite.index = custom_index
