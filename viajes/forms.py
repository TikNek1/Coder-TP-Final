from django import forms
from .models import Viaje, Piloto
from django_ckeditor_5.widgets import CKEditor5Widget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class RegistroCompletoForm(UserCreationForm):
    # Campos adicionales del modelo Piloto
    dni = forms.CharField(max_length=20)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'dni', 'fecha_nacimiento']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Piloto.objects.create(
                user=user,
                dni=self.cleaned_data['dni'],
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento']
            )
        return user

class ViajeForm(forms.ModelForm):
    class Meta:
        model = Viaje
        fields = ['nombre', 'detalle', 'fecha_salida', 'cant_dias', 'km', 'dificultad', 'guia', 'pilotos', 'activo', 'max_pilotos']
        widgets = {
            # 'fecha_salida': forms.DateInput(attrs={'type': 'date'}),
            'fecha_salida': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'),
            'detalle': CKEditor5Widget(config_name='default'),
        }

    def __init__(self, *args, **kwargs):
        super(ViajeForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs['class'] = 'form-control'
        self.fields['pilotos'].widget.attrs['id'] = 'id_pilotos'
        self.fields['km'].label = 'Kilómetros'
        self.fields['max_pilotos'].label = 'Máxima cantidad de pilotos'
        #self.fields['fecha_salida'].widget.format = '%Y-%m-%d'
        

        # Campo guía: mostrar label según haya guías o no
        guia_field = self.fields.get('guia', None)
        if guia_field and hasattr(guia_field, 'queryset'):
            if not guia_field.queryset.exists(): # type: ignore
                guia_field.empty_label = 'Aún sin asignar' # type: ignore
            else:
                guia_field.empty_label = 'Seleccione una guía' # type: ignore

        # Estado (activo / borrador)
        self.fields['activo'] = forms.ChoiceField(
            choices=[(True, 'Activo'), (False, 'Borrador')],
            widget=forms.Select(attrs={'class': 'form-control'}),
            label='Estado'
        )