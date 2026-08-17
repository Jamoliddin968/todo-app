from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-id"]