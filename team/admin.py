from django.contrib import admin

from team.models import Team


# add the Team model for the admin interface
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'leader')
    list_display_links = ('id', )
    list_editable = ('name', 'leader')
    search_fields = ('name', 'leader')

    # fieldsets for the 'add' form for a new team
    add_fieldsets = (
        ('Team', {'fields': ('name', 'leader')}),
        ('Info', {'fields': ('description', 'member')})
    )

    # fieldsets for the 'add' form for a new team
    fieldsets = (
        ('Team', {'fields': ('name', 'leader')}),
        ('Info', {'fields': ('description', 'member')})
    )
