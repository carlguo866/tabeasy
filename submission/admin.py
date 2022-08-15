from django.contrib import admin

# Register your models here.
from submission.models.ballot import Ballot
from submission.models.captains_meeting import CharacterPronouns, CaptainsMeeting, Character
from submission.models.section import Section, SubSection, BallotSection, CaptainsMeetingSection


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name','tournament']

@admin.register(SubSection)
class SubSectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'section','side','role']

class BallotSectionInlineAdmin(admin.TabularInline):
    model = BallotSection
    fields = ['subsection','score']

@admin.register(Ballot)
class BallotAdmin(admin.ModelAdmin):
    list_display = ['pk', 'round', 'judge', 'p_pd', 'd_pd','d_total_score','p_total_score', 'submit']
    list_filter = ['round__pairing', 'judge']
    search_fields = ['judge']
    inlines = [BallotSectionInlineAdmin]
    model = Ballot

class BallotInlineAdmin(admin.TabularInline):
    model = Ballot
    fields = ['judge']
    extra = 0
    show_change_link = True


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'side']
    # list_filter = ['tournament']
    search_fields = ['__str__']

class CharacterPronounsInlineAdmin(admin.TabularInline):
    model = CharacterPronouns
    fields = ['character','pronouns']
    extra = 0
    show_change_link = True


class CaptainsMeetingSectionInlineAdmin(admin.TabularInline):
    model = CaptainsMeetingSection
    fields = ['subsection', 'competitor']
    extra = 0
    show_change_link = True



@admin.register(CaptainsMeeting)
class CaptainsMeetingAdmin(admin.ModelAdmin):
    list_display = ['pk', '__str__', 'submit']
    list_filter = ['round__pairing']
    inlines = [CaptainsMeetingSectionInlineAdmin, CharacterPronounsInlineAdmin]
    search_fields = ['round__pairing','__str__']



