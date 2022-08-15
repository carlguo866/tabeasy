from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from submission.forms import BallotForm, BallotSectionForm, CaptainsMeetingForm, EditPronounsForm
from submission.models.ballot import Ballot
from submission.models.captains_meeting import CaptainsMeeting, CharacterPronouns, Character
from submission.models.section import BallotSection, Section, SubSection
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



class CaptainsMeetingUpdateView(LoginRequiredMixin, UserPassesTestMixin, PassRequestToFormViewMixin, UpdateView):
    model = CaptainsMeeting
    template_name = "tourney/captains_meeting.html"
    form_class = CaptainsMeetingForm
    permission_denied_message = 'You are not allowed to view this Captains Meeting Form.'

    def test_func(self):
        self.captains_meeting = get_object_or_404(CaptainsMeeting, pk=str_int(self.kwargs['encrypted_pk']))
        if self.request.user.is_staff:
            return True
        if self.request.user.is_team and self.request.user.team not in self.captains_meeting.round.teams:
            return False
        if self.request.user.is_judge and \
                self.request.user.judge not in self.captains_meeting.round.judges:
            return False
        return True

    def get_object(self, queryset=None):
        return CaptainsMeeting.objects.get(pk=str_int(self.kwargs['encrypted_pk']))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if CharacterPronouns.objects.filter(captains_meeting=self.object).exists():
            context['forms'] = [EditPronounsForm(instance=character_pronouns,
                                                 character=character_pronouns.character,captains_meeting=self.object,
                                                 prefix=character_pronouns.character.__str__())
                                for character_pronouns in
                                CharacterPronouns.objects.filter(captains_meeting=self.object).all()]
        else:
            context['forms'] = [EditPronounsForm(character=character,captains_meeting=self.object,
                                                 prefix=character.__str__())
                 for character in Character.objects.filter(tournament__name=TOURNAMENT_NAME).all()]
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if CharacterPronouns.objects.filter(captains_meeting=self.object).exists():
            forms = [EditPronounsForm(request.POST, instance=character_pronouns,
                                                 character=character_pronouns.character,
                                                captains_meeting=self.object,
                                                 prefix=character_pronouns.character.__str__())
                                for character_pronouns in
                                CharacterPronouns.objects.filter(captains_meeting=self.object).all()]
        else:
            forms = [EditPronounsForm(request.POST, character=character,captains_meeting=self.object, prefix=character.__str__())
                       for character in Character.objects.all()]
        is_valid = True
        for pronouns_form in forms:
            if not pronouns_form.is_valid():
                raise ValidationError(pronouns_form.errors)
                is_valid = False
        if not form.is_valid():
            is_valid = False
        if is_valid:
            return self.form_valid(form, forms)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, forms):
        for pronouns_form in forms:
            # pronouns_form.instance.captains_meeting = self.object
            pronouns_form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('index')