from django.db import models
import time
from django.utils import timezone
from users.models import User

# Create your models here.
class Dictionary(models.Model):
   #current_time = time.strftime('%d.%m.%Y %H:%M', time.localtime())
   name = models.CharField(max_length=255, unique=True)
   lang_from = models.CharField(max_length=255, blank=True, null=True)
   lang_to = models.CharField(max_length=255, blank=True, null=True)
   creation_date = models.DateField(default=timezone.now)
   owner_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
   def __str__(self):
      return f"{self.name}, {self.lang_from}, {self.lang_to}, {self.owner_id}"

class Translates(models.Model):
   dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
   word = models.CharField(max_length=255)
   translate = models.CharField(max_length=255)

   def __str__(self):
      return f"{self.dictionary}, {self.word}, {self.translate}"


