from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from db.models import Alarm
from db import Session


class BaseSchema(SQLAlchemyAutoSchema):
    class Meta:
        sqla_session = Session


class AlarmSchema(BaseSchema):
    class Meta(BaseSchema.Meta):
        model = Alarm
