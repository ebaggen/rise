from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TimeField, SubmitField


class AlarmEditForm(FlaskForm):
    time = TimeField('Time', format='%H:%M:%S')
    label = StringField('Label')
    enabled = BooleanField('Enabled')
    repeat = BooleanField('Repeat')
    sunday_repeat = BooleanField('Sunday')
    monday_repeat = BooleanField('Monday')
    tuesday_repeat = BooleanField('Tuesday')
    wednesday_repeat = BooleanField('Wednesday')
    thursday_repeat = BooleanField('Thursday')
    friday_repeat = BooleanField('Friday')
    saturday_repeat = BooleanField('Saturday')
    submit = SubmitField('Submit')
