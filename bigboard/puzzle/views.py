from django.shortcuts import render, redirect
from django.conf import settings
from hunts.models import *
from puzzle.models import Tag

# Create your views here.
def add_puzzle(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    return render(request, 'puzzle/add_puzzle.html')

def puzzle(request, puzzid):    
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    puzzlist = Puzzle.objects.raw('SELECT hunts_puzzle.*, hunts_hunt.huntname FROM hunts_puzzle INNER JOIN hunts_huntuser ON hunts_huntuser.huntid_id = hunts_puzzle.huntid_id INNER JOIN hunts_hunt ON hunts_hunt.huntid = hunts_puzzle.huntid_id WHERE hunts_puzzle.puzzid = %s AND hunts_huntuser.user_id = %s LIMIT 1', [puzzid, request.user.id])          
    taglist = Tag.objects.filter(puzzid = puzzid)
    return render(request, 'puzzle/onepuzzle.html', {'puzzdata' : puzzlist, 'taglist' : taglist})
