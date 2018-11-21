import os
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour = */1)
def scheduled_job():
    print('This job is run every day at UTC+8 8am.')
    os.system("python currencyCrawler.py")

@sched.scheduled_job('cron', minute = */20)
def timed_job_awake_your_app():
    print('awake app every 20 minutes.')
    url = 'https://currencycrawlersender.herokuapp.com/'
    r = requests.get(url)
    print(r.content)
    
sched.start()
