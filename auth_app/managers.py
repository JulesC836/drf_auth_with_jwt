from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(UserManager):
    """
    Gestionnaire d'utilisateurs personnalisé qui utilise l'email comme identifiant unique
    au lieu du nom d'utilisateur.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("L'adresse email est obligatoire."))
        
        email = self.normalize_email(email)
        user = self.model(email=email,username=email, **extra_fields)
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Le superutilisateur doit avoir is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Le superutilisateur doit avoir is_superuser=True.")
        
        return self.create_user(email, password, **extra_fields)


