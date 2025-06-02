from django.db import models
from django.contrib.auth.models import User

class Arduino(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre