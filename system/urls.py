from . import views
from . import auth_views
from django.urls import path

app_name = 'system'

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('odometers', views.all_odometers, name='all_odometers'),
    path('purchasers', views.all_purchasers, name='all_purchasers'),
]

urlpatterns += [
    path("", auth_views.login_page, name="login_page"),
    path("process-login", auth_views.process_login, name="process_login"),
    path("sign-out", auth_views.sign_out, name="sign_out"),
]
