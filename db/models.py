from sqlalchemy import Column, Integer, String, Boolean, Time
from db import Base

class Alarm(Base):
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

    def as_dict(self):
        return {
            'id'
        }
