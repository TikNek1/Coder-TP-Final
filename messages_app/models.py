from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    """
    Modelo que representa un mensaje entre dos usuarios.
    - Cada mensaje tiene un remitente (sender) y un destinatario (recipient).
    - Contiene el cuerpo del mensaje (body) y un timestamp que indica cuándo fue enviado.
    """
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'De {self.sender} a {self.recipient}'