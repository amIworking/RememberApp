from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100, default='unknown')
    last_name = models.CharField(max_length=100, default='unknown')

    def __str__(self):
        return f"{self.username}, {self.email}"

