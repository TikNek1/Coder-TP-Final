from django.urls import path
from . import views
from .views import ViajeDetailView, ViajeUpdateView, ViajeDeleteView, RegistroUsuarioView

urlpatterns = [
    path('', views.bienvenida, name='bienvenida'),
    path('viajes/', views.listar_viajes, name='listar_viajes'),
    path('guias/', views.lista_guias, name='listar_guias'),
    path('pilotos/', views.lista_pilotos, name='listar_pilotos'),
    path('viajes/<int:pk>/', ViajeDetailView.as_view(), name='detalle_viaje'),
    path('viaje/<int:pk>/editar/', ViajeUpdateView.as_view(), name='editar_viaje'),
    path('viaje/<int:pk>/eliminar/', ViajeDeleteView.as_view(), name='eliminar_viaje'),
    path('nuevo_viaje/', views.crear_viaje, name='crear_viaje'),
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
]