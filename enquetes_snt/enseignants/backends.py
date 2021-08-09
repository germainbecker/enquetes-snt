from django.contrib.auth import backends

class CustomModelBackend(backends.ModelBackend):
    """
    Surcharge de la classe ModelBackend.
    But : pour que tous les utilisateurs (actifs et inactifs) puissent s'authentifier dans la vue LoginView
    faisant appel au formulaire AuthenticationForm. Permet de gérer le message d'erreur pour les utilisateurs inactifs.
    """
    def user_can_authenticate(self, user):
        """Renvoie True que l'utilisateur user soit actif ou non.
        Par défaut, la fonction renvoyait False si user.is_active=False."""
        return True