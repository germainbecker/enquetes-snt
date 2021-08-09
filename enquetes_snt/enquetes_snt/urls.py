"""invest_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

#from invest_project import enseignants
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include, re_path
from enseignants import views as vues_enseignants
from enseignants.forms import MySetPasswordForm

urlpatterns = [
    path('', include('enigmes.urls')),
    path('enseignants/', include('enseignants.urls')),
    path('perso/', admin.site.urls),
    #path('enseignants/', include('django.contrib.auth.urls')),    
]

""" urlpatterns = [
    path('', include('enigmes.urls')),
    #path('enseignants/', include('enseignants.urls')),
    path('enseignants/inscription/', vues_enseignants.inscription, name='inscription'),
    path('enseignants/login/', auth_views.LoginView.as_view(template_name='enseignants/login.html'), name='login'),
    path('enseignants/logout/', auth_views.LogoutView.as_view(template_name='enseignants/logout.html'), name='logout'),
    path('enseignants/password_reset/', auth_views.PasswordResetView.as_view(template_name='enseignants/password_reset_form.html'), name='password_reset'),
    path('enseignants/password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='enseignants/password_reset_done.html'), name='password_reset_done'),
    path('enseignants/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class = MySetPasswordForm, template_name='enseignants/password_reset_confirm.html'), name='password_reset_confirm'),
    #re_path('^enseignants/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(template_name='enseignants/password_reset_confirm.html'), name='password_reset_confirm'),
    path('enseignants/reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='enseignants/password_reset_complete.html'), name='password_reset_complete'),
        #path('enseignants/password_reset/confirm/', auth_views.PasswordResetConfirmView.as_view(template_name='enseignants/password_reset_confirm.html'), name='password_reset_confirm'),
    path('perso/', admin.site.urls),
    path('enseignants/', include('django.contrib.auth.urls')),    
] """

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)