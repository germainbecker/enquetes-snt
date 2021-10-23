from django.core.exceptions import ValidationError
from django.http.response import JsonResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.db import transaction, IntegrityError

from .forms import (
    EnqueteCreateForm,
    EnigmeExampleCreateForm,
    EnigmeUpdateForm, 
    EnigmeCreateForm,
    CodeEnqueteForm, 
    EnqueteEleveForm,
    EnqueteCreateForm,
    EnqueteCreateListForm,
    EnqueteShareForm,
    EnqueteShareListForm,
    EnqueteUpdateForm,
    EnqueteUpdateListForm,
    UploadFileForm,
    UploadImageForm,
)
from .models import Enigme, Enquete, Resultat, Fichier, Image


def conditions(request):
    return render(request, 'enigmes/conditions.html')

def index(request):
    
    # Si le formulaire est validé
    if request.method == 'POST':
        # création d'une instance de formulaire et remplissage avec les données saisies
        form = CodeEnqueteForm(request.POST)
        
        # si le form est valide
        if form.is_valid():
            # on récupère le code
            code_enquete = form.cleaned_data['code']

            try:
                enquete = Enquete.objects.get(code=code_enquete)
            except Enquete.DoesNotExist:
                enquete = None
            
            # Si l'enquête n'existe pas
            if enquete == None :
                messages.warning(request, "Le code saisi est incorrect.")               
            
            # Si l'enquête n'est pas activée
            elif enquete.active == False:
                messages.warning(request, "L'enquête n'est pas activée par le professeur.")
        
            else:
                return redirect('enquete-eleve', code_enquete=code_enquete)
    
    else:
        form = CodeEnqueteForm()
    
    context = {'form': form}
    return render(request, 'enigmes/index.html', context)

def enseignants(request):
    if request.user.is_authenticated:
        return redirect('accueil')
    else:
        return render(request, 'enseignants/enseignants.html')

@login_required
def accueil(request):
    message = "Bienvenue sur la page d'accueil"
    context = {
        "message": message
    }
    return render(request, 'enigmes/accueil.html', context)

@login_required
def enigmes(request):
    context = {
        "enigmes": Enigme.objects.all()
    }
    return render(request, 'enigmes/liste.html', context)

@login_required
def mes_fichiers(request):
    user = request.user
    context = {}
    print(request.POST)
    if request.method == 'POST':
        if 'fichier' in request.POST:
            form_fichier = UploadFileForm(request.POST, request.FILES)
            if form_fichier.is_valid():
                fichier = form_fichier.save(commit=False)  # pour enregistrer l'auteur avant la sauvegarde en bdd
                fichier.auteur = user
                fichier.save()
                messages.success(request, "Le fichier a bien été ajouté !")
                redirect('mes-fichiers')
        if 'image' in request.POST:
            form_image = UploadImageForm(request.POST, request.FILES)
            if form_image.is_valid():
                image = form_image.save(commit=False)  # pour enregistrer l'auteur avant la sauvegarde en bdd
                image.auteur = user
                image.save()
                messages.success(request, "L'image a bien été ajoutée !")
                redirect('mes-fichiers')
        
        # suppression d'image non utilisée
        if 'supprimer-image' in request.POST:
            image_id = int(request.POST.get('supprimer-image'))
            image = get_object_or_404(Image, pk=image_id)
            if not image.enigme.all():  # si aucune énigme n'utilise l'image
                try:
                    with transaction.atomic():
                        image.image.delete()  # suppression du fichier
                        image.delete()  # suppression de l'instance
                        messages.success(request, "L'image a bien été supprimée.")
                        redirect('mes-fichiers')
                except IntegrityError:
                    messages.warning(request, "Une erreur interne est apparue. Merci de recommencer.")
            else:
                messages.warning(request, "Vous ne pouvez pas supprimer une image utilisée dans les énigmes.")
                redirect('mes-fichiers')
        
        # suppression de fichier pj non utilisé
        if 'supprimer-fichier' in request.POST:
            fichier_id = int(request.POST.get('supprimer-fichier'))
            fichier = get_object_or_404(Fichier, pk=fichier_id)
            if not fichier.enigme.all():  # si aucune énigme n'utilise le fichier
                try:
                    with transaction.atomic():
                        fichier.fichier.delete()  # suppression du fichier
                        fichier.delete()  # suppression de l'instance
                        messages.success(request, "Le fichier a bien été supprimé.")
                        redirect('mes-fichiers')
                except IntegrityError:
                    messages.warning(request, "Une erreur interne est apparue. Merci de recommencer.")
            else:
                messages.warning(request, "Vous ne pouvez pas supprimer un fichier utilisé dans les énigmes.")
                redirect('mes-fichiers')
    
    form_file = UploadFileForm()
    form_image = UploadImageForm()
    images = Image.objects.filter(auteur=user)
    fichiers = Fichier.objects.filter(auteur=user)
    context = {
        'user': user,
        'form_fichier': form_file,
        'form_image': form_image,
        'images': images,
        'fichiers': fichiers
    }

    # Ajout des fichiers téléversés au contexte

    enigmes_par_image = {}
    for image in images:
        enigmes = [enigme.pk for enigme in image.enigme.all()]
        enigmes_par_image[image] = enigmes
    
    enigmes_par_fichier = {}
    for fichier in fichiers:
        enigmes = [enigme.pk for enigme in fichier.enigme.all()]
        enigmes_par_fichier[fichier] = enigmes

    """ for enigme in enigmes_perso:
        if enigme.image:
            if enigme not in liste_images:
                liste_images[enigme.image] = [enigme]
            else:
                liste_images[enigme.image].append(enigme)
    print(liste_images)

    liste_pj = {}
    for enigme in enigmes_perso:
        if enigme.fichier:
            if enigme not in liste_pj:
                liste_pj[enigme.fichier] = [enigme]
            else:
                liste_pj[enigme.fichier].append(enigme)
    print(liste_pj) """

    context['enigmes_par_image'] = enigmes_par_image
    context['enigmes_par_fichier'] = enigmes_par_fichier

    print(context)

    return render(request, 'enigmes/mes_fichiers.html', context)


