from django.contrib import admin

from . models import Country, Driver, GrandPrix, Standing, Team, Transfer


class CountryAdmin(admin.ModelAdmin):
    list_display = ('country', 'country_abbr')
    search_fields = ('country',)


class DriverAdmin(admin.ModelAdmin):
    list_display = ('driver', 'driver_abbr', 'date_of_birth', 'country')
    list_filter = ('country',)
    search_fields = ('driver',)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('team', 'country')
    list_filter = ('country',)
    search_fields = ('team',)


class GrandPrixAdmin(admin.ModelAdmin):
    list_display = ('grand_prix', 'gp_abbr', 'country')
    list_filter = ('country',)


class StandingAdmin(admin.ModelAdmin):
    list_display = ('grand_prix', 'event_date', 'driver', 'pos', 'pts', 'pp', 'fl')
    list_filter = ('grand_prix', 'driver', 'pos')
    date_hierarchy = 'event_date'


class TransferAdmin(admin.ModelAdmin):
    list_display = ('driver', 'team', 'start_date', 'end_date')
    list_filter = ('team', 'driver')


admin.site.register(Country, CountryAdmin)
admin.site.register(Driver, DriverAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(GrandPrix, GrandPrixAdmin)
admin.site.register(Standing, StandingAdmin)
admin.site.register(Transfer, TransferAdmin)