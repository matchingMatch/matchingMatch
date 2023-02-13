from django.contrib import admin
from .models import Team, Stadium, MatchInfo, MatchRequest, Notice
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


class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'team_name', 'is_active']
    list_filter = ['is_active']
    actions = ['block', 'block_cancel']
    
    @admin.action(description='유저를 차단합니다.')
    def block(self, request, queryset):
        queryset.update(is_active=False)
    
    @admin.action(description='유저의 차단을 해제 합니다.')
    def block_cancel(self, request, queryset):
        queryset.update(is_active=True)
    
# Register your models here.
admin.site.register(Team, TeamAdmin)
admin.site.register(Stadium, PostAdmin)
admin.site.register(MatchInfo)
admin.site.register(MatchRequest)
admin.site.register(Notice)
