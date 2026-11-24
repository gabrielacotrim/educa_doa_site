from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('escolas/', views.escolas, name='escolas'),
    path('escola/<int:pk>/', views.escola_detalhe, name='escola_detalhe'),
    path('cadastro/doador/', views.cadastro_doador, name='cadastro_doador'),
    path('cadastro/escola/', views.cadastro_escola, name='cadastro_escola'),
    path('login/doador/', views.login_doador, name='login_doador'),
    path('login/escola/', views.login_escola, name='login_escola'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/doador/', views.dashboard_doador, name='dashboard_doador'),
    path('dashboard/escola/', views.dashboard_escola, name='dashboard_escola'),
    path('necessidade/nova/', views.nova_necessidade, name='nova_necessidade'),
    path('necessidade/<int:pk>/editar/', views.editar_necessidade, name='editar_necessidade'),
    path('necessidade/<int:necessidade_pk>/doar/', views.realizar_doacao, name='realizar_doacao'),
]
