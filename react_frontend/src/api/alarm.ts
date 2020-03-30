import Alarm from '../types/alarm';
import moment from 'moment';
import alarm from "../types/alarm";

export function fetchAlarms() {
    return fetch('/api/alarms')
            .then(res => res.json())
            .then(data => {
                return data.alarms.map((alarm: Alarm) => ({
                    ...alarm,
                    time: moment.utc(alarm.time, 'H:mm:ss').local().format('H:mm')
                }));
        });
}

export function createAlarm(alarm: Alarm) {
    return fetch('/api/alarms', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({...alarm, time: moment(alarm.time, 'H:mm').utc().format('H:mm:ss') })
    });
}

export function updateAlarm(alarm: Alarm) {
    return fetch('/api/alarm/' + alarm.id, {
        method: 'PUT',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({...alarm, time: moment(alarm.time, 'H:mm').utc().format('H:mm:ss') })
    });
}

export function deleteAlarm(alarmId: number) {
    return fetch('/api/alarm/' + alarmId, {
        method: 'DELETE',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    });
}