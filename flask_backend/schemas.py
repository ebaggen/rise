from flask_backend.models import Alarm
from flask_backend import ma


class AlarmSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Alarm


alarm_schema = AlarmSchema()
alarms_schema = AlarmSchema(many=True)
