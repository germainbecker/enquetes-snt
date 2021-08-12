from django.http.response import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.db import transaction, IntegrityError

from .forms import CustomClearableFileInput, EnqueteCreateForm, EnigmeUpdateForm, EnigmeCreateForm
from .models import Enigme, Enquete, Resultat
from django.http import HttpResponse
import csv

def index(request):
    context = {
        "nav": "nav_mini"
    }

    # Si le formulaire est validé
    if request.method == 'POST':
        print(request.POST)
        code_enquete = request.POST.get('code')

        try:
            enquete = Enquete.objects.get(code=code_enquete)
        except Enquete.DoesNotExist:
            enquete = None
        
        # Si l'enquête n'existe pas
        if enquete == None :
            messages.warning(request, "Le code ne correspond à aucune enquête.")
            return render(request, 'enigmes/index.html', context = {})
        
        # Si l'enquête n'est pas activée
        if enquete.active == False:
            messages.warning(request, "L'enquête n'est pas activée par le professeur.")
            return render(request, 'enigmes/index.html', context = {})
    
        else:
            return redirect('enquete-eleve', code_enquete=code_enquete)
    
    return render(request, 'enigmes/index.html', context)

def enseignants(request):
    if request.user.is_authenticated:
        return redirect('accueil')
    else:
        return render(request, 'enseignants/enseignants.html', {"nav": "nav_complete"})

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

class EnigmeListView(LoginRequiredMixin, ListView):
    model = Enigme
    template_name = 'enigmes/liste.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'enigmes'
    ordering = ['date_creation']

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['titre'] = "Toutes les énigmes"
        context['enigmes_perso'] = False
        return context

class EnigmeDetailView(LoginRequiredMixin, DetailView):
    model = Enigme
    context_object_name = 'enigme'

class EnigmeCreateView(LoginRequiredMixin, CreateView):
    model = Enigme
    context_object_name = 'enigme'
    form_class = EnigmeCreateForm

    def form_valid(self, form):
        """Ajoute l'auteur de l'énigme en bdd lors de la validation du formulaire"""
        form.instance.auteur = self.request.user
        return super().form_valid(form)

class EnigmeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Enigme
    #fields = ['theme', 'enonce', 'reponse', 'indication', 'image', 'fichier']
    context_object_name = 'enigme'
    template_name_suffix = '_update_form'
    form_class = EnigmeUpdateForm

    def form_valid(self, form):
        """Ajoute l'auteur de l'énigme en bdd lors de la validation"""
        form.instance.auteur = self.request.user
        return super().form_valid(form)
    
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

