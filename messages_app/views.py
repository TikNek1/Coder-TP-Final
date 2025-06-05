from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm
from django.db.models import Q

@login_required
def inbox(request):
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
    username = request.GET.get('username')
    if username:
        return redirect('conversation', username=username)
    return redirect('inbox')

@login_required
def conversation(request, username):
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
        form = MessageForm()

    return render(request, 'messages_app/conversation.html', {
        'chat_messages': messages,
        'form': form,
        'other_user': other_user,
    })