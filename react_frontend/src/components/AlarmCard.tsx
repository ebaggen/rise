import * as React from 'react';
import Alarm from '../types/alarm';
import Switch from '@material-ui/core/Switch';
import moment, { Moment } from 'moment'


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
            {moment(alarm.time, 'H:mm').format('h:mm A')}
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