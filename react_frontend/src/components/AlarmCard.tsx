import * as React from 'react';
import Alarm from '../types/alarm';
import Switch from '@material-ui/core/Switch';


export interface AlarmCardProps {
    alarm: Alarm,
    onClick: () => void
}

function AlarmCard({alarm, onClick}: AlarmCardProps) {
    const handleChange = () => {

    }

    return (
        <div onClick={onClick}>
            {alarm.time.format('h:mm A')}
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