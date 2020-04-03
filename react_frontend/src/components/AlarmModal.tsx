import * as React from 'react';
import Alarm from '../types/alarm';
import Button from 'react-bootstrap/Button';
import {TextField, Switch, FormControlLabel, FormGroup, Checkbox, IconButton,} from '@material-ui/core';
import DeleteIcon from '@material-ui/icons/Delete';
import { createAlarm, updateAlarm, deleteAlarm } from '../api/alarm';
import { AlarmForm } from './AlarmForm';
import { Popconfirm, Modal } from 'antd';


export interface AlarmModalProps {
    alarm: Alarm | null,
    showModal: boolean,
    close: () => void
}

function AlarmModal({alarm, showModal, close}: AlarmModalProps) {

    const onSubmit = (alarm: Alarm) => {
        if (alarm.id) {
            updateAlarm(alarm)
                .then(() => close())
        } else {
            createAlarm(alarm)
                .then(() => close())
        }
    };

    const onConfirmDelete = (alarmId?: number) => {
        if (alarmId) {
            deleteAlarm(alarmId)
                .then(() => close())
        }

    };

    return (
        <>
            <Modal
                visible={showModal}
                title={alarm ? 'Edit Alarm' : 'New Alarm'}
                onCancel={close}
            >
                {alarm &&
                    <Popconfirm
                        title='Are you sure you want to delete this alarm?'
                        onConfirm={() => onConfirmDelete(alarm.id)}
                    >
                        <IconButton aria-label="delete">
                            <DeleteIcon fontSize="large"/>
                        </IconButton>
                    </Popconfirm>
                }
                <AlarmForm alarm={alarm} onSubmit={onSubmit}/>
            </Modal>
        </>
    );
}

export default AlarmModal;