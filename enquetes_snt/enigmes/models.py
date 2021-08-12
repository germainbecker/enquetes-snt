from django.db import models
from django.db.models.fields import DateTimeField
from django.utils import timezone
#from django.contrib.auth.models import User
#from enseignants.models import User  -> remplacé par ligne ci-dessous
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
#from .utils import generer_code_enquete_unique
from django import forms

from django.utils.translation import gettext_lazy as _
import random, os
import ast
import pytz
import csv
import json
import datetime

def generer_code_enquete_unique():
    enquetes = Enquete.objects.all()
    codes_existants = set(enquete.code for enquete in enquetes)
    carac = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    code = "".join(random.choices(carac, k=8))
    while code in codes_existants:
        code = "".join(random.choices(carac, k=8))
    return code

class Enigme(models.Model):
    class Theme(models.TextChoices):
        NC = 'NC', _('Non défini')
        INT = 'INT', _('Internet')
        WEB = 'WEB', _('Le Web')
        RS = 'RS', _('Les réseaux sociaux')
        DATA = 'DATA', _('Les données structurées et leur traitement')
        LCM = 'LCM', _('Localisation, cartographie, mobilité')
        IEOC = 'IEOC', _('Informatique embarquée et objets connectés')
        IMG = 'IMG', _('La photographie numérique')
        PY = 'PY', _('Python')
    
    date_creation = models.DateTimeField('date de création', auto_now_add=True)
    date_modification = models.DateTimeField('date de modification', default=timezone.now)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)  # si un utilisateur supprime son compte, ses énigmes restent
    theme = models.CharField(
        'thème',
        max_length=4,
        choices=Theme.choices,
        default=Theme.NC
    )
    
    enonce = models.TextField('énoncé')
    reponse = models.CharField('réponse', max_length=100)
    indication = models.TextField('indication', blank=True, null=True)

    def repertoire_auteur(instance, nom_fichier):
        # le fichier sera uploadé dans MEDIA_ROOT/user_<id>/<nom_fichier>
        return 'auteur_{0}/{1}'.format(instance.auteur.id, nom_fichier)
    
    image = models.ImageField(
        "Image d'illustration",
        blank=True,
        max_length=100,
        upload_to=repertoire_auteur,
        #widgets=forms.FileField(attrs={'accept':'.png, .jpg, .jpeg, image/*'})
    )

    fichier = models.FileField("Fichier en pièce jointe", blank=True, max_length=100, upload_to=repertoire_auteur)

    def __str__(self):
        return str(self.id) + " / " + str(self.auteur)
    
    def get_absolute_url(self):
        return reverse('enigme-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'énigme'


class Enquete(models.Model):
    description = models.CharField('description', max_length=100, blank=True, default='')  # ne sert que pour l'auteur
    date_creation = models.DateTimeField('date de création', auto_now_add=True)
    active = models.BooleanField('active', default=True)
    indications = models.BooleanField('indications', default=True)  # indications affichées par défaut
    score =  models.BooleanField('score', default=True)  # score affichés après l'enquête
    correction = models.BooleanField('correction', default=False)  # reponses non affichées après l'enquête par défaut
    ordre_aleatoire = models.BooleanField('ordre aléatoire des énigmes', default=False)  # pas d'ordre aléatoire des énigmes par défaut
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)  # si un utilisateur supprime son compte, ses énigmes sont supprimées
    enigmes = models.ManyToManyField(Enigme, related_name='enigmes', blank=True)
    cle = models.CharField('clé', max_length=200, blank=True, default='')
    code = models.CharField(
        "code de l'enquête",
        max_length=10,
        unique=True,
        null=True,
        default=generer_code_enquete_unique
    )
        
    def liste_enigmes_ordre_initial(self):
        return list(self.enigmes.all())
    
    def liste_enigmes(self):
        import random
        L = list(self.enigmes.all())
        if not self.ordre_aleatoire:
            return L
        else:
            random.shuffle(L)  # mélange en place
            return L
    
    def liste_numeros_enigmes_ordre_initial(self):
        return [enigme.pk for enigme in self.liste_enigmes_ordre_initial()]

    def liste_numeros_enigmes(self):
        return [enigme.pk for enigme in self.liste_enigmes()]
    
    def creation_cle_enquete(self):
        enquete = Enquete.objects.get(pk=self.pk)
        liste_enigmes = enquete.liste_enigmes()
        liste_num_enigmes = [str(enigme.pk) for enigme in liste_enigmes]
        cle = ";".join(liste_num_enigmes)
        self.cle = cle

    def creation_tableau_resultats(self):
        liste_resultats = Resultat.objects.filter(enquete=self.pk)
        nb_enigmes = len(self.liste_enigmes_ordre_initial())
        liste_complete = []
        for resultat in liste_resultats:
            dico = {}
            # ajout de l'identifiant de l'élève
            dico['id_eleve'] = resultat.id_eleve
            # ajout du score
            dico['score'] = resultat.calcul_score()
            # ajout note convertie sur 20
            dico['note_sur_20'] = round(dico['score'] * 20 / nb_enigmes, 2) 
            # ajout réponses
            for num, rep in resultat.dictionnaire_reponses_eleve().items():
                dico['enquete' + str(num)] = rep
            # ajout date
            dico['date'] = resultat.date.astimezone(pytz.timezone("Europe/Paris")).strftime("%d/%m/%Y %H:%M:%S")
            liste_complete.append(dico)
        return liste_complete

    def genere_csv(self):
        nom_fichier = 'resultats_' + self.code + '_' + str(datetime.datetime.now().strftime("%Y-%m-%dT%H_%M_%S")) + '.csv'
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="' + nom_fichier +'"'},
        )
        donnees = self.creation_tableau_resultats()
        if donnees != []:
            writer = csv.DictWriter(response, list(donnees[0].keys()), delimiter = ",")
            writer.writeheader()
            writer.writerows(donnees)
            return response
        else:
            return None

    def __str__(self):
        return str(self.id) + " / " + str(self.auteur)

    class Meta:
        verbose_name = 'enquête'

