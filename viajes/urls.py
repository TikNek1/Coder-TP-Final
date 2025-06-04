from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import (
    ViajeDetailView, ViajeUpdateView, ViajeDeleteView, RegistroView, PerfilPilotoView, EditarUsuarioView, CambiarPasswordView, 
    ListaPilotosView, DetallePilotoView, PilotoUpdateView, PilotoDeleteView, ListaGuiasView, GuiaCreateView, GuiaUpdateView, GuiaDeleteView
    )

urlpatterns = [
    path('', views.bienvenida, name='bienvenida'),
    path('about/', TemplateView.as_view(template_name="about.html"), name="about"),

    # Viajes
    path('viajes/', views.listar_viajes, name='listar_viajes'),
    path('viajes/<int:pk>/', ViajeDetailView.as_view(), name='detalle_viaje'),
    path('viaje/<int:pk>/editar/', ViajeUpdateView.as_view(), name='editar_viaje'),
    path('viaje/<int:pk>/eliminar/', ViajeDeleteView.as_view(), name='eliminar_viaje'),
    path('nuevo_viaje/', views.crear_viaje, name='crear_viaje'),

    # GUIAS
    path('guias/', views.ListaGuiasView.as_view(), name='lista_guias'),
    path('guias/crear/', views.GuiaCreateView.as_view(), name='crear_guia'),
    path('guias/<int:pk>/editar/', views.GuiaUpdateView.as_view(), name='editar_guia'),
    path('guias/<int:pk>/eliminar/', views.GuiaDeleteView.as_view(), name='eliminar_guia'),

    # PILOTOS
    path('pilotos/', ListaPilotosView.as_view(), name='lista_pilotos'),
    path('pilotos/<int:pk>/', DetallePilotoView.as_view(), name='detalle_piloto'),
    path('pilotos/<int:pk>/editar/', PilotoUpdateView.as_view(), name='editar_piloto'),
    path('pilotos/<int:pk>/eliminar/', PilotoDeleteView.as_view(), name='eliminar_piloto'),

    # Registro y perfil de usuario
    path('registro/', RegistroView.as_view(), name='registro'),
    path('perfil/', PerfilPilotoView.as_view(), name='perfil_piloto'),
    path('mi-usuario/', EditarUsuarioView.as_view(), name='editar_usuario'),
    path('cambiar-password/', CambiarPasswordView.as_view(), name='cambiar_password'),
]