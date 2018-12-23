from django.shortcuts import render, redirect
from django.conf import settings
from hunts.models import *

# Create your views here.
def add_hunt(request):
    return render(request, 'hunts/add_hunt.html')

def all_hunts(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    huntlist = Hunt.objects.raw('SELECT hunts_hunt.* FROM hunts_hunt INNER JOIN hunts_huntuser ON hunts_hunt.huntid = hunts_huntuser.huntid_id WHERE user_id = %s', [request.user.id])
    return render(request, 'hunts/all_hunts.html', {'hunts' : huntlist})

def hunt(request, huntid):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))   
    hunt = Hunt.objects.filter(huntid = huntid)
    roundlist = Round.objects.raw('SELECT COUNT(*), hunts_round.roundid, roundname FROM hunts_puzzle INNER JOIN hunts_puzzround ON hunts_puzzle.puzzid = hunts_puzzround.puzzid_id INNER JOIN hunts_round ON hunts_puzzround.roundid_id = hunts_round.roundid LEFT JOIN hunts_answer ON hunts_answer.puzzid_id = hunts_puzzle.puzzid INNER JOIN hunts_huntuser ON hunts_huntuser.huntid_id = %s WHERE hunts_round.huntid_id = %s AND hunts_round.active = 1 AND hunts_puzzle.active = 1 AND hunts_huntuser.user_id = %s GROUP BY roundid, roundname ORDER BY roundid ASC;', [huntid, huntid, request.user.id])
    puzzlist = []
    print(roundlist)
    for r in roundlist:
        plist = Puzzle.objects.raw('SELECT puzzid, puzzname, hunts_puzzle.last_update, hunts_puzzle.isMeta, hunts_round.roundid, hunts_answer.answer, hunts_round.roundname FROM hunts_puzzle INNER JOIN hunts_puzzround ON hunts_puzzle.puzzid = hunts_puzzround.puzzid_id INNER JOIN hunts_round ON hunts_puzzround.roundid_id = hunts_round.roundid LEFT JOIN hunts_answer ON hunts_answer.puzzid_id = hunts_puzzle.puzzid WHERE hunts_round.huntid_id = %s AND hunts_round.active = 1 AND hunts_puzzle.active = 1 AND hunts_round.roundid = %s ORDER BY isMeta DESC, puzzname ASC;', [huntid, r.roundid])
        puzzlist.append(plist)  
    return render(request, 'hunts/base_hunt.html', {'rounds' : roundlist, 'puzzles' : puzzlist, 'hunt' : hunt})
