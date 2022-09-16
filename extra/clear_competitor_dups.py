from tourney.models import Competitor

for competitor in Competitor.objects.all():
    competitors = Competitor.objects.filter(name=competitor.name).all()
    if len(competitors) > 1:
        for i in range(1, len(competitors)):
            Competitor.objects.get(pk=competitors[i].pk).delete()