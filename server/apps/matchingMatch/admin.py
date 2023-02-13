from django.contrib import admin
from .models import Team, Stadium, MatchInfo, MatchRequest
from import_export import resources
from import_export.admin import ImportExportModelAdmin


class StadiumResource(resources.ModelResource):
    class Meta:
        model = Stadium
        fields = ('id', 'location', 'stadium_name', 'address')


class PostAdmin(ImportExportModelAdmin):
    fields = ('location', 'stadium_name', 'address')
    list_display = ('id', 'location', 'stadium_name', 'address')
    resource_class = StadiumResource


# Register your models here.
admin.site.register(Team)
admin.site.register(Stadium, PostAdmin)
admin.site.register(MatchInfo)
admin.site.register(MatchRequest)
