from django.db import models
from django.contrib.auth.models import User 

class TodoList(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=60)
    favorito = models.BooleanField(default=False)
    quantidade = models.IntegerField(default=1)


class DetalhesList(models.Model): 
    todo = models.OneToOneField(
        TodoList, 
        models.CASCADE,
        related_name="detalhe",)
    detalhes = models.TextField(blank=True, null=True)
    prioridade = models.CharField(max_length=10, choices=[("baixa", "Baixa"), ("media", "Media"), ("alta", "Alta")], default="media")
    concluido = models.BooleanField(default=False)
    def __str__(self): 
        return f'Detalhes de {self.todo.nome}'