from django.urls import path
from .views import (
    EnigmeListView,
    EnigmeDetailView,
    EnigmeCreateView,
    EnigmeExampleCreateView,
    EnigmeUpdateView,
)

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accueil/', views.accueil, name='accueil'),
    path('enseignants/', views.enseignants, name='enseignants'),
    path('enigmes/', EnigmeListView.as_view(), name='enigmes'),
    path('enigme/<int:pk>/', EnigmeDetailView.as_view(), name='enigme-detail'),
    path('enigme/<int:pk>/modification/', EnigmeUpdateView.as_view(), name='enigme-update'),
    path('enigme/creation/', EnigmeCreateView.as_view(), name='enigme-create'),
    path('enigme/creation/exemple/', EnigmeExampleCreateView.as_view(), name='enigme-example-create'),
    path('enquete/<int:enquete_id>/', views.enquete, name='enquete-detail'),
    path('enquete/<int:enquete_id>/suppression', views.suppression_enquete, name='enquete-delete'),
    path('enquete/<int:enquete_id>/resultats/', views.resultats_enquete, name='enquete-resultats'),
    path('enquete/creation/', views.creation_enquete, name='enquete-create'),
    path('enquete/creation/liste/', views.creation_enquete_liste, name='enquete-liste-create'),
    path('enquete/creation/manuelle/', views.creation_enquete_manuelle, name='enquete-manuelle-create'),
    #path('enquete/creation/manuelle/', EnqueteCreateView.as_view(template_name="enigmes/enquete_form_classe.html"), name='enquete-create'),
    path('mon-espace/', views.espace_perso, name='espace-perso'),
    path('mon-espace/mes-enigmes/', views.mes_enigmes, name='mes-enigmes'),
    path('eleve/enquete/<str:code_enquete>/', views.eleve, name='enquete-eleve'),
]