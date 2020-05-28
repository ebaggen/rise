from sqlalchemy import Column, Integer, String, Boolean, Time
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Alarm(db.Model):
    __tablename__ = 'alarms'

    id = Column(Integer, primary_key=True)
    label = Column(String(128))
    time = Column(Time)
    enabled = Column(Boolean)
    active = Column(Boolean)
    repeat = Column(Boolean)
    repeat_sunday = Column(Boolean)
    repeat_monday = Column(Boolean)
    repeat_tuesday = Column(Boolean)
    repeat_wednesday = Column(Boolean)
    repeat_thursday = Column(Boolean)
    repeat_friday = Column(Boolean)
    repeat_saturday = Column(Boolean)

    def __repr__(self):
        return '<Alarm @ {0} ({1})>'.format(self.time, self.label)

    # Converts an Alarm object to a datetime nearest now (in UTC!!)
    def next_occurrence(self) -> datetime:

        if not self.enabled:
            return datetime.max

        now = datetime.utcnow()

        # If alarm is NOT repeated, then the alarm is scheduled for its time within the next 24 hours
        if not self.repeat:

            alarm_time = datetime(year=now.year, month=now.month, day=now.day, hour=self.time.hour,
                                  minute=self.time.minute, second=self.time.second)

            # If alarm time is greater than current time, then the alarm is today
            if self.time > now.time():
                return alarm_time

            # Otherwise, it's tomorrow
            else:
                return alarm_time + timedelta(days=1)

        # If the the alarm IS repeated, then the alarm is day dependent
        # Multiple alarms may be produced
        else:

            # Returns the next weekday that an alarm is scheduled
            def _next_weekday(weekday: int) -> datetime:
                days_ahead = weekday - now.weekday()
                if days_ahead == 0 and now.time() > self.time:  # Target day is today, but time has already passed
                    days_ahead += 7
                if days_ahead < 0:  # Target day has already happened this week
                    days_ahead += 7
                return datetime(year=now.year, month=now.month, day=now.day, hour=self.time.hour,
                                minute=self.time.minute) + timedelta(days_ahead)

            schedule = [
                self.repeat_sunday, self.repeat_monday, self.repeat_tuesday,
                self.repeat_wednesday, self.repeat_thursday, self.repeat_friday, self.repeat_saturday
            ]

            # Return the first datetime as the alarm time
            return min([_next_weekday(day) for day, repeat in enumerate(schedule) if repeat])