""" class EnqueteDetailView(LoginRequiredMixin, DetailView):
    model = Enquete
    context_object_name = 'enquete'
    template_name = 'enigmes/enquete_detail.html' """

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
                elif 'activer-indications' in request.POST:
                    if not enquete.active:
                        enquete.indications = True
                        enquete.save()
                        messages.success(request, "Les indications seront affichées (si elles existent).")
                    else:
                        messages.warning(request, "Attention, vous ne pouvez pas modifier ce paramètre si l'enquête est active. Commencez par désactiver l'enquête.")
                elif 'desactiver-indications' in request.POST:
                    if not enquete.active:
                        enquete.indications = False
                        enquete.save()
                        messages.success(request, "Les indications ne seront pas affichées (si elles existent).")
                    else:
                        messages.warning(request, "Attention, vous ne pouvez pas modifier ce paramètre si l'enquête est active. Commencez par désactiver l'enquête.")
                elif 'activer-correction' in request.POST:
                    if not enquete.active:
                        enquete.correction = True
                        enquete.score = True
                        enquete.save()
                        messages.success(request, "Modification enregistrée ! Les élèves auront accès à la correction à la fin de l'enquête. Le score est aussi par défaut activé dans ce cas.")
                    else:
                        messages.warning(request, "Attention, vous ne pouvez pas modifier ce paramètre si l'enquête est active. Commencez par désactiver l'enquête.")
                elif 'desactiver-correction' in request.POST:
                    if not enquete.active:
                        enquete.correction = False
                        enquete.save()
                        messages.success(request, "Modification enregistrée ! Les élèves n'auront pas accès à la correction à la fin de l'enquête.")
                    else:
                        messages.warning(request, "Attention, vous ne pouvez pas modifier ce paramètre si l'enquête est active. Commencez par désactiver l'enquête.")
                elif 'activer-score' in request.POST:
                    if not enquete.active:
                        enquete.score = True
                        enquete.save()
                        messages.success(request, "Modification enregistrée ! Les élèves connaîtront leur score à la fin de l'enquête.")
                    else:
                        messages.warning(request, "Attention, vous ne pouvez pas modifier ce paramètre si l'enquête est active. Commencez par désactiver l'enquête.")
                elif 'desactiver-score' in request.POST:
                    if not enquete.active:
                        if enquete.correction:
                            enquete.score = True
                            enquete.save()
                            messages.warning(request, "Vous ne pouvez pas désactiver l'affichage du score car la correction est activée.")
                        else:
                            enquete.score = False
                            enquete.save()
                            messages.success(request, "Modification enregistrée ! Les élèves ne connaîtront pas leur score à la fin de l'enquête.")
                    else:
                        messages.warning(request, "Attention, vous ne pouvez pas modifier ce paramètre si l'enquête est active. Commencez par désactiver l'enquête.")
                elif 'activer-ordre-aleatoire' in request.POST:
                    if not enquete.active:
                        enquete.ordre_aleatoire = True
                        enquete.save()
                        messages.success(request, "Modification enregistrée ! Les questions seront données dans un ordre aléatoire.")
                    else:
                        messages.warning(request, "Attention, vous ne pouvez pas modifier ce paramètre si l'enquête est active. Commencez par désactiver l'enquête.")
                elif 'desactiver-ordre-aleatoire' in request.POST:
                    if not enquete.active:
                        enquete.ordre_aleatoire = False
                        enquete.save()
                        messages.success(request, "Modification enregistrée ! Les questions ne seront pas données dans un ordre aléatoire.")
                    else:
                        messages.warning(request, "Attention, vous ne pouvez pas modifier ce paramètre si l'enquête est active. Commencez par désactiver l'enquête.")

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
    #fields = ['description', 'enigmes']
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
    
    # Si la vue intercepte le formulaire complété (méthode POST)
    if request.method == 'POST':
        if 'enigmes' not in request.POST:
            messages.warning(request, "Vous n'avez sélectionné aucune énigme. L'enquête n'a pas été enregistrée.")
            return render(request, 'enigmes/enquete_form.html', context)
        else:
            liste_num_enigmes = request.POST.getlist('enigmes')
            description = request.POST.get('description')
            indications = request.POST.get('choix_indications')
            score = request.POST.get('choix_score')
            correction = request.POST.get('choix_correction')
            ordre = request.POST.get('choix_ordre')
            if liste_num_enigmes == [] or description == "":
                context['erreur'] = "Veuillez sélectionner au moins une énigme et renseigner une description pour créer une enquête !" 
            else:
                try:
                    with transaction.atomic():
                        enquete = Enquete.objects.create(auteur = request.user)
                        for num_enigme in liste_num_enigmes:
                            enigme = Enigme.objects.get(pk=int(num_enigme))
                            enquete.enigmes.add(enigme)
                        enquete.cle = ";".join(liste_num_enigmes)
                        enquete.description = description
                        enquete.score = True if score == "oui" or indications == "oui" else False
                        enquete.indications = True if indications == "oui" else False
                        enquete.correction = True if correction == "oui" else False
                        enquete.ordre_aleatoire = True if ordre == "oui" else False
                        enquete.save()
                        return redirect('espace-perso')
                except IntegrityError:
                    messages.warning(request, "Une erreur interne est apparue. Merci de recommencer.")

    return render(request, 'enigmes/enquete_form.html', context)

@login_required
def creation_enquete_liste(request): 
    if request.method == 'POST':
        cle_entree = request.POST.get('cle')
        description = request.POST.get('description')
        indications = request.POST.get('choix_indications')
        correction = request.POST.get('choix_correction')
        ordre = request.POST.get('choix_ordre')
        cle_nettoyee = cle_entree.replace(" ", "")  # suppression des espaces
        liste_num_enigmes = cle_nettoyee.split(";")
        print(liste_num_enigmes)
        try:
            with transaction.atomic():
                enquete = Enquete.objects.create(auteur = request.user)
                for num_enigme in liste_num_enigmes:
                    enigme = Enigme.objects.get(pk=int(num_enigme))
                    enquete.enigmes.add(enigme)
                enquete.cle = cle_nettoyee
                enquete.description = description
                enquete.indications = True if indications == "oui" else False
                enquete.correction = True if correction == "oui" else False
                enquete.ordre_aleatoire = True if ordre == "oui" else False
                enquete.save()
                messages.success(request, "L'enquête a bien été créée.")
                return redirect('espace-perso')
        except Enigme.DoesNotExist:
            messages.warning(request, "Une erreur est détectée dans la clé saisie : " + cle_entree + ". Vérifiez que les numéros existent bien, qu'ils sont séparés par des point-virgules, qu'il n'y a pas d'espace, ...")
        except IntegrityError:
                messages.warning(request, "Une erreur interne est apparue. Merci de recommencer.")

    return render(request, 'enigmes/enquete_form_cle.html')

