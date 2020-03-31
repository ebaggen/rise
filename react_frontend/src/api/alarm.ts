import Alarm from '../types/alarm';
import moment from 'moment';

export function fetchAlarms(): Promise<Alarm[]> {
    return fetch('/api/alarms')
            .then(res => {
                return res.json();
            })
            .then(data => {
                return data.alarms.map((alarm: Alarm) => ({
                    ...alarm,
                    time: moment.utc(alarm.time, 'H:mm').local()
                })) as Promise<Alarm[]>
            })
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