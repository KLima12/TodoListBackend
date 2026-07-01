from django.db import models
from django.contrib.auth.models import User 

class TodoList(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=60)
    favorito = models.BooleanField(default=False)
    quantidade = models.IntegerField(default=1)