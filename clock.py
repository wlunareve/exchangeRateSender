import os
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', hour = '*/1')
def scheduled_AUD_job():
    print('AUD crawl job is run every hour.')
    os.system("python currencyCrawler.py")

@sched.scheduled_job('cron', hour = '*/12')
def scheduled_currency_job():
    print('All currency crawl job is run every 12 hour.')
    os.system("python currencyCrawlerNew.py")

@sched.scheduled_job('cron', minute = '*/20')
def timed_job_awake_your_app():
    print('awake app every 20 minutes.')
    url = 'https://currencycrawlersender.herokuapp.com/'
    r = requests.get(url)
    
sched.start()
