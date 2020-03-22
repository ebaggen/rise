from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from db.models import Alarm


class AlarmSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Alarm
