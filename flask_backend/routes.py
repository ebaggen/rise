from db.models import Alarm
from db.schemas import AlarmSchema
from .forms import AlarmEditForm
from flask import render_template, redirect, request
from flask import current_app as app
from flask_backend import session
from time import time
from marshmallow import ValidationError
import datetime


@app.route('/api/alarms', methods=['GET'])
def get_alarms():
    alarms = session.query(Alarm).all()
    return {'alarms': AlarmSchema().dump(alarms, many=True)}


@app.route('/api/alarms', methods=['POST'])
def add_alarm():
    json_data = request.get_json()
    data = json_data['alarm']
    if not data:
        return {"message": "No input data provided"}, 400
    alarm = Alarm(
        time=datetime.datetime.strptime(data['time'], '%H:%M').time(),
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
    session.add(alarm)
    session.commit()
    return {'test': 'test'}


@app.route('/api/alarm/<id>', methods=['DELETE'])
def delete_alarm(id):
    session.query(Alarm).filter_by(id=id).delete()
    result = session.commit()
    return {'result': result}


@app.route('/api/alarm/<id>', methods=['PUT'])
def update_alarm(id):
    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400

    alarm = session.query(Alarm).filter_by(id=id).first()
    alarm.time = datetime.datetime.strptime(data['time'], '%H:%M').time()
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

    result = session.commit()
    return {'result': result}