class EnigmeListView(LoginRequiredMixin, ListView):
    model = Enigme
    template_name = 'enigmes/liste.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'enigmes'
    ordering = ['date_creation']

    def get_context_data(self, **kwargs):
        # Appel à l'implémentation d'origine pour récupérer le contexte
        context = super().get_context_data(**kwargs)
        # Ajout au contexte
        context['titre'] = "Toutes les énigmes"
        context['enigmes_perso'] = False
        return context

class EnigmeDetailView(LoginRequiredMixin, DetailView):
    model = Enigme
    context_object_name = 'enigme'


class EnigmeCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Enigme
    context_object_name = 'enigme'
    form_class = EnigmeCreateForm
    success_message = "Votre énigme a bien été ajoutée à la base 😊"

    def get_form_kwargs(self):
        kwargs = super(EnigmeCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Ajoute l'auteur de l'énigme en bdd lors de la validation du formulaire"""
        form.instance.auteur = self.request.user
        return super().form_valid(form)

class EnigmeExampleCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Enigme
    template_name = 'enigmes/enigme_example_form.html'
    context_object_name = 'enigme'
    form_class = EnigmeExampleCreateForm
    
    def get_form_kwargs(self):
        kwargs = super(EnigmeExampleCreateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        return self.form_class.get_initial()

class EnigmeUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Enigme
    #fields = ['theme', 'enonce', 'reponse', 'indication', 'image', 'fichier']
    context_object_name = 'enigme'
    template_name_suffix = '_update_form'
    form_class = EnigmeUpdateForm
    success_message = "Les modifications ont bien été enregistrées 😊"

    def get_form_kwargs(self):
        kwargs = super(EnigmeUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def test_func(self):
        """Seul l'auteur d'une énigme peut la modifier"""
        enigme = self.get_object()
        return self.request.user == enigme.auteur

class EnigmeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Enigme
    context_object_name = 'enigme'
    success_url = '/enigmes'
    
    def test_func(self):
        """Seul l'auteur d'une énigme peut la supprimer"""
        enigme = self.get_object()
        return self.request.user == enigme.auteur

@login_required
def mes_enigmes(request):
    enigmes_perso = Enigme.objects.filter(auteur=request.user)
    context = {
        "enigmes": enigmes_perso,
        "titre": "Mes énigmes",
        "enigmes_perso": True
    }
    return render(request, 'enigmes/liste.html', context)

@login_required
def enquete(request, enquete_id):    
    enquete = get_object_or_404(Enquete, pk=enquete_id)
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                if 'activer' in request.POST:
                    if not enquete.active:
                        enquete.active = True
                        enquete.save()
                        messages.success(request, "L'enquête est maintenant activée.")
                elif 'desactiver' in request.POST:
                    if enquete.active:
                        enquete.active = False
                        enquete.save()
                        messages.success(request, "L'enquête est maintenant désactivée.")
                elif 'modifier' in request.POST:
                    if not enquete.active:
                        return redirect('enquete-modification', enquete_id=enquete.pk)
                    else:
                        messages.warning(request, "Attention, vous ne pouvez pas modifier l'enquête si elle est active. Commencez par désactiver l'enquête.")
                
                elif 'dupliquer' in request.POST:
                    enquete_id = int(request.POST.get('dupliquer'))
                    enquete = Enquete.objects.get(pk=enquete_id)
                    enigmes = enquete.enigmes.all()
                    nouvelle_description = f"Copie de {enquete.description[:91]}" if len(enquete.description) >= 91 else f"copie {enquete.description}"

                    nouvelle_enquete = Enquete.objects.create(
                        description = nouvelle_description,
                        indications = enquete.indications,
                        score = enquete.score,
                        correction = enquete.correction,
                        ordre_aleatoire = enquete.ordre_aleatoire,
                        auteur = enquete.auteur,
                        cle = enquete.cle
                    )
                    nouvelle_enquete.enigmes.set(enigmes)

                    nouvelle_enquete.save()
                    
                    messages.success(request, "L'enquête a bien été dupliquée.")
                    return redirect('espace-perso')

                elif 'supprimer' in request.POST:
                    return redirect('enquete-delete', enquete_id=enquete.pk)
                
                elif 'telecharger-csv' in request.POST:
                    response = enquete.genere_csv()
                    if response is not None:  # présence d'au moins un résultat
                        return response
                    else:
                        messages.warning(request, "Aucun résultat. Le fichier CSV n'a pas été généré.")
        except IntegrityError:
            messages.warning(request, "Une erreur interne est apparue. Merci de recommencer.")

    liste_enigmes = enquete.liste_enigmes_ordre_initial()
    
    liste_num_enigmes = enquete.liste_numeros_enigmes_ordre_initial()
    nb_resultats = Resultat.objects.filter(enquete=enquete).count()
    context = {
        "enquete": enquete,
        "enigmes": liste_enigmes,
        "num_enigmes": liste_num_enigmes,
        "nb_resultats": nb_resultats
    }
    return render(request, 'enigmes/enquete_detail.html', context)

class EnqueteCreateView(LoginRequiredMixin, CreateView):
    model = Enquete
    context_object_name = 'enquete'
    form_class = EnqueteCreateForm

    def form_valid(self, form):
        """Ajoute l'auteur de l'énigme en bdd lors de la validation du formulaire"""
        form.instance.auteur = self.request.user
        return super().form_valid(form)

@login_required
def creation_enquete(request):
    return render(request, 'enigmes/enquete_creation.html')

@login_required
def creation_enquete_manuelle(request):
    context = {
        "enigmes": Enigme.objects.all(),
        "titre": "Créer une enquête par sélection manuelle"
    }

    if request.method == 'POST':
        # création d'une instance de formulaire et remplissage avec les données saisies
        form = EnqueteCreateForm(request.POST)
        context['form'] = form
        
        # si le form est valide
        if form.is_valid():
            # recupération des données nettoyées du formulaire            
            donnees = form.cleaned_data
            description = donnees['description']
            indications = donnees['indications']
            correction = donnees['correction']
            score = donnees['score']
            ordre_aleatoire = donnees['ordre_aleatoire']
            enigmes = list(donnees['enigmes'])
            cle = donnees['cle']

            # Validation backend : longueur description et clé (cachée) valide
            if len(description) > 100:
                messages.warning(request, "La description est limitée à 100 caractères maximum.")
                return render(request, 'enigmes/enquete_update_form.html', context)

            if not cle_est_valide(cle)[0]:
                messages.warning(request, "Un problème est survenu. Les modificaiton n'ont pas été enregistrées.")
                return render(request, 'enigmes/enquete_update_form.html', context)
            
            liste_num_enigmes = cle.split(";")

            # validation backend de la sélection d'au moins une énigme et du champ description
            if enigmes == []:
                messages.warning(request, "Vous n'avez sélectionné aucune énigme. L'enquête n'a pas été enregistrée.")
                return render(request, 'enigmes/enquete_form.html', context)
            if enigmes == [] or description == "":
                messages.warning(request, "Veuillez sélectionner au moins une énigme et renseigner une description pour créer une enquête !")
                return render(request, 'enigmes/enquete_form.html', context)
            
            # sinon, si tout est bon
            else:
                try:
                    # Sauvegarde de l'enquete en bdd 
                    with transaction.atomic():
                        # Création d'une instance Enquete avec enregistrement de l'auteur
                        enquete = Enquete.objects.create(auteur = request.user)
                        
                        # Ajout des énigmes sélectionnées à l'enquete (relation ManyToMany)
                        try :
                            for num_enigme in liste_num_enigmes:
                                enigme = Enigme.objects.get(pk=int(num_enigme))  # génère une ValueError si num_enigme ne peut être converti en un entier ou Object.DoesNotExist si un numéro ne correspond à aucune enquête
                                enquete.enigmes.add(enigme)
                        except:  # si un problème est rencontré, on n'utilise pas la clé mais la liste ordonnée par ordre croissant des énigmes cochées
                            for enigme in enigmes:
                                enquete.enigmes.add(enigme)
                            liste_num_enigmes = [str(enigme.pk) for enigme in enigmes]  # et on modifie la liste des num d'énigmes (par ordre chrono)
                            messages.warning(request, "Une erreur s'est produite. L'enquête a tout de même été sauvegardée mais l'ordre des énigmes est l'ordre croissant des numéros.")
                        
                        
                        for enigme in enigmes:
                            enquete.enigmes.add(enigme)
                        
                        # Création et ajout de la clé
                        enquete.cle = ";".join(liste_num_enigmes)
                        # Ajout des autres champs
                        enquete.description = description
                        enquete.score = score or indications
                        enquete.indications = indications
                        enquete.correction = correction
                        enquete.ordre_aleatoire = ordre_aleatoire
                        
                        # Sauvegarde en base de données
                        enquete.save()
                        
                        messages.success(request, "L'enquête a bien été créée. Vous la trouverez dans le tableau de bord.")
                        return redirect('espace-perso')
                
                except IntegrityError:
                    messages.warning(request, "Une erreur interne est apparue. Merci de recommencer.")
                    return render(request, 'enigmes/enquete_form.html', context)
    else:
        form = EnqueteCreateForm()
    
    context['form'] = form
    return render(request, 'enigmes/enquete_form.html', context)

@login_required
def modification_enquete(request, enquete_id):
    enquete = get_object_or_404(Enquete, pk=enquete_id)
    code = enquete.code
    context = {
        'enquete': enquete,
        'code': code 
    }
    return render(request, 'enigmes/enquete_modification.html', context)

@login_required
def modification_enquete_manuelle(request, enquete_id):

    enquete = get_object_or_404(Enquete, pk=enquete_id)

    if request.user != enquete.auteur:
        raise PermissionDenied

    code_enquete = enquete.code

    if enquete.active:
        messages.warning(request, "Vous devez désactiver l'enquête pour pouvoir la modifier")
        return redirect('enquete-detail', enquete_id=enquete.pk)

    context = {
        "code": code_enquete,
        "enigmes": Enigme.objects.all(),
    }

    if request.method == 'POST':
        # création d'une instance de formulaire et remplissage avec les données saisies
        form = EnqueteUpdateForm(request.POST)
        context['form'] = form
        
        # si le form est valide
        if form.is_valid():
            # recupération des données nettoyées du formulaire         
            donnees = form.cleaned_data
            description = donnees['description']
            indications = donnees['indications']
            correction = donnees['correction']
            score = donnees['score']
            ordre_aleatoire = donnees['ordre_aleatoire']
            enigmes_enquete = list(donnees['enigmes'])
            cle = donnees['cle']
            
            # Validation backend : longueur description et clé (cachée) valide
            if len(description) > 100:
                messages.warning(request, "La description est limitée à 100 caractères maximum.")
                return render(request, 'enigmes/enquete_update_form.html', context)

            if not cle_est_valide(cle)[0]:
                messages.warning(request, "Un problème est survenu. Les modificaiton n'ont pas été enregistrées.")
                return render(request, 'enigmes/enquete_update_form.html', context)
            
            liste_num_enigmes = cle.split(";")

            # validation backend de la sélection d'au moins une énigme et du champ description
            if enigmes_enquete == []:
                messages.warning(request, "Vous n'avez sélectionné aucune énigme. Les modifications n'ont pas été enregistrées.")
                return render(request, 'enigmes/enquete_update_form.html', context)
            if enigmes_enquete == [] or description == "":
                messages.warning(request, "Veuillez sélectionner au moins une énigme et renseigner une description.")
                return render(request, 'enigmes/enquete_update_form.html', context)
            
            # sinon, si tout est bon
            else:
                try:
                    # Sauvegarde des modifications en bdd 
                    with transaction.atomic():
                        # on supprime les énigmes (m2m) d'origine
                        enquete.enigmes.clear()
                        # Ajout des énigmes sélectionnées à l'enquete (relation ManyToMany)
                        
                        
                        try :
                            for num_enigme in liste_num_enigmes:
                                enigme = Enigme.objects.get(pk=int(num_enigme))  # génère une ValueError si num_enigme ne peut être converti en un entier ou Object.DoesNotExist si un numéro ne correspond à aucune enquête
                                enquete.enigmes.add(enigme)
                        except:  # si un problème est rencontré, on n'utilise pas la clé mais la liste ordonnée par ordre croissant des énigmes cochées
                            for enigme in enigmes_enquete:
                                enquete.enigmes.add(enigme)
                            liste_num_enigmes = [str(enigme.pk) for enigme in enigmes_enquete]  # et on modifie la liste des num d'énigmes (par ordre chrono)
                            messages.warning(request, "Une erreur s'est produite. L'enquête a tout de même été sauvegardée mais l'ordre des énigmes est l'ordre croissant des numéros.")    
                        
                        # Autres modifications
                        enquete.cle = ";".join(liste_num_enigmes)
                        enquete.description = description
                        enquete.score = score or indications
                        enquete.indications = indications
                        enquete.correction = correction
                        enquete.ordre_aleatoire = ordre_aleatoire
                        
                        # Sauvegarde en base de données
                        enquete.save()
                        
                        messages.success(request, "L'enquête a bien été modifiée. Voici le détail !")
                        return redirect('enquete-detail', enquete_id=enquete.pk)
                
                except IntegrityError:
                    messages.warning(request, "Une erreur interne est apparue. Merci de recommencer.")
                    return render(request, 'enigmes/enquete_update_form.html', context)
    else:
        #enigmes_enquete = list(enquete.enigmes)
        form = EnqueteUpdateForm(
            initial={
                'description': enquete.description,
                'indications': enquete.indications,
                'correction': enquete.correction,
                'score': enquete.score,
                'ordre_aleatoire': enquete.ordre_aleatoire,
            }
        )
        context['enigmes_selectionnees'] = list(enquete.enigmes.all())
        context['cle_initiale'] = enquete.cle
    context['form'] = form
    return render(request, 'enigmes/enquete_update_form.html', context)


@login_required
def modification_enquete_liste(request, enquete_id):

    enquete = get_object_or_404(Enquete, pk=enquete_id)

    if request.user != enquete.auteur:
        raise PermissionDenied

    code_enquete = enquete.code

    if enquete.active:
        messages.warning(request, "Vous devez désactiver l'enquête pour pouvoir la modifier")
        return redirect('enquete-detail', enquete_id=enquete.pk)

    context = {
        "code": code_enquete,
    }

    if request.method == 'POST':
        # création d'une instance de formulaire et remplissage avec les données saisies
        form = EnqueteUpdateListForm(request.POST)
        context['form'] = form

        if 'apercu-enquete' in request.POST:  # si l'utilisateur veut juste un aperçu
            
            # On rend le champ description facultatif pour 
            form.fields['description'].required = False
        
            # si le formulaire est valide
            if form.is_valid():
                # recupération des données nettoyées du formulaire         
                donnees = form.cleaned_data
                cle_entree = donnees['cle']
                cle_nettoyee = cle_entree.replace(" ", "")  # suppression des espaces éventuels

                if not cle_est_valide(cle_nettoyee)[0]:
                    messages.warning(request, "Un problème est survenu. Les modifications n'ont pas été enregistrées.")
                    return render(request, 'enigmes/enquete_update_form_cle.html', context)
                
                liste_num_enigmes = cle_nettoyee.split(";")

                # on construit la liste d'énigmes correspond à la clé (si la clé est valide)
                liste_enigmes = []
                                            
                try :
                    for num_enigme in liste_num_enigmes:
                        enigme = Enigme.objects.get(pk=int(num_enigme))  # génère une ValueError si num_enigme ne peut être converti en un entier ou Object.DoesNotExist si un numéro ne correspond à aucune enquête
                        liste_enigmes.append(enigme)
                except ValueError:
                    messages.warning(request, "Le format de la clé saisie (" + cle_entree + ") n'est pas valide. Vérifiez que les numéros des énignes sont bien des entiers.")
                    return render(request, 'enigmes/enquete_update_form_cle.html', context)
                except Enigme.DoesNotExist:
                    messages.warning(request, "La clé saisie (" + cle_entree + ") n'est pas valide car au moins un numéro fait référence à une énigme qui n'existe pas.")
                    return render(request, 'enigmes/enquete_update_form_cle.html', context)
                except IntegrityError:
                    messages.warning(request, "Une erreur interne est apparue. Merci de recommencer.")
                    return render(request, 'enigmes/enquete_update_form_cle.html', context)

                # on ajoute cette liste au contexte                    
                context['enigmes'] = liste_enigmes
                
                # on remet le champ description comme obligatoire avant de renvoyer le form au template
                form.fields['description'].required = True
                context['form'] = form
                return render(request, 'enigmes/enquete_update_form_cle.html', context)

        else:  # si sauvegarde en bdd
                        
            # si le formulaire est valide
            if form.is_valid():
                donnees = form.cleaned_data
                cle_entree = donnees['cle']
                description = donnees['description']
                indications = donnees['indications']
                correction = donnees['correction']
                score = donnees['score']
                ordre_aleatoire = donnees['ordre_aleatoire']
                cle_nettoyee = cle_entree.replace(" ", "")  # suppression des espaces éventuels
                
                # Validation backend : longueur description et clé valide
                if len(description) > 100:
                    messages.warning(request, "La description est limitée à 100 caractères maximum.")
                    return render(request, 'enigmes/enquete_update_form_cle.html', context)
                if not cle_est_valide(cle_nettoyee)[0]:
                    messages.warning(request, "Le format de la clé saisie (" + cle_entree + ") n'est pas valide : {}".format(" ; ".join(cle_est_valide(cle_nettoyee)[1])))
                    return render(request, 'enigmes/enquete_update_form_cle.html', context)
               
                # si tout est bon                    
                liste_num_enigmes = cle_nettoyee.split(";")
                try:
                    with transaction.atomic():

                        # on supprime les énigmes (m2m) d'origine
                        enquete.enigmes.clear()
                        # Ajout des énigmes sélectionnées à l'enquete (relation ManyToMany)
                        
                        try :
                            for num_enigme in liste_num_enigmes:
                                enigme = Enigme.objects.get(pk=int(num_enigme))  # génère une ValueError si num_enigme ne peut être converti en un entier ou Object.DoesNotExist si un numéro ne correspond à aucune enquête
                                enquete.enigmes.add(enigme)
                        except ValueError:
                            messages.warning(request, "Le format de la clé saisie (" + cle_entree + ") n'est pas valide. Vérifiez que les numéros des énignes sont bien des entiers.")
                            return render(request, 'enigmes/enquete_form_cle.html', context)
                        except Enigme.DoesNotExist:
                            messages.warning(request, "La clé saisie (" + cle_entree + ") n'est pas valide car au moins un numéro fait référence à une énigme qui n'existe pas.")
                            return render(request, 'enigmes/enquete_form_cle.html', context)
                        
                        enquete.cle = cle_nettoyee
                        enquete.description = description
                        enquete.score = score or indications
                        enquete.indications = indications
                        enquete.correction = correction
                        enquete.ordre_aleatoire = ordre_aleatoire
                        enquete.save()
                        messages.success(request, "L'enquête a bien été modifiée. Voici le détail !")
                        return redirect('enquete-detail', enquete_id=enquete.pk)
                
                except IntegrityError:
                    messages.warning(request, "Une erreur interne est apparue. Merci de recommencer.")

                
    else:
        #enigmes_enquete = list(enquete.enigmes)
        form = EnqueteUpdateListForm(
            initial={
                'cle': enquete.cle,
                'description': enquete.description,
                'indications': enquete.indications,
                'correction': enquete.correction,
                'score': enquete.score,
                'ordre_aleatoire': enquete.ordre_aleatoire,
            }
        )
        context['enigmes'] = enquete.liste_enigmes_ordre_initial()
    context['form'] = form
    return render(request, 'enigmes/enquete_update_form_cle.html', context)


def cle_est_valide(cle):
    '''Renvoie (True,) si la clé est valide et (False, errors) sinon,
    où errors est une liste de messages d'erreurs
    Une clé valide est au format <int>;<int>;<int>;...'''
    valide = True
    errors = []
    if " " in cle:
        valide = False
        errors.append("Il ne faut pas d'espace dans la clé")
    carac_acceptes = "0123456789;"
    for c in cle:
        if c not in carac_acceptes:
            valide = False
            errors.append('le caractère " {} " n\'est pas accepté'.format(c))
    liste_num = cle.split(";")
    num_cle = set()
    for c in liste_num:
        if c not in num_cle:
            num_cle.add(c)
        else:
            valide = False
            errors.append('le numéro {} est présent plusieurs fois dans la clé'.format(c))
    if valide:
        return (True,)
    else:
        return (False, errors)

@login_required
def creation_enquete_liste(request):

    # Si le formulaire est validé
    if request.method == 'POST':
        form = EnqueteCreateListForm(request.POST)
        if 'apercu-enquete' in request.POST:  # si on veut juste un aperçu
            if 'cle' in request.POST:
                context = {'form': form}
                form.fields['description'].required = False  # le champ description n'est pas obligatoire pour un apercu
                
                if form.is_valid():
                    donnees = form.cleaned_data
                    cle_entree = donnees['cle']
                    cle_nettoyee = cle_entree.replace(" ", "")  # suppression des espaces éventuels
                    
                    if not cle_est_valide(cle_nettoyee)[0]:
                        messages.warning(request, "Le format de la clé saisie (" + cle_entree + ") n'est pas valide : {}".format(" ; ".join(cle_est_valide(cle_nettoyee)[1])))
                    liste_num_enigmes = cle_nettoyee.split(";")
                    
                    # on construit la liste d'énigmes correspond à la clé (si la clé est valide)
                    liste_enigmes = []
                                                
                    try :
                        for num_enigme in liste_num_enigmes:
                            enigme = Enigme.objects.get(pk=int(num_enigme))  # génère une ValueError si num_enigme ne peut être converti en un entier ou Object.DoesNotExist si un numéro ne correspond à aucune enquête
                            liste_enigmes.append(enigme)
                    except ValueError:
                        messages.warning(request, "Le format de la clé saisie (" + cle_entree + ") n'est pas valide. Vérifiez que les numéros des énignes sont bien des entiers.")
                        return render(request, 'enigmes/enquete_form_cle.html', context)
                    except Enigme.DoesNotExist:
                        messages.warning(request, "La clé saisie (" + cle_entree + ") n'est pas valide car au moins un numéro fait référence à une énigme qui n'existe pas.")
                        return render(request, 'enigmes/enquete_form_cle.html', context)
                    except IntegrityError:
                        messages.warning(request, "Une erreur interne est apparue. Merci de recommencer.")
                        return render(request, 'enigmes/enquete_form_cle.html', context)

                    # on ajoute cette liste au contexte                    
                    context['enigmes'] = liste_enigmes
                    
                    # on remet le champ description comme obligatoire avant de renvoyer le form au template
                    form.fields['description'].required = True
                    context['form'] = form
                    return render(request, 'enigmes/enquete_form_cle.html', context)

        else:  # sinon si on veut sauvegarder l'enquête en bdd
            # création d'une instance de formulaire et remplissage avec les données saisies
            form = EnqueteCreateListForm(request.POST)
            context = {'form': form}
            
            # si le form est valide
            if form.is_valid():
                donnees = form.cleaned_data
                cle_entree = donnees['cle']
                description = donnees['description']
                indications = donnees['indications']
                correction = donnees['correction']
                score = donnees['score']
                ordre_aleatoire = donnees['ordre_aleatoire']
                cle_nettoyee = cle_entree.replace(" ", "")  # suppression des espaces éventuels
                
                if len(description) > 100:
                    messages.warning(request, "La description est limitée à 100 caractères maximum.")
                
                if not cle_est_valide(cle_nettoyee)[0]:
                    messages.warning(request, "Le format de la clé saisie (" + cle_entree + ") n'est pas valide : {}".format(" ; ".join(cle_est_valide(cle_nettoyee)[1])))
                liste_num_enigmes = cle_nettoyee.split(";")
                
                try:
                    with transaction.atomic():
                        
                        enquete = Enquete.objects.create(auteur = request.user)
                        
                        try :
                            for num_enigme in liste_num_enigmes:
                                enigme = Enigme.objects.get(pk=int(num_enigme))  # génère une ValueError si num_enigme ne peut être converti en un entier ou Object.DoesNotExist si un numéro ne correspond à aucune enquête
                                enquete.enigmes.add(enigme)
                        except ValueError:
                            messages.warning(request, "Le format de la clé saisie (" + cle_entree + ") n'est pas valide. Vérifiez que les numéros des énignes sont bien des entiers.")
                            return render(request, 'enigmes/enquete_form_cle.html', context)
                        except Enigme.DoesNotExist:
                            messages.warning(request, "La clé saisie (" + cle_entree + ") n'est pas valide car au moins un numéro fait référence à une énigme qui n'existe pas.")
                            return render(request, 'enigmes/enquete_form_cle.html', context)
                        
                        enquete.cle = cle_nettoyee
                        enquete.description = description
                        enquete.score = score or indications
                        enquete.indications = indications
                        enquete.correction = correction
                        enquete.ordre_aleatoire = ordre_aleatoire
                        enquete.save()
                        messages.success(request, "L'enquête a bien été créée. Vous la trouverez dans le tableau de bord.")
                        return redirect('espace-perso')
                
                except IntegrityError:
                    messages.warning(request, "Une erreur interne est apparue. Merci de recommencer.")
    
    # si requête GET, le formulaire est vide
    else:
        form = EnqueteCreateListForm()
        
    context = {'form': form}
    return render(request, 'enigmes/enquete_form_cle.html', context)

@login_required
def partage_enquete(request, code_enquete):
    # Si le formulaire est validé
    if request.method == 'POST':
        enquete_a_copier = get_object_or_404(Enquete, code=code_enquete)
        form = EnqueteShareForm(request.POST)
        context = {'form': form}
        
        if form.is_valid():
            
            donnees = form.cleaned_data
            description = donnees['description']
            indications = donnees['indications']
            correction = donnees['correction']
            score = donnees['score']
            ordre_aleatoire = donnees['ordre_aleatoire']

            try:
                with transaction.atomic():
                    enquete = Enquete.objects.create(auteur = request.user)

                    enquete.description = description
                    enquete.indications = indications
                    enquete.correction = correction
                    enquete.score = score
                    enquete.ordre_aleatoire = ordre_aleatoire
                    enquete.enigmes.set(enquete_a_copier.enigmes.all())
                    enquete.cle = enquete_a_copier.cle
                    enquete.save()
                    
                    messages.success(request, "L'enquête a bien été copiée sur votre compte. La voici !")
                    return redirect('enquete-detail', enquete_id=enquete.pk)

            except IntegrityError:
                    messages.warning(request, "Une erreur interne est apparue. Merci de recommencer.")
    # Si requête GET
    else:
        try:
            enquete_a_copier = Enquete.objects.get(code=code_enquete)
        # Si l'enquête n'existe pas
        except Enquete.DoesNotExist:
            messages.warning(request, "Le code saisi ne correspond à aucune enquête.")
            return redirect('espace-perso')    

        form = EnqueteShareForm(instance=enquete_a_copier)
        context = {'form': form}
        context['code'] = code_enquete
        context['cle'] = enquete_a_copier.cle
        context['enigmes'] = enquete_a_copier.liste_enigmes_ordre_initial()
            
    return render(request, 'enigmes/enquete_partage.html', context)

@login_required
def partage_enquete_v0(request, code_enquete):
    # Si le formulaire est validé
    if request.method == 'POST':
        # création d'une instance de formulaire et remplissage avec les données saisies
        form = EnqueteShareForm(request.POST)
        context = {'form': form}
        # si le form est valide
        if form.is_valid():
            # si l'utilisateur veut un aperçu de l'enquete
            if 'apercu-enquete' in request.POST:
                donnees = form.cleaned_data    
                cle_entree = donnees['cle']
                enquete_a_copier = Enquete.objects.get(code=code_enquete)
                if enquete_a_copier.cle == cle_entree:
                    context['enigmes'] = enquete_a_copier.liste_enigmes_ordre_initial()
                    return render(request, 'enigmes/enquete_partage.html', context)
                else:
                    cle_nettoyee = cle_entree.replace(" ", "")  # suppression des espaces éventuels
                    if not cle_est_valide(cle_nettoyee)[0]:
                        messages.warning(request, "Le format de la clé saisie (" + cle_entree + ") n'est pas valide : {}".format(" ; ".join(cle_est_valide(cle_nettoyee)[1])))
                    liste_num_enigmes = cle_nettoyee.split(";")
                    liste_enigmes = []
                    try:
                        with transaction.atomic():                            
                            try :
                                for num_enigme in liste_num_enigmes:
                                    enigme = Enigme.objects.get(pk=int(num_enigme))  # génère une ValueError si num_enigme ne peut être converti en un entier ou Object.DoesNotExist si un numéro ne correspond à aucune enquête
                                    liste_enigmes.append(enigme)
                            except ValueError:
                                messages.warning(request, "Le format de la clé saisie (" + cle_entree + ") n'est pas valide. Vérifiez que les numéros des énignes sont bien des entiers.")
                                return render(request, 'enigmes/enquete_partage.html', context)
                            except Enigme.DoesNotExist:
                                messages.warning(request, "La clé saisie (" + cle_entree + ") n'est pas valide car au moins un numéro fait référence à une énigme qui n'existe pas.")
                                return render(request, 'enigmes/enquete_partage.html', context)

                            context['enigmes'] = liste_enigmes
                            
                    except IntegrityError:
                        messages.warning(request, "Une erreur interne est apparue. Merci de recommencer.")
                return render(request, 'enigmes/enquete_partage.html', context)
            
            
            # sinon, s'il a validé la clé            
            else:
                donnees = form.cleaned_data    
                cle_entree = donnees['cle']
                cle_nettoyee = cle_entree.replace(" ", "")  # suppression des espaces éventuels
                
                if not cle_est_valide(cle_nettoyee)[0]:
                    messages.warning(request, "Le format de la clé saisie (" + cle_entree + ") n'est pas valide : {}".format(" ; ".join(cle_est_valide(cle_nettoyee)[1])))
                liste_num_enigmes = cle_nettoyee.split(";")
                
                try:
                    with transaction.atomic():
                        
                        enquete = Enquete.objects.create(auteur = request.user)
                        
                        try :
                            for num_enigme in liste_num_enigmes:
                                enigme = Enigme.objects.get(pk=int(num_enigme))  # génère une ValueError si num_enigme ne peut être converti en un entier ou Object.DoesNotExist si un numéro ne correspond à aucune enquête
                                enquete.enigmes.add(enigme)
                        except ValueError:
                            messages.warning(request, "Le format de la clé saisie (" + cle_entree + ") n'est pas valide. Vérifiez que les numéros des énignes sont bien des entiers.")
                            return render(request, 'enigmes/enquete_partage.html', context)
                        except Enigme.DoesNotExist:
                            messages.warning(request, "La clé saisie (" + cle_entree + ") n'est pas valide car au moins un numéro fait référence à une énigme qui n'existe pas.")
                            return render(request, 'enigmes/enquete_partage.html', context)
                        
                        form = EnqueteShareListForm(initial = {'cle': cle_nettoyee})
                        context = {'form': form}
                        
                        messages.success(request, "L'enquête a bien été créée. Vous la trouverez dans le tableau de bord.")
                        return redirect('espace-perso')
                
                except IntegrityError:
                    messages.warning(request, "Une erreur interne est apparue. Merci de recommencer.")
    else:
        try:
            enquete_a_copier = Enquete.objects.get(code=code_enquete)
        except Enquete.DoesNotExist:
            enquete_a_copier = None
        
        # Si l'enquête n'existe pas
        if enquete_a_copier == None :
            messages.warning(request, "Le code saisi ne correspond à aucune enquête.")
            return redirect('espace-perso')
        else:
            cle = enquete_a_copier.cle
            form = EnqueteShareForm(initial = {'cle': cle})
            context = {'form': form}
            context['enigmes'] = enquete_a_copier.liste_enigmes_ordre_initial()
            
    return render(request, 'enigmes/enquete_partage.html', context)

@login_required
def espace_perso(request):
    user = request.user

    if request.method == 'POST':
        try:
            with transaction.atomic():
                if 'activer' in request.POST:
                    enquete_id = int(request.POST.get('activer'))
                    enquete = Enquete.objects.get(pk=enquete_id)
                    enquete.active = True
                    enquete.save()
                    messages.success(request, "L'enquête de code {} a bien été activée.".format(enquete.code))
                elif 'desactiver' in request.POST:
                    enquete_id = int(request.POST.get('desactiver'))
                    enquete = Enquete.objects.get(pk=enquete_id)
                    enquete.active = False
                    enquete.save()
                    messages.success(request, "L'enquête de code {} a bien été désactivée.".format(enquete.code))
                elif 'modifier' in request.POST:
                    enquete_id = int(request.POST.get('modifier'))
                    enquete = Enquete.objects.get(pk=enquete_id)
                    if enquete.active:
                        messages.warning(request, f"Vous devez désactiver l'enquête de code {enquete.code} avant de pouvoir la modifier.")
                    else:
                        return redirect('enquete-modification', enquete_id=enquete.pk)
                elif 'dupliquer' in request.POST:
                    enquete_id = int(request.POST.get('dupliquer'))
                    enquete = Enquete.objects.get(pk=enquete_id)
                    enigmes = enquete.enigmes.all()
                    nouvelle_description = f"Copie de {enquete.description[:91]}" if len(enquete.description) >= 91 else f"copie {enquete.description}"

                    nouvelle_enquete = Enquete.objects.create(
                        description = nouvelle_description,
                        indications = enquete.indications,
                        score = enquete.score,
                        correction = enquete.correction,
                        ordre_aleatoire = enquete.ordre_aleatoire,
                        auteur = enquete.auteur,
                        cle = enquete.cle
                    )
                    nouvelle_enquete.enigmes.set(enigmes)

                    nouvelle_enquete.save()
                    
                    messages.success(request, "L'enquête a bien été dupliquée.")
                elif 'telecharger-csv' in request.POST:
                    enquete_id = int(request.POST.get('telecharger-csv'))
                    enquete = Enquete.objects.get(pk=enquete_id)
                    response = enquete.genere_csv()
                    if response is not None:  # présence d'au moins un résultat
                        return response
                    else:
                        messages.warning(request, "Aucun résultat. Le fichier CSV n'a pas été généré.")


        except IntegrityError:
            messages.warning(request, "Une erreur interne est apparue. Merci de recommencer.")
        
    enigmes_perso = Enigme.objects.filter(auteur=user)
    enquetes_perso = Enquete.objects.filter(auteur=user).order_by('-date_creation')
    
    context = {
        "auteur": user,
        "enigmes_perso" : enigmes_perso,
        "enquetes_perso" : enquetes_perso
    }
    return render(request, 'enigmes/espace_perso.html', context)

@login_required
def enquete_informations(request):
    return render(request, 'enigmes/informations.html')


@login_required
def suppression_enquete(request, enquete_id):
    enquete = get_object_or_404(Enquete, pk=enquete_id)
    context = {"enquete": enquete}
    
    # Une enquête ne peut être supprimée que par son auteur
    if request.user != enquete.auteur:
        messages.warning(request, "Vous ne pouvez pas supprimer une enquête dont vous n'êtes pas l'auteur.")

    # Si l'utilisateur valide la suppression
    if request.method == 'POST':
        enquete.delete()
        messages.success(request, "L'enquête a bien été supprimée.")
        return redirect('espace-perso')
    
    return render(request, 'enigmes/enquete_confirm_delete.html', context)
    

def eleve(request, code_enquete):
    try:
        enquete = Enquete.objects.get(code=code_enquete)
    except Enquete.DoesNotExist:
        enquete = None
    if enquete is None:
        messages.warning(request, "Ce code est incorrect")
        return redirect('index')
    
    # Si l'enquête n'est pas active
    if enquete.active == False:
        messages.warning(request, "L'enquête n'est pas activée par le professeur.")
        return redirect('index')
    

    if not enquete.ordre_aleatoire:
        liste_enigmes = enquete.liste_enigmes_ordre_initial()
    else:
        liste_enigmes = enquete.liste_enigmes()
    context = {
        "enquete": enquete,
        "enigmes": liste_enigmes,
    }

    if request.method == 'POST':
        try:
            form = EnqueteEleveForm(request.POST, enigmes=liste_enigmes)
            context['form'] = form
            if form.is_valid():
                donnees = form.cleaned_data
                identifiant_eleve = donnees['id_eleve']
                # recupération des réponses
                liste_num_enigmes = enquete.liste_numeros_enigmes()  # liste de int
                # construction du champ "reponses" du modèle
                dic_reponses = {num: donnees[str(num)] for num in liste_num_enigmes}
                # enregistrement
                resultat = Resultat.objects.create(
                    enquete=enquete,
                    id_eleve=identifiant_eleve,
                    reponses=str(dic_reponses) 
                )
                # si réponses affichées
                if enquete.correction or enquete.score:
                    context['reponses'] = dic_reponses
                    context['score'] = resultat.calcul_score()
                    context['correction'] =  resultat.bonnes_mauvaises_reponses()
                    return render(request, 'enigmes/enquete_eleve_reponses.html', context)
                # sinon redirection vers remerciements
                
                else:
                    return render(request, 'enigmes/enquete_eleve_remerciements.html', context)
        except:
            messages.error(request, "Une erreur interne s'est produite. Les réponses n'ont pas été envoyées.")
    else:
        form = EnqueteEleveForm(enigmes=liste_enigmes)
        context['form'] = form
    return render(request, 'enigmes/enquete_eleve.html', context)

@login_required
def resultats_enquete(request, enquete_id):
    enquete = get_object_or_404(Enquete, pk=enquete_id)
    liste_enigmes = enquete.liste_enigmes_ordre_initial()
    liste_num_enigmes = enquete.liste_numeros_enigmes_ordre_initial()
    liste_resultats = Resultat.objects.filter(enquete=enquete)
    liste_complete = [resultat.dico_complet() for resultat in liste_resultats]
    
    nb_bonnes_reponses = {num_enigmes: 0 for num_enigmes in liste_num_enigmes}
    for dico_resultat in liste_complete:
        for enigme in dico_resultat["reponses"]:
            if dico_resultat["reponses"][enigme]["correct"]:
                nb_bonnes_reponses[enigme] = nb_bonnes_reponses[enigme] + 1
    if len(liste_resultats) != 0:
        pourcentage_bonnes_reponses = {num_enigmes: round(nb_bonnes_reponses[num_enigmes]/len(liste_resultats)*100) for num_enigmes in nb_bonnes_reponses}
    else:
        pourcentage_bonnes_reponses = {num_enigmes: 0 for num_enigmes in nb_bonnes_reponses}
    
    context = {
            "enquete": enquete,
            "num_enigmes": liste_num_enigmes,
            "enigmes": liste_enigmes,
            "reponses": liste_resultats,
            "resultats": liste_complete,
            "pourcentage": pourcentage_bonnes_reponses
        }
    # gestion du fetch pour actualiser les résultats
    if request.method == 'POST':
        if "maj" in request.POST:
            response = {
                "resultats": liste_complete,
                "pourcentage": pourcentage_bonnes_reponses,
                "enigmes": liste_num_enigmes
            }
            return JsonResponse(response)
        elif 'telecharger-csv' in request.POST:
            response = enquete.genere_csv()
            if response is not None:  # présence d'au moins un résultat
                return response
            else:
                messages.warning(request, "Aucun résultat. Le fichier CSV n'a pas été généré.")
    return render(request, 'enigmes/enquete_resultats.html', context)  
        
