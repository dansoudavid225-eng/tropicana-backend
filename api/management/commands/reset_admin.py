from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()
        email = "tropicanapio.officiel@gmail.com"
        password = "Tropicana2026!"

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": "admin"}
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        self.stdout.write("Mot de passe réinitialisé avec succès.")
