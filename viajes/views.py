from django.shortcuts import render, redirect, get_object_or_404
from .models import Viaje, Guia, Piloto
from .forms import ViajeForm, RegistroForm, PilotoForm, EditarUsuarioForm, GuiaForm
from django.db.models import Q
from datetime import datetime
from django.views import View
from django.views.generic import DetailView, UpdateView, DeleteView, ListView, CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login
from django.urls import reverse_lazy

# -------------------------------------------------------------------------------------------------------------------
# *** LANDING PAGE ***
# -------------------------------------------------------------------------------------------------------------------

def bienvenida(request):
    """
    Vista para la página de bienvenida.
    Renderiza la plantilla 'bienvenida.html'.
    """
    return render(request, 'bienvenida.html')

# -------------------------------------------------------------------------------------------------------------------
# *** USUARIOS ***
# -------------------------------------------------------------------------------------------------------------------

class RegistroView(CreateView):
    """
    Vista para registrar nuevos usuarios.
    Utiliza el formulario RegistroForm para crear un nuevo usuario.
    """
    model = User
    form_class = RegistroForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """
        Si el formulario es válido, registra al usuario y lo autentica automáticamente.
        """
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f"Usuario {user.username}  registrado correctamente. Por favor, hacé login y completá tu perfil.")
        return super().form_valid(form)


class PerfilPilotoView(LoginRequiredMixin, View):
    """
    Vista para crear o actualizar el perfil de un piloto.
    Renderiza un formulario para completar o editar el perfil del piloto.
    """
    template_name = 'usuarios/completar_perfil.html'

    def get(self, request):
        """
        Muestra el formulario con los datos del piloto si existe, o vacío si no.
        """
        try:
            piloto = request.user.piloto
            form = PilotoForm(instance=piloto)
        except Piloto.DoesNotExist:
            form = PilotoForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Procesa el formulario para crear o actualizar el perfil del piloto.
        """
        try:
            piloto = request.user.piloto
            form = PilotoForm(request.POST, request.FILES, instance=piloto)
        except Piloto.DoesNotExist:
            form = PilotoForm(request.POST, request.FILES)

        if form.is_valid():
            piloto = form.save(commit=False)
            piloto.user = request.user
            piloto.save()
            messages.success(request, "Perfil actualizado.")
            return redirect('bienvenida')

        return render(request, self.template_name, {'form': form})


class EditarUsuarioView(LoginRequiredMixin, UpdateView):
    """
    Vista para editar los datos de un usuario existente.
    """
    model = User
    form_class = EditarUsuarioForm
    template_name = 'usuarios/editar_usuario.html'
    success_url = reverse_lazy('bienvenida')

    def get_object(self):
        """
        Retorna el usuario autenticado.
        """
        return self.request.user

    def form_valid(self, form):
        """
        Muestra un mensaje de éxito si los datos del usuario se actualizan correctamente.
        """
        messages.success(self.request, "Tus datos de usuario fueron actualizados.")
        return super().form_valid(form)


class CambiarPasswordView(PasswordChangeView):
    """
    Vista para cambiar la contraseña del usuario autenticado.
    """
    template_name = 'usuarios/cambiar_password.html'
    success_url = reverse_lazy('bienvenida')

    def form_valid(self, form):
        """
        Muestra un mensaje de éxito si la contraseña se actualiza correctamente.
        """
        messages.success(self.request, "Tu contraseña fue actualizada correctamente.")
        return super().form_valid(form)

# -------------------------------------------------------------------------------------------------------------------
# *** VIAJES ***
# -------------------------------------------------------------------------------------------------------------------

def listar_viajes(request):
    """
    Vista para listar los viajes disponibles.
    Permite filtrar por nombre y mes de salida.
    """
    nombre = request.GET.get('nombre', '')
    mes = request.GET.get('mes', '')  # formato esperado: YYYY-MM

# Primer filtro según permisos
    if request.user.is_authenticated and (request.user.is_superuser or request.user.groups.filter(name='TikNek').exists()):
        viajes = Viaje.objects.all()
    else:
        viajes = Viaje.objects.filter(activo=True)

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


class ViajeDetailView(DetailView):
    """
    Vista para mostrar los detalles de un viaje.
    """
    model = Viaje
    template_name = 'viajes/detalle_viaje.html'
    context_object_name = 'viaje'

    def get_context_data(self, **kwargs):
        """
        Agrega al contexto si el usuario puede editar el viaje.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['puede_editar'] = user.is_superuser or user.groups.filter(name='TikNek').exists()  # type: ignore
        return context


class ViajeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Vista para editar un viaje existente.
    """
    model = Viaje
    form_class = ViajeForm
    template_name = 'viajes/editar_viaje.html'
    success_url = reverse_lazy('listar_viajes')

    def get_success_url(self):
        """
        Redirige a los detalles del viaje después de actualizarlo.
        """
        messages.success(self.request, "Viaje actualizado correctamente.")
        return reverse_lazy('detalle_viaje', kwargs={'pk': self.object.pk}) # type: ignore

    def test_func(self):
                return self.request.user.is_superuser or self.request.user.groups.filter(name='TikNek').exists() # type: ignore

class ViajeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Vista para eliminar un viaje.
    """
    model = Viaje
    template_name = 'viajes/eliminar_viaje.html'

    def get_success_url(self):
        """
        Redirige a la lista de viajes después de eliminarlo.
        """
        messages.success(self.request, "Viaje eliminado")
        return reverse_lazy('listar_viajes')

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

# -------------------------------------------------------------------------------------------------------------------
# *** GUIAS ***
# En esta sección están las vistas para listar GUIAS y ver los detalles de un piloto, además del CRUD.
# -------------------------------------------------------------------------------------------------------------------

class ListaGuiasView(ListView):
    model = Guia
    template_name = 'guias/lista_guias.html'
    context_object_name = 'guias'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['puede_editar'] = user.is_superuser or user.groups.filter(name='TikNek').exists() # type: ignore
        return context

    def get_queryset(self):
        return Guia.objects.prefetch_related('viajes').all()

class GuiaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Guia
    form_class = GuiaForm
    template_name = 'guias/guia_form.html'

    def get_success_url(self):
        messages.success(self.request, "Guía actualizado correctamente.")
        return reverse_lazy('lista_guias')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='TikNek').exists() # type: ignore

class GuiaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Guia
    template_name = 'guias/eliminar_guia.html'

    def get_success_url(self):
        messages.success(self.request, "Guía eliminado")
        return reverse_lazy('lista_guias')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='TikNek').exists() # type: ignore

class GuiaCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Guia
    form_class = GuiaForm
    template_name = 'guias/guia_form.html'
    success_url = reverse_lazy('lista_guias')

    def form_valid(self, form):
        messages.success(self.request, f"{form.instance} creado correctamente")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='TikNek').exists() # type: ignore

# -------------------------------------------------------------------------------------------------------------------
# *** PILOTOS ***
# -------------------------------------------------------------------------------------------------------------------

class ListaPilotosView(LoginRequiredMixin, ListView):
    """
    Vista para listar pilotos.
    Permite filtrar por nombre, apellido, ciudad y país.
    """
    model = Piloto
    template_name = 'pilotos/lista_pilotos.html'
    context_object_name = 'pilotos'

    def get_queryset(self):
        """
        Filtra la lista de pilotos según los parámetros de búsqueda.
        """
        queryset = Piloto.objects.select_related('user').all()
        query = self.request.GET.get('q', '')
        pais = self.request.GET.get('pais', '')

        if query:
            queryset = queryset.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(ciudad__icontains=query)
            )
        if pais:
            queryset = queryset.filter(pais__icontains=pais)
        
        return queryset

    def get_context_data(self, **kwargs):
        """
        Agrega al contexto una lista de países para el filtro desplegable.
        """
        context = super().get_context_data(**kwargs)
        context['paises'] = Piloto.objects.exclude(pais='').exclude(pais__isnull=True).values_list('pais', flat=True).distinct().order_by('pais')
        return context

class DetallePilotoView(LoginRequiredMixin, DetailView):
    model = Piloto
    template_name = 'pilotos/detalle_piloto.html'
    context_object_name = 'piloto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['puede_editar'] = user.is_superuser or user.groups.filter(name='TikNek').exists() # type: ignore
        return context

class PilotoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Piloto
    form_class = PilotoForm
    template_name = 'pilotos/editar_piloto.html'

    def get_success_url(self):
        messages.success(self.request, "Piloto actualizado correctamente.")
        return reverse_lazy('detalle_piloto', kwargs={'pk': self.object.pk}) # type: ignore

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='TikNek').exists() # type: ignore

class PilotoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Piloto
    template_name = 'pilotos/eliminar_piloto.html'
    context_object_name = 'piloto'

    def get_success_url(self):
        messages.success(self.request, "Piloto eliminado")
        return reverse_lazy('lista_pilotos')

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.groups.filter(name='TikNek').exists() # type: ignore
