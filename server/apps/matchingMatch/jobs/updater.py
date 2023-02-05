from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from server.apps.matchingMatch.views import check_endOfGame


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    @scheduler.scheduled_job('cron', second='*/5', name='check_endOfGame')
    def auto_check():
        check_endOfGame()
    scheduler.start()
