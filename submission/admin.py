from django.contrib import admin

# Register your models here.
from submission.models.ballot import Ballot
from submission.models.section import Section, SubSection, BallotSection


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
