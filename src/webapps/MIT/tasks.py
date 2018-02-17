# # Create your tasks here
# from celery import shared_task

#@shared_task
#def add(x, y):
#     return x + y


# @shared_task
# def mul(x, y):
#     return x * y


# @shared_task
# def xsum(numbers):
#     return sum(numbers)

from __future__ import absolute_import, unicode_literals
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from webapps.celery import app

from MIT.views import update, update_daily

@periodic_task(
    run_every=(crontab(minute='*/5')),
    name="update_stockinfo",
    ignore_result=True
)
def update_stockinfo():
    print "update_stockinfo"
    update()

# Execute daily at midnight.
@periodic_task(
    run_every=(crontab(minute=0, hour=0)),
    name="update_daily",
    ignore_result=True
)
def update_daily():
    print "update_daily"
    update_daily()
