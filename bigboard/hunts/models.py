from django.db import models
from puzzle.models import *
from django.contrib.auth.models import User

class Hunt(models.Model):
     huntid = models.AutoField(primary_key=True)
     huntname = models.CharField('Hunt Name', max_length=120)
     last_update = models.DateTimeField('Last Updated')
     active = models.SmallIntegerField('Active')

     def __str__(self):
         return str(self.huntid)

class Puzzle(models.Model):
     puzzid = models.AutoField(primary_key=True)
     puzzname = models.CharField('Puzzle Name', max_length=120)
     last_update = models.DateTimeField('Last Updated')
     huntid = models.ForeignKey(Hunt, null=True, on_delete=models.SET_NULL) 
     isMeta = models.SmallIntegerField('Metapuzzle')
     active = models.SmallIntegerField('Active')
     url = models.URLField('URL')
     discordchannelid = models.BigIntegerField('Discord ID', default='0')
     googlesheet = models.CharField('Google Sheets Link', max_length=120, null=True)
     priority = models.SmallIntegerField('Priority', default='0')

     def __str__(self):
         return str(self.puzzid)

class Round(models.Model):
     roundid = models.AutoField(primary_key=True)
     roundname = models.CharField('Round Name', max_length=120)
     last_update = models.DateTimeField('Last Updated')
     huntid = models.ForeignKey(Hunt, null=True, on_delete=models.SET_NULL)
     active = models.SmallIntegerField('Active')
     discordchannelid = models.BigIntegerField('Discord ID', default='0')
     
     def __str__(self):
         return str(self.roundid)

class PuzzRound(models.Model):
     id = models.AutoField(primary_key=True)
     puzzid = models.ForeignKey(Puzzle, null=True, on_delete=models.SET_NULL)
     roundid = models.ForeignKey(Round, null=True, on_delete=models.SET_NULL)
     
     def __str__(self):
         return str(self.id)

class Answer(models.Model):
     answerid = models.AutoField(primary_key=True)
     answer = models.CharField('Round Name', max_length=120)
     last_update = models.DateTimeField('Last Updated')
     puzzid = models.ForeignKey(Puzzle, null=True, on_delete=models.SET_NULL)
     
     def __str__(self):
         return str(self.answerid)

class HuntUser(models.Model):
     permissionid = models.AutoField(primary_key=True)
     huntid = models.ForeignKey(Hunt, null=True, on_delete=models.SET_NULL)
     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
     
     def __str__(self):
         return str(self.huntid) + ' ' + str(self.user)

