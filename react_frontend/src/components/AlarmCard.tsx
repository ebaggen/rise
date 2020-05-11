import * as React from 'react';
import Alarm from '../types/alarm';
import {Switch} from 'antd';
import '../App.css'


export interface AlarmCardProps {
    alarm: Alarm,
    onClick: () => void
}

function AlarmCard({alarm, onClick}: AlarmCardProps) {
    const handleChange = () => {

    }

    return (
        <div onClick={onClick} className="Alarm-card">
            <div className="Alarm-card-top">
                {alarm.time.format('h:mm A')}
                <Switch
                    checked={alarm.enabled}
                    onChange={handleChange}
                />
            </div>
            {alarm.label}
        </div>
    );
}

export default AlarmCard;