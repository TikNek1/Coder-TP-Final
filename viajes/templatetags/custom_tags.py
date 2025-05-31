from django import template

register = template.Library()

# esto es para controlar el acceso a boton de agregar, tiene que ser un usuario con grupo asignado
@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()