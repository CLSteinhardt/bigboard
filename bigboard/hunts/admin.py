from django.contrib import admin
from .models import *
from puzzle.models import *

# Register your models here.
admin.site.register(Hunt)
admin.site.register(Round)
admin.site.register(PuzzRound)
admin.site.register(Puzzle)
admin.site.register(Answer)
admin.site.register(HuntUser)
