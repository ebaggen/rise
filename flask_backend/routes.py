from db.models import Alarm
from db.schemas import AlarmSchema
from .forms import AlarmEditForm
from flask import render_template, redirect, request
from flask import current_app as app
from flask_backend import db
from time import time
from marshmallow import ValidationError


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


@app.route('/api/alarms', methods=['GET'])
def get_alarms():
    alarms = db.session.query(Alarm).all()
    return {'alarms': AlarmSchema().dump(alarms, many=True)}


@app.route('/api/alarms', methods=['POST'])
def add_alarm():
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400
    try:
        data = AlarmSchema().load(json_data)
    except ValidationError as err:
        return err.messages, 422
    alarm = Alarm(
        time=data['time'],
        label=data['label'],
        enabled=data['enabled'],
        repeat=data['repeat'],
        repeat_sunday=data['repeat_sunday'],
        repeat_monday=data['repeat_monday'],
        repeat_tuesday=data['repeat_tuesday'],
        repeat_wednesday=data['repeat_wednesday'],
        repeat_thursday=data['repeat_thursday'],
        repeat_friday=data['repeat_friday'],
        repeat_saturday=data['repeat_saturday']
    )
    db.session.add(alarm)
    db.session.commit()
    return {'test': 'test'}


@app.route('/api/alarm/<id>', methods=['DELETE'])
def delete_alarm(id):
    db.session.query(Alarm).filter_by(id=id).delete()
    result = db.session.commit()
    return {'result': result}


@app.route('/api/alarm/<id>', methods=['PUT'])
def update_alarm(id):
    json_data = request.get_json()
    if not json_data:
        return {"message": "No input data provided"}, 400

    try:
        data = AlarmSchema().load(json_data)
    except ValidationError as err:
        return err.messages, 422

    alarm = db.session.query(Alarm).filter_by(id=id).first()
    alarm.time = data['time']
    alarm.label = data['label']
    alarm.enabled = data['enabled']
    alarm.repeat = data['repeat']
    alarm.repeat_sunday = data['repeat_sunday']
    alarm.repeat_monday = data['repeat_monday']
    alarm.repeat_tuesday = data['repeat_tuesday']
    alarm.repeat_wednesday = data['repeat_wednesday']
    alarm.repeat_thursday = data['repeat_thursday']
    alarm.repeat_friday = data['repeat_friday']
    alarm.repeat_saturday = data['repeat_saturday']

    result = db.session.commit()
    return {'result': result}
