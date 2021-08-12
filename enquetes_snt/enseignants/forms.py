from django import forms
from .models import User  # modèle personnalisé
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.forms.utils import ErrorList
from django.contrib.auth import forms as auth_forms, views as auth_views

from django.utils.translation import gettext_lazy as _

class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):  # redéfinition de la méthode  __init__ de la classe 
        
        

        # pour personnaliser la liste d'erreurs (ErrorList)
        kwargs.update({'error_class': ParagraphErrorList})
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].help_text = 'Seule une adresse académique est valide (du type prenom.nom@ac-&lt;academie&gt;.&lt;domaine&gt;).'
        self.fields['password1'].help_text = 'Le mot de passe doit contenir au moins 8 caractères, ne peut pas être constitué uniquement de chiffres.'
        self.fields['password2'].help_text = None

    first_name = forms.CharField(label="Prénom", max_length=100)
    last_name = forms.CharField(label="Nom", max_length=100)
    email = forms.EmailField()


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
        help_texts = {
            'username': None,
        }
        error_messages = {
            'username' : {
                'unique': 'Cette adresse email est déjà utilisée.'
            }
        }

class MySetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):  # redéfinition de la méthode  __init__ de la classe 
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].help_text = 'Le mot de passe doit contenir au moins 8 caractères, ne peut pas être constitué uniquement de chiffres.'
        self.fields['new_password2'].help_text = None

class ParagraphErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: 
            return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])

class MyAuthenticationForm(auth_forms.AuthenticationForm):
    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("Ce compte est inactif. Pour l'activer, vous devez cliquer sur le lien qui vous a été envoyé par email."),
    }
    
