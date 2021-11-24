from django.db import models
from django.db.models.fields import DateTimeField
from django.db.models.fields.related import ForeignKey
from django.utils import timezone
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse
from django import forms
from django.utils.functional import cached_property
from enigmes.validators import FileValidator
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

import random, os
import ast
import pytz
import csv
import json
import datetime

class Fichier(models.Model):
    
    def repertoire_fichiers_auteur(instance, nom_fichier):
        # le fichier sera uploadé dans MEDIA_ROOT/auteur_<id>/<nom_fichier>
        return 'auteur_{0}/fichiers/{1}'.format(instance.auteur.id, nom_fichier)
    
    fichier = models.FileField(
        "Sélectionner un fichier",
        blank=False,
        max_length=100,
        upload_to=repertoire_fichiers_auteur,
        validators=[
            FileValidator(
                max_size=1024 * 1000, # 1 Mio
                content_types=(
                    'text/csv',
                    'application/vnd.oasis.opendocument.spreadsheet',  #.ods
                    'application/vnd.ms-excel',  #.xls
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  #.xlsx
                    'text/x-python',  #.py
                    'text/html',
                    'text/css',
                    'text/plain', #.txt
                    'application/json',
                    'image/jpeg',
                    'image/png',
                )
            )
        ]
    )

    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)  # si un utilisateur supprime son compte, ses fichiers restent
    
    @property
    def url(self):
        return self.fichier.url

    def __str__(self):
        return os.path.basename(self.fichier.name)

class Image(models.Model):
    
    def repertoire_images_auteur(instance, nom_fichier):
        # le fichier sera uploadé dans MEDIA_ROOT/auteur_<id>/<nom_fichier>
        return 'auteur_{0}/images/{1}'.format(instance.auteur.id, nom_fichier)
    
    image = models.ImageField(
        "Sélectionner une image",
        blank=False,
        max_length=100,
        upload_to=repertoire_images_auteur,
        validators=[
            FileValidator(
                max_size=1024 * 300, # 300 Kio
                content_types=(
                    'image/jpeg',
                    'image/png',
                )
            )
        ]
    )

    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)  # si un utilisateur supprime son compte, ses fichiers restent

    @property
    def name(self):
        return os.path.basename(self.image.name)

    @property
    def url(self):
        return self.image.url

    def __str__(self):
        return os.path.basename(self.image.name)

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
    reponse2 = models.CharField('réponse 2', max_length=100, blank=True, null=True)
    reponse3 = models.CharField('réponse 3', max_length=100, blank=True, null=True)
    reponse4 = models.CharField('réponse 4', max_length=100, blank=True, null=True)
    indication = models.TextField('indication', blank=True, null=True)

    def repertoire_auteur(instance, nom_fichier):
        # le fichier sera uploadé dans MEDIA_ROOT/auteur_<id>/<nom_fichier>
        return 'auteur_{0}/{1}'.format(instance.auteur.id, nom_fichier)
    
    image = models.ForeignKey(Image, related_name='enigme', blank=True, null=True,on_delete=models.SET_NULL)
    
    """ image = models.ImageField(
        "Téléverser une image d'illustration",
        blank=True,
        max_length=100,
        upload_to=repertoire_auteur,
        validators=[
            FileValidator(
                max_size=1024 * 300, # 300 Kio
                content_types=(
                    'image/jpeg',
                    'image/png',
                )
            )
        ]
    ) """

    url_image = models.URLField("URL de l'image d'illustration", blank=True, null=True)

    credits_image = models.TextField("Crédits de l'image", blank=True, null=True)

    fichier = models.ForeignKey(Fichier, related_name='enigme', blank=True, null=True,on_delete=models.SET_NULL)

    """ fichier = models.FileField(
        "Fichier en pièce jointe",
        blank=True,
        max_length=100,
        upload_to=repertoire_auteur,
        validators=[
            FileValidator(
                max_size=1024 * 1000, # 1 Mio
                content_types=(
                    'text/csv',
                    'application/vnd.oasis.opendocument.spreadsheet',  #.ods
                    'application/vnd.ms-excel',  #.xls
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  #.xlsx
                    'text/x-python',  #.py
                    'text/html',
                    'text/css',
                    'text/plain', #.txt
                    'application/json',
                    'image/jpeg',
                    'image/png',
                )
            )]
        ) """

    def __str__(self):
        return str(self.id) + " / " + str(self.auteur)
    
    def get_absolute_url(self):
        return reverse('enigme-detail', kwargs={'pk': self.pk})

    def liste_reponses(self):
        lst = [self.reponse]
        for r in [self.reponse2, self.reponse3, self.reponse4]:
            if r is not None:
                lst.append(r)
        return [reponse_nettoyee(rep) for rep in lst]

    class Meta:
        verbose_name = 'énigme'


class Enquete(models.Model):
    description = models.CharField('description', max_length=100, default='')  # ne sert que pour l'auteur
    date_creation = models.DateTimeField('date de création', auto_now_add=True)
    active = models.BooleanField('active', default=True)
    indications = models.BooleanField('indications', default=True)  # indications affichées par défaut
    score =  models.BooleanField('score', default=True)  # score affichés après l'enquête par défaut
    correction = models.BooleanField('correction', default=False)  # reponses non affichées après l'enquête par défaut
    ordre_aleatoire = models.BooleanField('ordre aléatoire des énigmes', default=False)  # pas d'ordre aléatoire des énigmes par défaut
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)  # si un utilisateur supprime son compte, ses enquêtes sont supprimées
    enigmes = models.ManyToManyField(Enigme, related_name='enigmes', blank=True)
    cle = models.CharField('clé', max_length=200, default='')
    code = models.CharField(
        "code de l'enquête",
        max_length=10,
        unique=True,
        null=True,
        default=generer_code_enquete_unique
    )

    @cached_property 
    def liste_enigmes_ordre_initial(self):
        '''on se base sur la clé pour avoir l'ordre'''
        liste_num_enigmes = self.cle.split(";")
        liste_enigmes = []
        for num_enigme in liste_num_enigmes:
            enigme = Enigme.objects.select_related('auteur', 'image', 'fichier').get(pk=int(num_enigme))
            liste_enigmes.append(enigme)
        return liste_enigmes
    
    @cached_property 
    def liste_enigmes(self):
        import random
        L = list(self.enigmes.all())
        if not self.ordre_aleatoire:
            return L
        else:
            random.shuffle(L)  # mélange en place
            return L
    
    @cached_property 
    def liste_numeros_enigmes_ordre_initial(self):
        liste_num_enigmes = self.cle.split(";")
        return [int(num) for num in liste_num_enigmes]

    @cached_property
    def liste_numeros_enigmes(self):
        return [enigme.pk for enigme in self.liste_enigmes]
    
    def creation_cle_enquete(self):
        enquete = Enquete.objects.get(pk=self.pk)
        liste_enigmes = enquete.liste_enigmes
        liste_num_enigmes = [str(enigme.pk) for enigme in liste_enigmes]
        cle = ";".join(liste_num_enigmes)
        self.cle = cle

    def dico_bonnes_reponses(self):
        liste_enigmes = self.liste_enigmes_ordre_initial
        bonnes_reponses = {enigme.pk: enigme.liste_reponses for enigme in liste_enigmes}
        return bonnes_reponses

    def creation_tableau_resultats(self):
        liste_resultats = Resultat.objects.filter(enquete=self.pk)
        nb_enigmes = len(self.liste_numeros_enigmes_ordre_initial)
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

def reponse_nettoyee(ch: str) -> str :
    """
    Renvoie une nouvelle chaine, en minuscules, correspond à la chaine ch mais
    avec suppression des espaces de fin et début, et des accents.
    Permet de comparer deux réponses.
    Ex : 
    >>> reponse_nettoyee(' Épinal    ')
    'epinal' 
    """
    
    # suppression des accents
    import unicodedata
    s = ''.join(c for c in unicodedata.normalize('NFD', ch)
                if unicodedata.category(c) != 'Mn')
    # suppression de espaces de début et fin
    s = s.strip()
    # en minuscules
    return s.lower()

class Resultat(models.Model):
    enquete = models.ForeignKey(Enquete, related_name='enquete', blank=True, on_delete=models.CASCADE)  # si une enquete est supprimée ses résultats le sont aussi
    reponses = models.TextField('réponses', null=True, blank=True)  # du type "{enigme.pk : 'rep', ...}" --> utiliser ast.literal_eval pour évaluer en dictionnaire
    id_eleve = models.CharField(
        'id_eleve',
        max_length=100,
        default='',
        validators=[
            RegexValidator(
                r'^([a-zA-Z]?)[0-9\-\_]*',
                "L'identifiant saisi n'est pas valide. Veuillez consultez votre professeur.",
            )
        ]
    )
    date = models.DateTimeField('date', auto_now_add=True)
    
    def dictionnaire_reponses_eleve(self):
        """
        Renvoie un dictionnaire associant à chaque enquete.pk la réponse saisie par l'utilsateur
        
        Exemple : Si l'attribut reponses d'un objet Resultat est "{1: "hello", 4: "bye"}" alors la méthode appliquée
        à l'objet renvoie le dictionnaire {1: "hello", 4: "bye"}.
        """
        reponses_eleves = ast.literal_eval(self.reponses)  # type(reponses_eleves) = dict 
        return reponses_eleves

    def bonnes_mauvaises_reponses(self):
        liste_enigmes = self.enquete.liste_enigmes
        bonnes_reponses = {enigme.pk: enigme.reponse for enigme in liste_enigmes}
        reponses_eleves = self.dictionnaire_reponses_eleve()
        correction_reponses = {num_enigme: None for num_enigme in bonnes_reponses.keys()}

        for enigme in liste_enigmes:
            lst_bonnes_reponses = enigme.liste_reponses()  # les réponses de cette liste sont nettoyées
            if reponse_nettoyee(reponses_eleves[enigme.pk]) in lst_bonnes_reponses:
                correction_reponses[enigme.pk] = True
            else:
                correction_reponses[enigme.pk] = False
        return correction_reponses
    
    def calcul_score(self):
        return list(self.bonnes_mauvaises_reponses().values()).count(True)

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
