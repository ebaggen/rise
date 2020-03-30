from datetime import datetime, timedelta
from functools import reduce
from flask_backend.models import db, Alarm
from flask_backend import rq
from redis import Redis
from rq_scheduler import Scheduler
from paho.mqtt.client import Client

client = Client()

scheduler = Scheduler(connection=Redis(), interval=1)
#default_queue = rq.get_queue()

#default_worker = rq.get_worker()
#default_worker.work(burst=True)

#scheduler = rq.get_scheduler(interval=1)
#scheduler.run()


#@rq.job
def notify_alarm():
    print('notify alarm')
    client.connect('localhost')
    client.publish('rise/alarm/wake-up')
    client.disconnect()

    # Schedule next alarm
    schedule_alarm()


#@rq.job
def notify_alarm_warning():
    print('notify warning')
    client.connect('localhost')
    client.publish('rise/alarm/30-min-warning')
    client.disconnect()


def schedule_alarm():
    pass
    # Cancel all alarms
    for job, time in scheduler.get_jobs(with_times=True):
        print('canceling job: ', time)
        scheduler.cancel(job)

    # Get the next alarm by filtering by next occurrence
    next_alarm = reduce(
        lambda a, b: a if a.next_occurrence() < b.next_occurrence() else b, db.session.query(Alarm).all()
    )

    # If the alarm is enabled (this will only catch cases where NO alarms are enabled or exist
    if next_alarm and next_alarm.enabled:
        # Schedule MQTT calls appropriate times
        scheduler.enqueue_at(next_alarm.next_occurrence(), notify_alarm)
        #notify_alarm.queue(next_alarm.next_occurrence())
        print('scheduled notify_alarm at ', next_alarm.next_occurrence())

        # Only schedule upcoming events if there is enough time
        if datetime.now() < next_alarm.next_occurrence() - timedelta(seconds=30):
            scheduler.enqueue_at(next_alarm.next_occurrence() - timedelta(seconds=30), notify_alarm_warning)
            #notify_alarm_warning.queue(next_alarm.next_occurrence() - timedelta(seconds=30))
            print('scheduled notify_alarm_warning at ', next_alarm.next_occurrence() - timedelta(seconds=30))
