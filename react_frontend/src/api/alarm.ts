import Alarm from '../types/alarm'

export function fetchAlarms() {
    return fetch('/api/alarms')
            .then(res => res.json())
            .then(data => {
                return data.alarms;
        });
}

export function createAlarm(alarm: Alarm) {
    return fetch('/api/alarms', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ alarm })
    });
}

export function updateAlarm(alarm: Alarm) {
    return fetch('/api/alarm/' + alarm.id, {
        method: 'PUT',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(alarm)
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