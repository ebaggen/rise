from typing import Dict, Any
from flask_backend.scheduler import schedule_alarm
from flask_backend.models import db, Alarm
from flask_backend.schemas import alarms_schema
from flask import request
from flask import current_app as app
import datetime


# Get all alarms
@app.route('/api/alarms', methods=['GET'])
def get_alarms():
    alarms = db.session.query(Alarm).all()
    return {'alarms': alarms_schema.dump(alarms)}


# Add a new alarm (no id)
@app.route('/api/alarms', methods=['POST'])
def add_alarm():
    json_data = request.get_json()
    data = json_data['alarm']
    if not data:
        return {"message": "No input data provided"}, 400
    alarm = Alarm(
        time=datetime.datetime.strptime(data['time'], '%H:%M:%S').time(),
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

    schedule_alarm()

    return {'test': 'test'}


# Delete alarm
@app.route('/api/alarm/<id>', methods=['DELETE'])
def delete_alarm(id: int) -> Dict[str, Any]:
    db.session.query(Alarm).filter_by(id=id).delete()
    result = db.session.commit()

    schedule_alarm()

    return {'result': result}


# Update alarm with <id>
@app.route('/api/alarm/<id>', methods=['PUT'])
def update_alarm(id):
    data = request.get_json()
    if not data:
        return {"message": "No input data provided"}, 400
    print(data)
    alarm = db.session.query(Alarm).filter_by(id=id).first_or_404()
    alarm.time = datetime.datetime.strptime(data['time'], '%H:%M:%S').time()
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

    schedule_alarm()

    return {'result': result}
