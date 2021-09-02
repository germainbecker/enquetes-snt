from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings

from django.contrib.auth import views as auth_views

from .forms import UserRegisterForm, ParagraphErrorList, MyAuthenticationForm

LISTE_ADRESSES_CORRECTES = [
    'ac-aix-marseille.fr',
    'ac-amiens.fr',
    'ac-besancon.fr',
    'ac-bordeaux.fr',
    'ac-clermont.fr',
    'ac-corse.fr',
    'ac-creteil.fr',
    'ac-dijon.fr',
    'ac-grenoble.fr',
    'ac-guadeloupe.fr',
    'ac-guyane.fr',
    'ac-reunion.fr',
    'ac-lille.fr',
    'ac-limoges.fr',
    'ac-lyon.fr',
    'ac-martinique.fr',
    'ac-mayotte.fr',
    'ac-montpellier.fr',
    'ac-nancy-metz.fr',
    'ac-nantes.fr',
    'ac-nice.fr',
    'ac-normandie.fr',
    'ac-noumea.fr',
    'ac-orleans-tours.fr',
    'ac-paris.fr',
    'ac-poitiers.fr',
    'ac-polynesie.pf', # polynesie francaise ?
    'ac-reims.fr',
    'ac-rennes.fr',
    'ac-spm.fr', # saint-pierre et miquelon ?
    'ac-strasbourg.fr',
    'ac-toulouse.fr',
    'ac-versailles.fr',
    'ac-wf.wf', # wallis et futuna ?
]

LISTE_ADRESSES_EXCEPTIONS = settings.EMAIL_EXCEPTIONS

def adresse_email_valide(adresse: str) -> bool:
    """Renvoie True si et seulement si adresse est une adresse e-mail valide"""
    academie = adresse.split('@')[1]
    return academie in LISTE_ADRESSES_CORRECTES or adresse in LISTE_ADRESSES_EXCEPTIONS

def inscription(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, error_class=ParagraphErrorList)
        if form.is_valid():
            
            # Vérification adresse email valide
            adresse_email = form.cleaned_data.get('email')
            
            # Si adresse email non valide (pas @ac-....fr)
            if not adresse_email_valide(adresse_email):
                messages.warning(request, "Le compte n'a pas pu être créé car l'adresse email renseignée n'est pas valide. Assurez-vous d'utiliser votre adresse email académique. Veuillez contacter l'administrateur pour les cas particuliers.")

            # Si adresse email valide
            else:
                enseignant = form.save(commit=False)  # renvoie un objet mais ne l'enregistre en bdd
                enseignant.is_active = False  # on n'active pas le compte par défaut
                enseignant.save()  # enregistrement en bdd

                # envoi de l'email de validation
                domaine = get_current_site(request).domain
                sujet_email = f'Activation de votre compte sur {domaine}'
                message = render_to_string('enseignants/email_activation_compte.html', {
                    'user': enseignant,
                    'domain': domaine,
                    'uid': urlsafe_base64_encode(force_bytes(enseignant.pk)),
                    'token': default_token_generator.make_token(enseignant), 
                })
                destinataire = form.cleaned_data.get('email')
                send_mail(
                    sujet_email,
                    message,
                    settings.EMAIL_HOST_USER,
                    [destinataire],
                    fail_silently=False,
                )

                # message d'information de l'envoi de l'email de validation
                pseudo_enseignant = form.cleaned_data.get('username')
                messages.success(request, f'Un email de validation a été envoyé à l\'adresse indiquée. Cliquez sur le lien présent dans cet email pour valider et finaliser la création du compte pour {pseudo_enseignant}.')
                return redirect('enseignants')
    else:
        form = UserRegisterForm()
    context = {
        'form' : form
    }
    return render(request, 'enseignants/inscription.html', context)

def activation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model()._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Votre compte est activé. Vous pouvez désormais vous identifier et accéder à la plateforme !")
        return redirect('enseignants')
    else:
        messages.warning(request, "Le lien d'activation n'est pas valide.")
        return render(request, 'enseignants/enseignants.html')
