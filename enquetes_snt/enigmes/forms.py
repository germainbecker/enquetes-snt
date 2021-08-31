from django.db.models.base import Model
from django.db.models.fields import BooleanField, TextField
from django.forms import Form, ModelForm, ModelMultipleChoiceField, TextInput, CharField, CheckboxSelectMultiple, ModelChoiceField, MultipleChoiceField
from django.forms import widgets
from django.utils.html import format_html
from django.core.validators import RegexValidator
from django.forms.widgets import ClearableFileInput, Textarea

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
        fields = ('theme', 'enonce', 'reponse', 'indication', 'image', 'fichier')
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
            'fichier': CustomClearableFileInput(),
        }
        help_texts = {
            'image': "Les extensions acceptées sont .jpg et .png. La taille maximale autorisée est 300 Kio.",
            'fichier': "Les extensions acceptées sont .csv, .ods, .xls, .xlsx, .py, .html, .css, .txt, .jpg, .png et .json. La taille maximale de la pièce jointe est de 1 Mio."
        }

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
        fields = ('theme', 'enonce', 'reponse', 'indication', 'image', 'fichier')
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
    
    class Meta:
        model = Enigme
        fields = ['theme', 'enonce', 'reponse', 'indication', 'image', 'fichier']
        widgets = {
            'image': CustomClearableFileInput(),
            'fichier': CustomClearableFileInput(),
        }
        help_texts = {
            'image': "Les extensions acceptées sont .jpg et .png. La taille maximale autorisée est 300 Kio.",
            'fichier': "Les extensions acceptées sont .csv, .ods, .xls, .xlsx, .py, .html, .css, .txt, .jpg, .png et .json. La taille maximale de la pièce jointe est de 1 Mio."
        }

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
 
