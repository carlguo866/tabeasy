from ajax_select import register, LookupChannel
from .models import Team

@register('p_team')
class PTeamLookup(LookupChannel):

    model = Team

    def get_query(self, q, request):
        return self.model.objects.filter(team_name__icontains=q).order_by('team_name')[:50]

    def format_item_display(self, item):
        return u"<div class='tag'>%s</div>" % item.team_name