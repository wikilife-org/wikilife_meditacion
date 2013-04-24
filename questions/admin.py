from questions.models import Poll, Choice, Chart, Contact
from django.contrib import admin

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['question','sequence', 'photo']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'sequence')
    search_fields = ['question']

class ChartAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['title','poll1', 'poll2', 'published', 'pie_chart']}),
    ]
    list_display = ('title', 'poll1', 'poll2', 'pie_chart')
    search_fields = ['title']

admin.site.register(Poll, PollAdmin)
admin.site.register(Chart, ChartAdmin)
admin.site.register(Contact)
