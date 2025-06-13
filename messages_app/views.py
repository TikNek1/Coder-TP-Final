from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm
from django.db.models import Q

@login_required
def inbox(request):
    """
    Vista para mostrar la bandeja de entrada del usuario autenticado.
    - Obtiene todos los usuarios excepto el usuario actual.
    - Identifica los usuarios con los que el usuario actual ha intercambiado mensajes.
    - Renderiza la plantilla 'inbox.html' con la lista de usuarios y chats activos.

    Contexto enviado al template:
    - users: Lista de todos los usuarios excepto el usuario actual.
    - active_chats: Lista de usuarios con los que el usuario actual ha intercambiado mensajes.
    """

    users = User.objects.exclude(id=request.user.id)

    # Usuarios con los que intercambió mensajes
    messages_sent = Message.objects.filter(sender=request.user).values_list('recipient', flat=True)
    messages_received = Message.objects.filter(recipient=request.user).values_list('sender', flat=True)
    chat_user_ids = set(messages_sent) | set(messages_received)

    active_chats = User.objects.filter(id__in=chat_user_ids).exclude(id=request.user.id)

    return render(request, "messages_app/inbox.html", {
        "users": users,
        "active_chats": active_chats
    })

@login_required
def chat_with_user_redirect(request):
    """
    Redirige al usuario a la conversación con otro usuario específico.
    - Si se proporciona un parámetro 'username' en la URL, redirige a la vista de conversación con ese usuario.
    - Si no se proporciona, redirige a la bandeja de entrada.

    Parámetros:
    - username (GET): Nombre de usuario del destinatario con el que se desea iniciar una conversación.
    """
    username = request.GET.get('username')
    if username:
        return redirect('conversation', username=username)
    return redirect('inbox')

@login_required
def conversation(request, username):
    """
    Vista para manejar la conversación entre el usuario autenticado y otro usuario.
    - Obtiene los mensajes entre el usuario actual y el usuario especificado.
    - Permite enviar nuevos mensajes mediante un formulario.

    Parámetros:
    - username: Nombre de usuario del destinatario con el que se está conversando.

    Contexto enviado al template:
    - chat_messages: Lista de mensajes entre el usuario actual y el destinatario.
    - form: Formulario para enviar un nuevo mensaje.
    - other_user: Usuario con el que se está conversando.
    """
    other_user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        recipient__in=[request.user, other_user]
    )

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = other_user
            msg.save()
            return redirect('conversation', username=other_user.username)
    else:
        # Si viene con un query param ?mensaje=..., se usa como valor inicial del form (para las preguntas por viajes!)
        mensaje_inicial = request.GET.get('mensaje')
        if mensaje_inicial:
            form = MessageForm(initial={'body': mensaje_inicial})
        else:
            form = MessageForm()

    return render(request, 'messages_app/conversation.html', {
        'chat_messages': messages,
        'form': form,
        'other_user': other_user,
    })