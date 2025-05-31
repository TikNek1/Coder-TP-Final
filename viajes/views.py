from django.shortcuts import render, redirect, get_object_or_404
from .models import Viaje, Guia, Piloto
from .forms import ViajeForm, RegistroUsuarioForm, RegistroCompletoForm
from django.db.models import Q
from datetime import datetime
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.urls import reverse_lazy

def bienvenida(request):
    return render(request, 'bienvenida.html')

class RegistroUsuarioView(CreateView):
    form_class = RegistroCompletoForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('listar_viajes')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # self.object es el User creado
        return response

def listar_viajes(request):
    nombre = request.GET.get('nombre', '')
    mes = request.GET.get('mes', '')  # formato esperado: YYYY-MM

    # Primer filtro según permisos
    if request.user.is_authenticated and (request.user.is_superuser or request.user.groups.filter(name='TikNek').exists()):
        viajes = Viaje.objects.all()
    else:
        viajes = Viaje.objects.filter(activo=True)

    #viajes = Viaje.objects.all()

    if nombre:
        viajes = viajes.filter(nombre__icontains=nombre)

    if mes:
        try:
            fecha_inicio = datetime.strptime(mes, "%Y-%m")
            fecha_fin = datetime(fecha_inicio.year, fecha_inicio.month + 1, 1) if fecha_inicio.month < 12 else datetime(fecha_inicio.year + 1, 1, 1)
            viajes = viajes.filter(fecha_salida__gte=fecha_inicio, fecha_salida__lt=fecha_fin)
        except ValueError:
            pass  # si el mes viene mal formateado, no se filtra por fecha

    return render(request, 'viajes/lista_viajes.html', {
        'viajes': viajes.order_by('fecha_salida'),
    })

# Vista para ver los detalles de un viaje
# def detalle_viaje(request, viaje_id):
#     viaje = get_object_or_404(Viaje, id=viaje_id)
#     return render(request, 'viajes/detalle_viaje.html', {'viaje': viaje})

class ViajeDetailView(DetailView):
    model = Viaje
    template_name = 'viajes/detalle_viaje.html'
    context_object_name = 'viaje'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['puede_editar'] = user.is_superuser or user.groups.filter(name='TikNek').exists() # type: ignore
        return context

class ViajeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Viaje
    form_class = ViajeForm
    template_name = 'viajes/editar_viaje.html'
    success_url = reverse_lazy('listar_viajes')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='TikNek').exists() # type: ignore

class ViajeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Viaje
    template_name = 'viajes/eliminar_viaje.html'
    success_url = reverse_lazy('listar_viajes')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='TikNek').exists() # type: ignore

# Vista para crear un nuevo viaje
def crear_viaje(request):
    if request.method == 'POST':
        form = ViajeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_viajes')
    else:
        form = ViajeForm()
    
    return render(request, 'viajes/crear_viaje.html', {'form': form})

# Vista para listar guías
def lista_guias(request):
    guias = Guia.objects.all()
    return render(request, 'viajes/lista_guias.html', {'guias': guias})

# Vista para listar pilotos
def lista_pilotos(request):
    pilotos = Piloto.objects.all()
    return render(request, 'viajes/lista_pilotos.html', {'pilotos': pilotos})
