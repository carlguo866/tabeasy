from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView

from ballot.forms import BallotForm, BallotSectionForm
from ballot.models import Ballot
from ballot.models.section import BallotSection, Section, SubSection
from tabeasy.utils.mixins import PassRequestToFormViewMixin
from tabeasy_secrets.secret import str_int, TOURNAMENT_NAME




class BallotUpdateView(LoginRequiredMixin, UserPassesTestMixin, PassRequestToFormViewMixin, UpdateView):
    model = Ballot
    template_name = "tourney/ballot.html"
    form_class = BallotForm
    permission_denied_message = 'You are not allowed to view this ballot.'

    def test_func(self):
        self.ballot = get_object_or_404(Ballot, pk=str_int(self.kwargs['encrypted_pk']))
        if self.request.user.is_staff:
            return True
        if self.request.user.is_judge and self.ballot.judge != self.request.user.judge:
            return False
        if self.request.user.is_team and \
            self.request.user.team not in self.ballot.round.teams:
            return False
        return True

    def get_object(self, queryset=None):
        return Ballot.objects.get(pk=str_int(self.kwargs['encrypted_pk']))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section_forms'] = []
        if BallotSection.objects.filter(ballot=self.object).exists():
            for section in Section.objects.filter(tournament__name=TOURNAMENT_NAME).all():
                context['section_forms'].append(
                    sorted([BallotSectionForm(instance=ballot_section,
                                       subsection=ballot_section.subsection,
                                       prefix=ballot_section.subsection.__str__())
                     for ballot_section in
                     BallotSection.objects.filter(ballot=self.object, subsection__section=section).all()
                     ],key= lambda x: x.init_subsection.sequence)
                )
        else:
            for section in Section.objects.filter(tournament__name=TOURNAMENT_NAME).all():
                context['section_forms'].append(
                    sorted([BallotSectionForm(subsection=subsection, ballot=self.object,
                                      prefix=subsection.__str__())
                    for subsection in
                    SubSection.objects.filter(section=section).all()],
                    key= lambda x: x.init_subsection.sequence)
                )

        context['section_forms'] = sorted(context['section_forms'],
                                    key= lambda x: x[0].init_subsection.sequence)
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        section_forms = []
        if BallotSection.objects.filter(ballot=self.object).exists():
            for section in Section.objects.filter(tournament__name=TOURNAMENT_NAME).all():
                section_forms.append(
                    sorted([BallotSectionForm(request.POST, instance=ballot_section,
                                       subsection=ballot_section.subsection,
                                       prefix=ballot_section.subsection.__str__())
                     for ballot_section in
                     BallotSection.objects.filter(ballot=self.object, subsection__section=section).all()
                     ], key= lambda x: x.init_subsection.sequence)
                )
        else:
            for section in Section.objects.filter(tournament__name=TOURNAMENT_NAME).all():
                section_forms.append(
                    sorted([BallotSectionForm(request.POST, subsection=subsection, ballot=self.object,
                                      prefix=subsection.__str__())
                     for subsection in
                     SubSection.objects.filter(section=section).all()],
                    key= lambda x: x.init_subsection.sequence)
                )
        section_forms = sorted(section_forms, key=lambda x: x[0].init_subsection.sequence)
        is_valid = True
        for section in section_forms:
            for subsection_form in section:
                if not subsection_form.is_valid():
                    raise ValidationError(subsection_form.errors)
                    is_valid = False
        if not form.is_valid():
            is_valid = False
        if is_valid:
            return self.form_valid(form, section_forms)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, section_forms):
        for section in section_forms:
            for subsection_form in section:
                subsection_form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return self.request.path