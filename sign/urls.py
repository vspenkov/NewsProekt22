from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterForm, BaseRegisterView, upgrade_me
    # upgrade_me


urlpatterns = [
    path('login/', LoginView.as_view(template_name = 'account/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name = 'account/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name = 'account/signup.html'), name='signup'),
    path('upgrade/', upgrade_me, name = 'upgrade')
]
