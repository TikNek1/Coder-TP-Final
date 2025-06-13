from django import template

# Registrar un nuevo módulo de etiquetas y filtros personalizados para usar en los templates de Django
register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    """
    Filtro personalizado para agregar clases CSS a un campo de formulario en un template de Django.

    Este filtro permite modificar dinámicamente los atributos de un campo de formulario
    desde el template, añadiendo una clase CSS específica.

    Uso en el template:
    {{ form.campo|add_class:"mi-clase-css" }}

    Parámetros:
    - field: El campo del formulario al que se le quiere agregar la clase CSS.
    - css: La clase CSS que se desea agregar al campo.

    Retorna:
    - El campo del formulario renderizado con la clase CSS añadida.
    """
    return field.as_widget(attrs={"class": css})