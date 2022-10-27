from django.db import models
import time
struct = time.localtime()
current_time = time.strftime('%d.%m.%Y %H:%M', struct)


# Create your models here.
class Dictionary(models.Model):
   name = models.CharField(max_length=40)
   lang_from = models.CharField(max_length=40, default='unknown')
   lang_to = models.CharField(max_length=40, default='unknown')
   creation_date = models.CharField(max_length=40,default=current_time)

   def __str__(self):
      return f"{self.name}, {self.lang_from}, {self.lang_to}"

class Translates(models.Model):
   dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE)
   word = models.CharField(max_length=40)
   translate = models.CharField(max_length=40)

   def __str__(self):
      return f"{self.dictionary}, {self.word}, {self.translate}"


