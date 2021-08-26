from django.urls import path


from django.contrib.auth import views as auth_views

from . import views
from .forms import MySetPasswordForm, MyAuthenticationForm

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('login/', auth_views.LoginView.as_view(form_class=MyAuthenticationForm, template_name='enseignants/login.html'), name='login'),
    path('activation/<uidb64>/<token>/', views.activation, name='account_activation'),
    path('logout/', auth_views.LogoutView.as_view(template_name='enseignants/logout.html'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='enseignants/password_reset_form.html', html_email_template_name='enseignants/password_reset_email.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='enseignants/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class = MySetPasswordForm, template_name='enseignants/password_reset_confirm.html'), name='password_reset_confirm'),
    #re_path('^enseignants/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(template_name='enseignants/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='enseignants/password_reset_complete.html'), name='password_reset_complete'),
        #path('enseignants/password_reset/confirm/', auth_views.PasswordResetConfirmView.as_view(template_name='enseignants/password_reset_confirm.html'), name='password_reset_confirm'),
]