# -*- coding: utf-8 -*-
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from datetime import datetime,timedelta
import logging
sched = BlockingScheduler()

def my_job():
    print 'my_job1 is running, Now is %s' % datetime.now().strftime("%Y-%m-%d %H:%M:%S")
sched.add_jobstore('sqlalchemy',url='mysql+mysqldb://root:123456@localhost:3306/scrapy?charset=utf8')
sched.add_job(my_job,'interval',id='myjob',seconds=5)

# def my_listener(event):
#     if event.exception:
#         print('The job crashed!')
#     else:
#         print('The job is working!')
#
# sched.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)  # DEBUG

fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)

sched.start()
# sched.remove_all_jobs()