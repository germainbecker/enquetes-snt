from django.db.models.base import Model
from django.db.models.fields import BooleanField, TextField
from django.forms import Form, ModelForm, ModelMultipleChoiceField, TextInput, CharField, CheckboxSelectMultiple, ModelChoiceField, MultipleChoiceField
from django.forms import widgets
from django.utils.html import format_html
from django.core.validators import RegexValidator
from django.forms.widgets import ClearableFileInput, Textarea
from django.core.exceptions import ValidationError

from enigmes.models import Enquete, Enigme
from enseignants.forms import ParagraphErrorList
import os



# Pour personnaliser le formulaire de la vue EnigmeUpdateView

class CustomClearableFileInput(ClearableFileInput):
    """Personnalisation du champ FileInput"""
    template_name = "enigmes/custom_clearable_file_input.html"
    def format_value(self, value):
        if self.is_initial(value):
            value.basename = os.path.basename(value.name)
            return value

class EnigmeCreateForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        # pour personnaliser la liste d'erreurs (ErrorList)
        kwargs.update({'error_class': ParagraphErrorList})
        super(EnigmeCreateForm, self).__init__(*args, **kwargs)
    
    class Meta:
        
        model = Enigme
        fields = ('theme', 'enonce', 'reponse', 'indication', 'url_image', 'image', 'credits_image', 'fichier')
        widgets = {
            'enonce': Textarea(
                attrs={'placeholder': 'L\'énoncé peut être écrit en Markdown ou en HTML'}
            ),
            'reponse': TextInput(
                attrs={'placeholder': '100 caractères max.'}
            ),
            'indication': Textarea(
                attrs={'placeholder': 'Si vous écrivez une indication, vous pouvez aussi l\'écrire en Markdown ou en HTML'}
            ),
            'image': CustomClearableFileInput(),
            'credits_image': Textarea(
                attrs={'placeholder': "Indiquez ici la licence, l'auteur et si possible la source de l'image d'illustration.", 'class': "credits-images", 'rows': '2'}
            ),
            'fichier': CustomClearableFileInput(),
        }
        help_texts = {
            'url_image': "Copiez l'URL de l'image désirée (à privilégier). Vous pouvez également téléverser une image d'illustration ci-dessous.",
            'image': "Les extensions acceptées sont .jpg et .png. La taille maximale autorisée est 300 Kio.",
            'fichier': "Les extensions acceptées sont .csv, .ods, .xls, .xlsx, .py, .html, .css, .txt, .jpg, .png et .json. La taille maximale de la pièce jointe est de 1 Mio."
        }
    
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        credits_image = cleaned_data.get("credits_image")
        image = cleaned_data.get("image")
        url_image = cleaned_data.get("url_image")
        no_image = (url_image == '' and (image == None or image == False))
        if credits_image != '' and no_image:
            raise ValidationError(
                "Il n'est pas possible de définir les crédits si aucune image n'est sélectionnée."
            )


class EnigmeExampleCreateForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        # pour personnaliser la liste d'erreurs (ErrorList)
        kwargs.update({'error_class': ParagraphErrorList})
        super(EnigmeExampleCreateForm, self).__init__(*args, **kwargs)
    
    def get_initial():
        enonce = '''En Markdown on peut facilement écrire en _italique_ ou en **gras**. On peut aussi insérer des liens : [un lien vers codepen](https://codepen.io/gbecker/pen/jObKbvX?editors=1100).

Un saut de ligne crée un nouveau paragraphe. On peut écrire des listes :

* Premier élément
* Deuxième élément
* Troisième élément

On peut aussi insérer facilement du `code` en ligne ou sur plusieurs lignes. Par exemple, du code Python en écrivant :

```python
def niveau_gris(r, v, b):
    return int((r + v + b) / 3)
```

ou d'un autre langage, comme HTML :

```html
<body>
    <h1>Mon blog</h1>
    <h2>Mon premier article<h2>
    <p>Super article trop <strong>génial</strong> !</p>
</body>
```

Et plein d'autres choses : [voici quelques exemples](https://fr.wikipedia.org/wiki/Markdown#Quelques_exemples).

<p>On peut aussi écrire tout cela directement en <strong>HTML</strong>.</p>
'''
        indication = '''Les indications sont facultatives (il faut alors laisser ce champ vide). On peut les écrire en **Markdown** ou en **HTML**.'''
        initial = {
            'enonce': enonce,
            'indication': indication,
        }
        return initial

    class Meta:
        
        model = Enigme
        fields = ('theme', 'enonce', 'reponse', 'indication', 'image', 'credits_image', 'fichier')
        widgets = {
            'enonce': Textarea(
                attrs={'placeholder': 'L\'énoncé peut être écrit en Markdown ou en HTML'}
            ),
            'reponse': TextInput(
                attrs={'placeholder': '100 caractères max.'}
            ),
            'indication': Textarea(
                attrs={'placeholder': 'Si vous écrivez une indication, vous pouvez aussi l\'écrire en Markdown ou en HTML'}
            ),
            'image': CustomClearableFileInput(),
            'credits_image': Textarea(
                attrs={'placeholder': "Indiquez ici la licence, l'auteur, et si possible la source de l'image d'illustration.", 'class': "credits-images", 'rows': '2'}
            ),
            'fichier': CustomClearableFileInput(),
        }
        help_texts = {
            'image': "Les extensions acceptées sont .jpg et .png. La taille maximale autorisée est 300 Kio.",
            'fichier': "Les extensions acceptées sont .csv, .ods, .xls, .xlsx, .py, .html, .css, .txt, .jpg, .png et .json. La taille maximale de la pièce jointe est de 1 Mio."
        }

class EnigmeUpdateForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        # pour personnaliser la liste d'erreurs (ErrorList)
        kwargs.update({'error_class': ParagraphErrorList})
        super(EnigmeUpdateForm, self).__init__(*args, **kwargs)
        if self.data:
            data = self.data.copy()
            credits_image = self.data.get("credits_image")
            image = self.data.get("image")
            url_image = self.data.get("url_image")
            no_image = (url_image == '' and (image == None or image == False))
            if credits_image != '' and no_image:
                data['credits_image'] = ''
                self.data = data
            
    
    class Meta:
        model = Enigme
        fields = ['theme', 'enonce', 'reponse', 'indication', 'url_image', 'image', 'credits_image', 'fichier']
        widgets = {
            'image': CustomClearableFileInput(),
            'credits_image': Textarea(
                attrs={'placeholder': "Indiquez ici la licence, l'auteur et si possible la source de l'image d'illustration.", 'class': "credits-images", 'rows': '2'}
            ),
            'fichier': CustomClearableFileInput(),
        }
        help_texts = {
            'image': "Les extensions acceptées sont .jpg et .png. La taille maximale autorisée est 300 Kio.",
            'fichier': "Les extensions acceptées sont .csv, .ods, .xls, .xlsx, .py, .html, .css, .txt, .jpg, .png et .json. La taille maximale de la pièce jointe est de 1 Mio."
        }
    
    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        image = cleaned_data.get("image")
        url_image = cleaned_data.get("url_image")
        
        # on s'assure de ne pas enregistrer des crédits si aucune image (url ou fichier) n'est choisie
        credits_image = cleaned_data.get("credits_image")
        no_image = (url_image == '' and (image == None or image == False))
        if credits_image != '' and no_image:
            raise ValidationError(
                "Il n'est pas possible de définir les crédits si aucune image n'est sélectionnée."
            )
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if instance.url_image is not None:  # si une url est définie
            instance.image = None  # on s'assure qu'aucun image téléversée n'est associée à l'énigme
        if commit:
            instance.save()
            self.save_m2m()
        return instance
    
"""     def form_valid(self, form):
        updated_enigme = form.save(commit=False)
        print('avant', updated_enigme)
        if updated_enigme.url_image is not None:
            updated_enigme.image = None
        updated_enigme.save()
        print('après', updated_enigme)
        form.save_m2m() """


class CodeEnqueteForm(Form):
    code = CharField(label='Code à saisir', max_length=10)

