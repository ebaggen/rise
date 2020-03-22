from db.models import Alarm
from db.schemas import AlarmSchema
from .forms import AlarmEditForm
from flask import render_template, redirect, request
from flask import current_app as app
from flask_backend import db, alarm_schema
from time import time


@app.route('/')
def index():
    alarms = db.session.query(Alarm).order_by(Alarm.time.asc()).all()
    return render_template('index.html', alarms=alarms, form=AlarmEditForm())


@app.route('/new_alarm', methods=['GET', 'POST'])
def new_alarm():
    form = AlarmEditForm()
    if form.is_submitted():
        alarm = Alarm(
            time=form.time.data,
            label=form.label.data,
            enabled=form.enabled.data,
            repeat=form.repeat.data,
            repeat_sunday= False, # form.sunday_repeat.data,
            repeat_monday= False, # form.monday_repeat.data,
            repeat_tuesday=False, # form.tuesday_repeat.data,
            repeat_wednesday=False, # form.wednesday_repeat.data,
            repeat_thursday=False, # form.thursday_repeat.data,
            repeat_friday=False, # form.friday_repeat.data,
            repeat_saturday=False # form.saturday_repeat.data,
        )
        db.session.add(alarm)
        db.session.commit()
        return redirect('/')
    return render_template('edit_alarm.html', form=form)


@app.route('/delete_alarm')
def delete_alarm():
    id = request.form['id']
    alarm_to_delete = Alarm.query.get(id)
    db.session.delete(alarm_to_delete)
    db.session.commit()


@app.route('/api')
def api():
    return {'time': time()}


@app.route('/api/alarms')
def get_alarms():
    alarms = db.session.query(Alarm).order_by(Alarm.time.asc()).all()
    return {'alarms': alarm_schema.dump(alarms, many=True)}
