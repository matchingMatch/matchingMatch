from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore
from server.apps.matchingMatch.views import check_endOfGame


# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(schedule_api(), 'cron', second='*/10')
#     register_events(scheduler)

#     @scheduler.scheduled_job('cron', second='*/5', name='check_endOfGame')
#     def auto_check():
#         check_endOfGame()
#     scheduler.start()


# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
#     register_events(scheduler)

#     @scheduler.scheduled_job('cron', second='*/5', name='auto_check')
#     def auto_check():
#         check_endOfGame()
#     scheduler.start()


# def start():
#     scheduler = BackgroundScheduler()

#     # scheduler.add_job(schedule_api, 'interval', seconds=1)
#     scheduler.add_job(schedule_api, 'cron', seconds='*/5')
#     def auto_check():
#         check_endOfGame()
#     scheduler.start()
from datetime import datetime


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'djangojobstore')
    register_events(scheduler)

    @scheduler.scheduled_job('interval', minutes=10, name='auto_check')
    def auto_check():
        timeZone = datetime.now()
        print(f'Now: {timeZone.second}')
        print("This is SCHEDULER APPS PROCESSING")
        check_endOfGame()

    scheduler.start()
    scheduler.remove_jobstore('djangojobstore', shutdown=True)
