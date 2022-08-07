from tourney.models import Round, Ballot, CaptainsMeeting, Pairing, Team


# pairing = Pairing.objects.create(round_num=5, division='Disney',team_submit=True,final_submit=True)
# p_team = Team.objects.get(pk=1)
# d_team = Team.objects.get(pk=4)
# if pairing.rounds.count() == 0:
#
# final_round = Round.objects.create(pairing=pairing,courtroom='A',p_team=p_team,d_team=d_team,
# #                                    presiding_judge=)
final_round = Round.objects.get(pairing__round_num=5)
for judge in final_round.judges:
    Ballot.objects.create(judge=judge, round=final_round)
CaptainsMeeting.objects.create(round=final_round)

# exec(open('extra/final_round.py').read())
