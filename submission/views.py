from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from submission.forms import BallotForm, BallotSectionForm, CaptainsMeetingForm, CharacterPronounsForm, \
    CaptainsMeetingSectionForm, ParadigmForm, ParadigmPreferenceItemForm
from submission.models.ballot import Ballot
from submission.models.captains_meeting import CaptainsMeeting
from submission.models.character import CharacterPronouns, Character
from submission.models.paradigm import ParadigmPreference, ParadigmPreferenceItem, Paradigm
from submission.models.section import BallotSection, Section, SubSection, CaptainsMeetingSection
from tabeasy.utils.mixins import PassRequestToFormViewMixin
from tabeasy_secrets.secret import str_int
from tourney.models import Judge


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
            for section in Section.objects.filter(tournament=self.object.judge.user.tournament).all():
                context['section_forms'].append(
                    sorted([BallotSectionForm(instance=ballot_section,
                                       subsection=ballot_section.subsection,
                                       prefix=ballot_section.subsection.__str__(),
                                       request=self.request)
                     for ballot_section in
                     BallotSection.objects.filter(ballot=self.object, subsection__section=section).all()
                     ],key= lambda x: x.init_subsection.sequence)
                )
        else:
            for section in Section.objects.filter(tournament=self.object.judge.user.tournament).all():
                context['section_forms'].append(
                    sorted([BallotSectionForm(subsection=subsection, ballot=self.object,
                                      prefix=subsection.__str__(),
                                      request=self.request)
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
            for section in Section.objects.filter(tournament=self.object.judge.user.tournament).all():
                section_forms.append(
                    sorted([BallotSectionForm(request.POST, instance=ballot_section,
                                       subsection=ballot_section.subsection,
                                       prefix=ballot_section.subsection.__str__(),
                                       request=self.request)
                     for ballot_section in
                     BallotSection.objects.filter(ballot=self.object, subsection__section=section).all()
                     ], key= lambda x: x.init_subsection.sequence)
                )
        else:
            for section in Section.objects.filter(tournament=self.object.judge.user.tournament).all():
                section_forms.append(
                    sorted([BallotSectionForm(request.POST, subsection=subsection, ballot=self.object,
                                      prefix=subsection.__str__(), request=self.request)
                     for subsection in
                     SubSection.objects.filter(section=section).all()],
                    key= lambda x: x.init_subsection.sequence)
                )
        section_forms = sorted(section_forms, key=lambda x: x[0].init_subsection.sequence)
        is_valid = True
        for section in section_forms:
            for subsection_form in section:
                if not subsection_form.is_valid():
                    is_valid = False
                # if subsection_form.cleaned_data.get('score') == 0:
                #     subsection_form.errors['zero'] = f'You cannot score a 0 for {subsection_form.instance}!'
                #     is_valid = False
        if not form.is_valid():
            is_valid = False
        if is_valid:
            return self.form_valid(form, section_forms)
        else:
            return self.form_invalid(form, section_forms)

    def form_valid(self, form, section_forms):
        for section in section_forms:
            for subsection_form in section:
                subsection_form.save()

        return super().form_valid(form)

    def form_invalid(self, form, section_forms):
        context = self.get_context_data()
        context['section_forms'] = section_forms
        return self.render_to_response(context)

    def get_success_url(self):
        if self.ballot.submit:
            for opponent in self.ballot.round.p_team.opponents():
                opponent.save()
            for opponent in self.ballot.round.d_team.opponents():
                opponent.save()
            self.ballot.round.p_team.save()
            self.ballot.round.d_team.save()
            for opponent in self.ballot.round.p_team.opponents():
                opponent.save()
            for opponent in self.ballot.round.d_team.opponents():
                opponent.save()
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
            context['pronouns_forms'] = [CharacterPronounsForm(instance=character_pronouns,
                                                               character=character_pronouns.character, captains_meeting=self.object,
                                                               prefix=character_pronouns.character.__str__())
                                         for character_pronouns in
                                         CharacterPronouns.objects.filter(captains_meeting=self.object).all()]
        else:
            context['pronouns_forms'] = [CharacterPronounsForm(character=character, captains_meeting=self.object,
                                                               prefix=character.__str__())
                                         for character in Character.objects.filter(tournament=self.object.round.pairing.tournament).all()]

        context['section_forms'] = []
        if CaptainsMeetingSection.objects.filter(captains_meeting=self.object).exists():
            for section in Section.objects.filter(tournament=self.object.round.pairing.tournament).all():
                temp = []
                for subsection in CaptainsMeetingSection.objects.filter(captains_meeting=self.object,
                                                          subsection__section=section).all():
                    if not (subsection.subsection.type == 'cross' and \
                        subsection.subsection.role == 'wit'):
                        temp.append(
                            CaptainsMeetingSectionForm(instance=subsection,
                                                       captains_meeting=self.object,
                                                       subsection=subsection.subsection,
                                                       prefix=subsection.subsection.__str__(),
                                                       request=self.request)
                        )
                temp = sorted(temp, key= lambda x: x.init_subsection.sequence)
                context['section_forms'].append(temp)
        else:
            for section in Section.objects.filter(tournament=self.object.round.pairing.tournament).all():
                temp = []
                for subsection in SubSection.objects.filter(section=section).all():
                    if not (subsection.type == 'cross' and \
                            subsection.role == 'wit'):
                        temp.append(
                            CaptainsMeetingSectionForm(subsection=subsection, captains_meeting=self.object,
                                          prefix=subsection.__str__(), request=self.request)
                        )
                temp = sorted(temp, key=lambda x: x.init_subsection.sequence)
                context['section_forms'].append(temp)
        context['section_forms'] = sorted(context['section_forms'],
                                    key= lambda x: x[0].init_subsection.sequence)

        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if CharacterPronouns.objects.filter(captains_meeting=self.object).exists():
            pronouns_forms = [CharacterPronounsForm(request.POST, instance=character_pronouns,
                                                    character=character_pronouns.character,
                                                    captains_meeting=self.object,
                                                    prefix=character_pronouns.character.__str__(),
                                                    form=form)
                              for character_pronouns in
                              CharacterPronouns.objects.filter(captains_meeting=self.object).all()]
        else:
            pronouns_forms = [CharacterPronounsForm(request.POST, character=character, captains_meeting=self.object,
                                                    prefix=character.__str__(), form=form)
                              for character in Character.objects.filter(tournament=self.object.round.pairing.tournament)]


        section_forms = []
        if CaptainsMeetingSection.objects.filter(captains_meeting=self.object).exists():
            for section in Section.objects.filter(tournament=self.object.round.pairing.tournament).all():
                temp = []
                for subsection in CaptainsMeetingSection.objects.filter(captains_meeting=self.object,
                                                                           subsection__section=section).all():
                    if not (subsection.subsection.type == 'cross' and \
                        subsection.subsection.role == 'wit'):
                        temp.append(
                            CaptainsMeetingSectionForm(request.POST, instance=subsection,
                                                       captains_meeting=self.object,
                                                       subsection=subsection.subsection,
                                                       prefix=subsection.subsection.__str__(),
                                                       form=form, request=self.request)
                        )
                temp = sorted(temp, key=lambda x: x.init_subsection.sequence)
                section_forms.append(temp)
        else:
            for section in Section.objects.filter(tournament=self.object.round.pairing.tournament).all():
                temp = []
                for subsection in SubSection.objects.filter(section=section).all():
                    if not (subsection.type == 'cross' and \
                            subsection.role == 'wit'):
                        temp.append(
                            CaptainsMeetingSectionForm(request.POST, subsection=subsection,
                                                       captains_meeting=self.object,
                                                       prefix=subsection.__str__(),
                                                       form=form,request=self.request)
                        )
                temp = sorted(temp, key=lambda x: x.init_subsection.sequence)
                section_forms.append(temp)

        section_forms = sorted(section_forms,
                                    key= lambda x: x[0].init_subsection.sequence)

        is_valid = True

        if not form.is_valid():
            is_valid = False

        for pronouns_form in pronouns_forms:
            if not pronouns_form.is_valid():
                is_valid = False

        characters = []
        wits = []
        direct_atts = []
        cross_atts = []
        speeches = []
        for section in section_forms:
            for subsection_form in section:
                if not subsection_form.is_valid():
                    is_valid = False
                elif form.cleaned_data.get('submit'):
                    #check for character
                    character = subsection_form.cleaned_data.get('character')
                    if character in characters:
                        is_valid = False
                        subsection_form.errors['character'] = "Each witness can only be called once."
                    elif character:
                        characters.append(character)

                    if subsection_form.instance.subsection.role == 'wit' and \
                        subsection_form.instance.subsection.type == 'direct':
                        competitor = subsection_form.cleaned_data.get('competitor')
                        if competitor in wits:
                            is_valid = False
                            subsection_form.errors['wits'] = f"{competitor} is portraying two witnesses."
                        elif competitor:
                            wits.append(competitor)

                    if subsection_form.instance.subsection.role == 'att' and \
                            subsection_form.instance.subsection.type == 'direct':
                        competitor = subsection_form.cleaned_data.get('competitor')
                        if competitor in direct_atts:
                            is_valid = False
                            subsection_form.errors['direct_atts'] = f"{competitor} is doing two directs."
                        elif competitor:
                            direct_atts.append(competitor)

                    if subsection_form.instance.subsection.role == 'att' and \
                            subsection_form.instance.subsection.type == 'cross':
                        competitor = subsection_form.cleaned_data.get('competitor')
                        if competitor in cross_atts:
                            is_valid = False
                            subsection_form.errors['cross_atts'] = f"{competitor} is doing two crosses."
                        elif competitor:
                            cross_atts.append(competitor)

                    if subsection_form.instance.subsection.role == 'att' and \
                            subsection_form.instance.subsection.type == 'statement':
                        competitor = subsection_form.cleaned_data.get('competitor')
                        if competitor in speeches:
                            is_valid = False
                            subsection_form.errors['speeches'] = f"{competitor} is doing both opening and closing."
                        elif competitor:
                            speeches.append(competitor)

        if form.cleaned_data.get('submit'):
            if direct_atts and cross_atts and \
                sorted(direct_atts) != sorted(cross_atts):
                is_valid = False
                section_forms[0][0].errors['atts_num'] = 'The crossing attorneys and directing attorneys have a mismatch.'
            for wit in wits:
                if wit in direct_atts or wit in cross_atts:
                    is_valid = False
                    section_forms[0][0].errors[
                        'att_n_wit'] = f'{wit} assigned as both an attorney and witness.'


        if is_valid:
            return self.form_valid(form, pronouns_forms, section_forms)
        else:
            return self.form_invalid(form, pronouns_forms, section_forms)

    def form_valid(self, form, pronouns_forms, section_forms):
        for pronouns_form in pronouns_forms:
            # pronouns_form.instance.captains_meeting = self.object
            pronouns_form.save()
        for section in section_forms:
            for subsection_form in section:
                subsection_form.save()

                if subsection_form.init_subsection.role == 'wit' and \
                        subsection_form.init_subsection.type == 'direct':
                    subsection = SubSection.objects.get(section=subsection_form.init_subsection.section,
                                                        role=subsection_form.init_subsection.role,
                                                        type='cross')
                    if CaptainsMeetingSection.objects.filter(captains_meeting=subsection_form.init_captains_meeting,
                                                             subsection=subsection
                                                             ).exists():
                        CaptainsMeetingSection.objects.filter(captains_meeting=subsection_form.init_captains_meeting,
                                                              subsection=subsection
                                                              ).update(competitor=subsection_form.instance.competitor,
                                                                       character=subsection_form.instance.character)
                    else:
                        CaptainsMeetingSection.objects.create(
                            captains_meeting=subsection_form.init_captains_meeting,
                            subsection=subsection,
                            competitor=subsection_form.instance.competitor,
                            character=subsection_form.instance.character
                        )

        return super().form_valid(form)

    def form_invalid(self, form, pronouns_forms, section_forms):
        context = self.get_context_data()
        context['pronouns_forms'] = pronouns_forms
        context['section_forms'] = section_forms
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse_lazy('index')

def edit_paradigm(request, judge):
    judge = Judge.objects.get(user__username=judge)
    if Paradigm.objects.filter(judge=judge).exists():
        paradigm = Paradigm.objects.get(judge=judge)
    else:
        paradigm = Paradigm.objects.create(judge=judge)

    if request.method == "POST":
        paradigm_form = ParadigmForm(request.POST, instance=paradigm)
        if ParadigmPreferenceItem.objects.filter(paradigm=paradigm).exists():
            paradigm_preference_item_forms = [
                ParadigmPreferenceItemForm(request.POST, instance=each, prefix=each.__str__())
                for each in ParadigmPreferenceItem.objects.filter(paradigm=paradigm).all()
            ]
        else:
            paradigm_preference_item_forms = [
                ParadigmPreferenceItemForm(request.POST, paradigm=paradigm, paradigm_preference=each,
                                           prefix=each.__str__())
                for each in ParadigmPreference.objects.all()
            ]

        is_true = True

        if paradigm_form.is_valid():
            paradigm_form.save()
        else:
            is_true = False

        for form in paradigm_preference_item_forms:
            if form.is_valid():
                form.save()
            else:
                is_true = False

        if is_true:
            return redirect('index')

    else:
        paradigm_form = ParadigmForm(instance=paradigm)
        if ParadigmPreferenceItem.objects.filter(paradigm=paradigm).exists():
            paradigm_preference_item_forms = [
                ParadigmPreferenceItemForm(instance=each, prefix=each.__str__())
                for each in ParadigmPreferenceItem.objects.filter(paradigm=paradigm).all()
            ]
        else:
            paradigm_preference_item_forms = [
                ParadigmPreferenceItemForm(paradigm=paradigm, paradigm_preference=each,
                                           prefix=each.__str__())
                for each in ParadigmPreference.objects.all()
            ]

    return render(request, 'tourney/paradigm.html', {'judge': judge,
                                                     'paradigm_form':paradigm_form,
                                                     'forms': paradigm_preference_item_forms})

