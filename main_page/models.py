from django.db import models
import time
from django.utils import timezone
from users.models import User

# Create your models here.
class Dictionary(models.Model):
   #current_time = time.strftime('%d.%m.%Y %H:%M', time.localtime())
   level_choices = [("A1","A1"),
                    ("A2","A2"),
                    ("B1","B1"),
                    ("B2","B2"),
                    ("C1","C1"),
                    ("C2","C2")]
   name = models.CharField(max_length=255, unique=True)
   lang_from = models.CharField(max_length=3, default="EN")
   lang_to = models.CharField(max_length=3, default="RU")
   owner = models.ForeignKey(User, on_delete=models.CASCADE)
   private = models.BooleanField(default=False)
   level = models.CharField(max_length=2, choices=level_choices)
   raiting = models.IntegerField(null=True)
   creation_date = models.DateField(default=timezone.now)
   def __str__(self):
      return f"{self.name}, {self.lang_from}, {self.lang_to}, {self.owner}"

class Translates(models.Model):
   dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
   word = models.CharField(max_length=255)
   translate = models.CharField(max_length=255)

   def __str__(self):
      return f"{self.dictionary}, {self.word}, {self.translate}"


