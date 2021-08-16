from django.db.models.base import Model
from django.forms import Form, ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple, TextInput, CharField, CheckboxSelectMultiple, ModelChoiceField, MultipleChoiceField
from django.forms import widgets
from django.utils.html import format_html

from django.forms.widgets import ClearableFileInput

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


class EnqueteEleveForm(Form):
    
    id_eleve = CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        enigmes = kwargs.pop('enigmes')
        super(EnqueteEleveForm, self).__init__(*args, **kwargs)
        for enigme in enigmes:
            self.fields[str(enigme.pk)] = CharField(max_length=100, label='Réponse', required=False)

# ---------- NON UTILISÉ ----------

class CustomSelectMultiple(ModelMultipleChoiceField):
    def label_from_instance(self, obj: Model) -> str:
        return format_html(obj.enonce)

class EnqueteCreateForm(ModelForm):
    enigmes = ModelMultipleChoiceField(
        widget = CheckboxSelectMultiple,
        queryset=Enigme.objects.all()
    )

    class Meta:
        model = Enquete
        fields = ['enigmes', 'description', 'indications', 'correction', 'score', 'ordre_aleatoire']
        widgets = {
            'enigmes': CheckboxSelectMultiple,
        }
    
# ------------------------------