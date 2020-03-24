from time import sleep
from db import Session
from db.models import Alarm
from datetime import datetime, timedelta
from clock_engine.controllers.hue import HueController
from clock_engine.controllers.sonos import SonosController


# Converts an Alarm object to a datetime nearest a provided a datetime
def alarm_to_datetime(alarm: Alarm, now: datetime) -> datetime:

    # If alarm is NOT repeated, then the alarm is scheduled for its time within the next 24 hours
    if not alarm.repeat:

        alarm_time = datetime(year=now.year, month=now.month, day=now.day, hour=alarm.time.hour,
                              minute=alarm.time.minute)

        # If alarm time is greater than current time, then the alarm is today
        if alarm.time > now.time():
            print('alarm.time is {0} and it is currently {1}, so the alarm is today'.format(alarm.time, now.time()))
            return alarm_time

        # Otherwise, it's tomorrow
        else:
            print('alarm.time is {0} and it is currently {1}, so the alarm is tomorrow'.format(alarm.time, now.time()))
            return alarm_time + timedelta(days=1)

    # If the the alarm IS repeated, then the alarm is day dependent
    # Multiple alarms may be produced
    else:

        # Returns the next weekday that an alarm is scheduled
        def _next_weekday(weekday: int) -> datetime:
            days_ahead = weekday - now.weekday()
            if days_ahead == 0 and now.time() > alarm.time:  # Target day is today, but time has already passed
                days_ahead += 7
            if days_ahead < 0:  # Target day has already happened this week
                days_ahead += 7
            return datetime(year=now.year, month=now.month, day=now.day, hour=alarm.time.hour,
                            minute=alarm.time.minute) + timedelta(days_ahead)

        alarm_datetimes = []

        if alarm.repeat_sunday:
            alarm_datetimes.append(_next_weekday(6))
        if alarm.repeat_monday:
            alarm_datetimes.append(_next_weekday(0))
        if alarm.repeat_tuesday:
            alarm_datetimes.append(_next_weekday(1))
        if alarm.repeat_wednesday:
            alarm_datetimes.append(_next_weekday(2))
        if alarm.repeat_thursday:
            alarm_datetimes.append(_next_weekday(3))
        if alarm.repeat_friday:
            alarm_datetimes.append(_next_weekday(4))
        if alarm.repeat_saturday:
            alarm_datetimes.append(_next_weekday(5))

        # Return the first datetime as the alarm time
        return min(alarm_datetimes)


# Returns the next alarm by querying from the database and sorting by time
def get_next_alarm(now: datetime) -> Alarm:
    # Query all alarms
    alarms = Session().query(Alarm).filter_by(enabled=True).all()

    # Select and sort all alarms within the next 24 hours
    dts = list(map(lambda alarm: alarm_to_datetime(alarm, now), alarms))

    return alarms[dts.index(min(dts))] if len(alarms) > 0 else None


if __name__ == '__main__':
    sonos = SonosController(10, '192.168.0.109')
    hue = HueController(10, '192.168.0.59')

    current_date = datetime.now().replace(microsecond=0)

    next_alarm = get_next_alarm(current_date)
    next_alarm_dt = alarm_to_datetime(next_alarm, current_date)

    while True:
        try:
            current_date = datetime.now().replace(microsecond=0)
            # todo: Check incoming messages from Redis or something here

            if next_alarm is not None:

                # Seconds remaining until next alarm
                time_until_next_alarm = (next_alarm_dt - current_date).total_seconds()

                if time_until_next_alarm <= 0:
                    print('Wake up!')
                    next_alarm = get_next_alarm(current_date)
                    next_alarm_dt = alarm_to_datetime(next_alarm, current_date)
                    continue

                print('next alarm <', next_alarm.label, '> is in ', time_until_next_alarm, ' seconds')

                # Kick off controllers!
                if time_until_next_alarm <= hue.duration and not hue.is_active():
                    hue.start()

                if time_until_next_alarm <= sonos.duration and not sonos.is_active():
                    sonos.start()

            else:
                print('no upcoming alarms')

            sleep(1)

        except KeyboardInterrupt:
            sonos.stop()
            hue.stop()
            quit()
