from django.db import models

import main_page.models


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    added_dicts = models.ManyToManyField('main_page.Dictionary')
    points = models.IntegerField(default=0)
    user_level = models.IntegerField(default=0)