validateur_id_eleve = RegexValidator(
                regex=r'^([a-zA-Z]?)[0-9\-\_]*$',
                message="L'identifiant saisi n'est pas valide. Consulte ton professeur si nécessaire.",
                code='identifiant_invalide'
            )

class EnqueteEleveForm(Form):

    """ def __init__(self, *args, **kwargs):
        # pour personnaliser la liste d'erreurs (ErrorList)
        kwargs.update({'error_class': ParagraphErrorList})
        super(EnqueteEleveForm, self).__init__(*args, **kwargs) """
    
    id_eleve = CharField(
        label='Identifiant',
        max_length=10,
        required=True,
        validators=[validateur_id_eleve]
    )

    def __init__(self, *args, **kwargs):
        kwargs.update({'error_class': ParagraphErrorList})
        enigmes = kwargs.pop('enigmes')
        super(EnqueteEleveForm, self).__init__(*args, **kwargs)
        for enigme in enigmes:
            self.fields[str(enigme.pk)] = CharField(max_length=100, label='Réponse :', required=False)

class EnqueteCreateListForm(ModelForm):
    class Meta:
        model = Enquete
        fields = ['cle', 'description', 'indications', 'correction', 'score', 'ordre_aleatoire']
        help_texts = {
            'cle': format_html(
                "Saisissez la liste des énigmes souhaitées. Indiquez les numéros des énigmes en les séparant par des point-virgules. <br>Par exemple, <em>7;5;8;2</em> va générer une enquête avec les énigmes n° 7, 5, 8 et 2."
            ),
            'description': format_html(
                "Renseignez une description pour l'enquête (à destination du professeur uniquement)."
            ),
            'indications': format_html(
                "Cochez la case pour que les indications (si elles existent) soient affichées pour les élèves."
            ),
            'correction': format_html(
                "Cochez la case pour que la correction soit proposée aux élèves après leur enquête."
            ),
            'score': format_html(
                "Cochez la case pour que le score des élèves soit affiché après leur enquête. Si la correction est activée (juste au-dessus), le score est automatiquement affiché."
            ),
            'ordre_aleatoire': format_html(
                "Cochez la case pour que les énigmes de l'enquête soient proposées dans un ordre aléatoire aux élèves."
            )
        }
        widgets = {
            'cle' : TextInput(
                attrs={'placeholder': 'Ex : 7;5;8;2'}
            ),
            'description': TextInput(
                attrs={'placeholder': '100 caractères max.'}
            )
        }

class EnqueteCreateForm(ModelForm):
    
    class Meta:
        model = Enquete
        fields = ['enigmes', 'description', 'indications', 'correction', 'score', 'ordre_aleatoire']
        help_texts = {
            'cle': format_html(
                "Saisissez la liste des énigmes souhaitées. Indiquez les numéros des énigmes en les séparant par des point-virgules. <br>Par exemple, <em>7;5;8;2</em> va générer une enquête avec les énigmes n° 7, 5, 8 et 2."
            ),
            'description': format_html(
                "Renseignez une description pour l'enquête (à destination du professeur uniquement)."
            ),
            'indications': format_html(
                "Cochez la case pour que les indications (si elles existent) soient affichées pour les élèves."
            ),
            'correction': format_html(
                "Cochez la case pour que la correction soit proposée aux élèves après leur enquête."
            ),
            'score': format_html(
                "Cochez la case pour que le score des élèves soit affiché après leur enquête. Si la correction est activée (juste au-dessus), le score est automatiquement affiché."
            ),
            'ordre_aleatoire': format_html(
                "Cochez la case pour que les énigmes de l'enquête soient proposées dans un ordre aléatoire aux élèves."
            )
        }
        widgets = {
            'cle' : TextInput(
                attrs={'placeholder': 'Ex : 7;5;8;2'}
            ),
            'description': TextInput(
                attrs={'placeholder': '100 caractères max.'}
            )
        }
    
    enigmes = ModelMultipleChoiceField(
        queryset=Enigme.objects.all(),
        widget=CheckboxSelectMultiple
    )
 
