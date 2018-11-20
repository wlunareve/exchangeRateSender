import os
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour = 1)
def scheduled_job():
    print('This job is run every day at UTC+8 8am.')
    os.system("python currencyCrawler.py")


sched.start()