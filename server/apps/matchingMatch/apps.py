from django.apps import AppConfig
from django.conf import settings


class MatchingmatchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server.apps.matchingMatch'

    def ready(self):
        if settings.SCHEDULER_DEFAULT:
            from server.apps.matchingMatch.jobs import updater
            updater.start()