@login_required
def espace_perso(request):
    user = request.user
    if request.method == 'POST':
        if 'activer' in request.POST:
            enquete_id = int(request.POST.get('activer'))
            enquete = Enquete.objects.get(pk=enquete_id)
            enquete.active = True
            enquete.save()
        elif 'desactiver' in request.POST:
            enquete_id = int(request.POST.get('desactiver'))
            enquete = Enquete.objects.get(pk=enquete_id)
            enquete.active = False
            enquete.save()
        elif 'supprimer' in request.POST:
            enquete_id = int(request.POST.get('supprimer'))
            enquete = Enquete.objects.get(pk=enquete_id)
            return redirect('enquete-delete', enquete_id=enquete_id)
    context = {
        "auteur": user,
        "enigmes_perso" : Enigme.objects.filter(auteur=user),
        "enquetes_perso" : Enquete.objects.filter(auteur=user).order_by('-date_creation'),
    }
    return render(request, 'enigmes/espace_perso.html', context)

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
    enquete = get_object_or_404(Enquete, code=code_enquete)
    print(enquete)
    # Si l'enquête n'est pas active
    if enquete.active == False:
        messages.warning(request, "L'enquête n'est pas activée par le professeur.")
        return redirect('index')

    if not enquete.ordre_aleatoire:
        liste_enigmes = enquete.liste_enigmes_ordre_initial()
        print(liste_enigmes)
    else:
        liste_enigmes = enquete.liste_enigmes()
        print(liste_enigmes)
    
    context = {
        "enquete": enquete,
        "enigmes": liste_enigmes
    }

    # si le formulaire est validé
    if request.method == 'POST':
        donnees = request.POST
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


    return render(request, 'enigmes/enquete_eleve.html', context)

@login_required
def resultats_enquete(request, enquete_id):
    enquete = get_object_or_404(Enquete, pk=enquete_id)
    liste_enigmes = enquete.liste_enigmes_ordre_initial()
    liste_num_enigmes = enquete.liste_numeros_enigmes_ordre_initial()
    liste_resultats = Resultat.objects.filter(enquete=enquete)
    liste_complete = [resultat.dico_complet() for resultat in liste_resultats]
    
    nb_bonnes_reponses = {num_enigmes: 0 for num_enigmes in liste_num_enigmes}
    print(nb_bonnes_reponses)
    for dico_resultat in liste_complete:
        for enigme in dico_resultat["reponses"]:
            print(enigme)
            if dico_resultat["reponses"][enigme]["correct"]:
                nb_bonnes_reponses[enigme] = nb_bonnes_reponses[enigme] + 1
    if len(liste_resultats) != 0:
        pourcentage_bonnes_reponses = {num_enigmes: round(nb_bonnes_reponses[num_enigmes]/len(liste_resultats)*100) for num_enigmes in nb_bonnes_reponses}
        print(pourcentage_bonnes_reponses)
    else:
        pourcentage_bonnes_reponses = {num_enigmes: 0 for num_enigmes in nb_bonnes_reponses}

    """ liste_reponses = [resultat.dictionnaire_reponses_eleve() for resultat in liste_resultats] 
    liste_scores = [resultat.calcul_score() for resultat in liste_resultats]
    liste_complete = [
        {
            "id": liste_resultats[i].id_eleve,
            "score": liste_scores[i],
            "reponses": {}
        }
        for i in range(len(liste_resultats))
    ]  """
    
    context = {
            "enquete": enquete,
            "enigmes": liste_num_enigmes,
            "reponses": liste_resultats,
            "resultats": liste_complete,
            "pourcentage": pourcentage_bonnes_reponses
        }
    # gestion du fetch pour actualiser les résultats
    if request.method == 'POST':
        print("requete POST : ", request.POST)
        if "maj" in request.POST:
            response = {
                "resultats": liste_complete,
                "pourcentage": pourcentage_bonnes_reponses,
                "enigmes": liste_num_enigmes
            }
            print(response)
            return JsonResponse(response)
        else:
            return render(request, 'enigmes/enquete_resultats.html', context) # A MODIFIER
    return render(request, 'enigmes/enquete_resultats.html', context) # A MODIFIER  
        
