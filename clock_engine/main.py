from threading import Thread
from soco import SoCo
from time import sleep, time
from phue import Bridge
from db import Session
from db.models import Alarm
from datetime import datetime, timedelta
from enum import Enum


class HueController:
    def __init__(self, duration):
        self._duration = duration

        self._thread = Thread()

        # Initialize Hue connection
        self._bridge = Bridge('192.168.0.59')
        self._lights = self._bridge.lights

        self._cancellation_token = False

    def start(self):
        if not self._thread.is_alive():
            self._thread = Thread(target=self.__loop, args=(lambda: self._cancellation_token,))
            self._thread.start()
        else:
            raise Exception('Thread already exists.')

    def stop(self):
        if self._thread.is_alive():
            self._cancellation_token = True
            self._thread.join()
            self._cancellation_token = False

    def __loop(self, cancellation_token):
        for light in self._lights:
            light.brightness = 0
            light.on = False

        # Test parameters
        # todo: make this config data
        ending_brightness = 100
        step_time = 1
        elapsed_time = 0

        while elapsed_time < self._duration and not cancellation_token():
            percent_complete = elapsed_time / self._duration * 100
            brightness_percent = percent_complete / 100 * ending_brightness
            brightness = max(min(int(brightness_percent / 100 * 254), 254), 1)
            for light in self._lights:
                light.on = True
                light.brightness = brightness
                print('{0} brightness is at {1}'.format(light.name, light.brightness))

                # todo: implement color changing functionality

            sleep(step_time)
            elapsed_time += step_time


class SonosController:
    def __init__(self, duration):
        self._duration = duration

        self._thread = Thread()
        self._cancellation_token = False

        # Initialize sonos speaker connection
        # todo: make this config data
        self._sonos = SoCo('192.168.0.109')

    def start(self):
        if not self._thread.is_alive():
            self._thread = Thread(target=self.__loop, args=(lambda: self._cancellation_token,))
            self._thread.start()
        else:
            raise Exception('Thread already exists.')

    def stop(self):
        if self._thread.is_alive():
            self._cancellation_token = True
            self._thread.join()
            self._cancellation_token = False

    def __loop(self, cancellation_token):
        # todo: select station/track info to play
        self._sonos.volume = 0

        # Test parameters
        # todo: make this config data
        ending_volume = 40
        step_time = 1
        elapsed_time = 0

        # Start playing
        self._sonos.play()

        # Increment volume for duration of alarm
        while elapsed_time < self._duration and not cancellation_token():
            self._sonos.volume += max(min(int(elapsed_time / 100 * ending_volume), 100), 1)
            sleep(step_time)
            elapsed_time += step_time
            print('sonos volume is at {0}'.format(self._sonos.volume))


class Day(Enum):
    SUNDAY = 7
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6


# Returns true if the alarm is during the remaining hours of today, enabled, and
def is_alarm_today(alarm, date):
    return alarm.time > date.time() and alarm.enabled and (alarm.repeat is False or (
            alarm.repeat and (
            date.day == Day.SUNDAY and alarm.repeat_sunday)
    (date.day == Day.MONDAY and alarm.repeat_monday) or
            (date.day == Day.TUESDAY and alarm.repeat_tuesday) or
            (date.day == Day.WEDNESDAY and alarm.repeat_wednesday) or
            (date.day == Day.THURSDAY and alarm.repeat_thursday) or
            (date.day == Day.FRIDAY and alarm.repeat_friday) or
            (date.day == Day.SATURDAY and alarm.repeat_saturday) or
            (date.day == Day.SUNDAY and alarm.repeat_sunday)
    ))


def is_alarm_tomorrow(alarm, date):
    return alarm.time < date.time() and alarm.enabled and (alarm.repeat is False or (
            alarm.repeat and (
            date.day == 1 and alarm.repeat_tuesday) or
            (date.day == 2 and alarm.repeat_wednesday) or
            (date.day == 3 and alarm.repeat_thursday) or
            (date.day == 4 and alarm.repeat_friday) or
            (date.day == 5 and alarm.repeat_saturday) or
            (date.day == 6 and alarm.repeat_sunday) or
            (date.day == 7 and alarm.repeat_monday)
    ))


def alarms_to_datetimes(alarms, now):
    upcoming_alarms = []

    for alarm in alarms:
        if is_alarm_today(alarm, now):
            dt_alarm = now.replace(hour=alarm.time.hour, minute=alarm.time.minute, second=0, microsecond=0)
            upcoming_alarms.append(dt_alarm)
        elif is_alarm_tomorrow(alarm, now):
            dt_alarm = now.replace(hour=alarm.time.hour, minute=alarm.time.minute, second=0, microsecond=0)
            dt_alarm = dt_alarm + timedelta(days=1)
            upcoming_alarms.append(dt_alarm)

    upcoming_alarms.sort()

    return upcoming_alarms


if __name__ == '__main__':
    sonos = SonosController(10)
    hue = HueController(10)
    next_alarm = time() + 2
    controllers_active = False
    session = Session()

    while True:
        try:
            current_date = datetime.now().replace(microsecond=0)

            # Query all alarms
            alarms = session.query(Alarm).all()
            print(alarms)

            # Select and sort all alarms within the next 24 hours
            upcoming_alarms = alarms_to_datetimes(alarms, current_date)

            next_alarm = upcoming_alarms[0] if len(upcoming_alarms) > 0 else None

            if next_alarm is not None:

                # Seconds remaining until next alarm
                time_until_next_alarm = (next_alarm - current_date).total_seconds()


                # Kick off controllers!
                if time_until_next_alarm <= 10 and not controllers_active:
                    controllers_active = True
                    print('starting controllers!')
                    sonos.start()
                    hue.start()
                elif not controllers_active:
                    print('Time until next alarm: {0} seconds.'.format(time_until_next_alarm))

            sleep(1)

        except KeyboardInterrupt:
            sonos.stop()
            hue.stop()
            quit()
