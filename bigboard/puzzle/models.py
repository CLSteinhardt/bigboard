from django.db import models
from hunts.models import *

# Create your models here.
class Tag(models.Model):
     tagid = models.AutoField(primary_key=True)
     tag = models.CharField('Tag', max_length=120)
     puzzid = models.ForeignKey(Puzzle, null=True, on_delete=models.SET_NULL)
     
     def __str__(self):
         return str(self.tagid)

     
