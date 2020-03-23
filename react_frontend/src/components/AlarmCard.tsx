import * as React from 'react';
import Alarm from '../types/alarm';
import Switch from '@material-ui/core/Switch';
import moment from 'moment'


export interface AlarmCardProps {
    alarm: Alarm,
    onClick: () => void
}

function AlarmCard({alarm, onClick}: AlarmCardProps) {
    const handleChange = () => {
        if (alarm.enabled) {
            const date = new Date();
            alert('Alarm set for ' + date + ' from now.');
        }
    }

    return (
        <div onClick={onClick}>
            {moment(alarm.time, 'H:mm:ss').format('h:mm a')}
            <Switch
                checked={alarm.enabled}
                onChange={handleChange}
            />
            <br/>
            {alarm.label}
        </div>
    );
}

export default AlarmCard;