class Resultat(models.Model):
    enquete = models.ForeignKey(Enquete, related_name='enquete', blank=True, on_delete=models.CASCADE)  # si une enquete est supprimée ses résultats le sont aussi
    reponses = models.TextField('réponses', null=True, blank=True)  # du type "{enigme.pk : 'rep', ...}" --> utiliser ast.literal_eval pour évaluer en dictionnaire
    id_eleve = models.CharField('id_eleve', max_length=100, default='')
    date = models.DateTimeField('date', auto_now_add=True)

    def dictionnaire_reponses_eleve(self):
        """
        Renvoie un dictionnaire associant à chaque enquete.pk la réponse saisie par l'utilsateur
        
        Exemple : Si l'attribut reponses d'un objet Resultat est "{1: "hello", 4: "bye"}" alors la méthode appliquée
        à l'objet renvoie le dictionnaire {1: "hello", 4: "bye"}.
        """
        reponses_eleves = ast.literal_eval(self.reponses)  # type(reponses_eleves) = dict 
        return reponses_eleves

    """ def calcul_score(self):
        liste_enigmes = self.enquete.liste_enigmes()
        bonnes_reponses = {enigme.pk: enigme.reponse for enigme in liste_enigmes}
        reponses_eleves = self.dictionnaire_reponses_eleve()
        score = 0
        for num_enigme in bonnes_reponses.keys():
            if reponses_eleves[num_enigme] == bonnes_reponses[num_enigme]:
                score = score + 1
        return score """
    
    def bonnes_mauvaises_reponses(self):
        liste_enigmes = self.enquete.liste_enigmes()
        bonnes_reponses = {enigme.pk: enigme.reponse for enigme in liste_enigmes}
        reponses_eleves = self.dictionnaire_reponses_eleve()
        correction_reponses = {num_enigme: None for num_enigme in bonnes_reponses.keys()}
        for num_enigme in bonnes_reponses.keys():
            if reponses_eleves[num_enigme] == bonnes_reponses[num_enigme]:
                correction_reponses[num_enigme] = True
            else:
                correction_reponses[num_enigme] = False
        return correction_reponses
    
    def calcul_score(self):
        return list(self.bonnes_mauvaises_reponses().values()).count(True)
    
    def dico_complet(self):
        liste_enigmes = self.enquete.liste_enigmes_ordre_initial()
        reponses_eleve = self.dictionnaire_reponses_eleve()
        correction_reponses = self.bonnes_mauvaises_reponses()
        d = {
            "id": self.id_eleve,
            "score": list(correction_reponses.values()).count(True),
            "reponses": {
                enigme.pk: {
                    "rep_eleve": reponses_eleve[enigme.pk],
                    "correct": correction_reponses[enigme.pk]
                }
                for enigme in liste_enigmes
            },
            "date": self.date
        }
        return d

    def mise_en_forme_date(self):
        d = self.date
        d = d.strftime("%d/%m/%Y %H:%M")
        timezone = pytz.timezone("Europe/Paris")
        d_aware = timezone.localize(d)
        return d_aware

    def __str__(self):
        return "enquête " + str(self.enquete.pk) + " - " + str(self.enquete.code) + " - " + str(self.reponses)

    class Meta:
        verbose_name = 'résultat'
