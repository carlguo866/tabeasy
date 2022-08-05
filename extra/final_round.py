from tourney.models import Round, Ballot, CaptainsMeeting



final_round = Round.objects.get(pairing__round_num=5)
for judge in final_round.judges:
    Ballot.objects.create(judge=judge, round=final_round)
CaptainsMeeting.objects.create(round=final_round)

# exec(open('extra/final_round.py').read())
