import * as React from 'react';
import Alarm from '../types/alarm';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import {TextField, Switch, FormControlLabel, FormGroup, Checkbox} from '@material-ui/core'
import {Formik, Form} from "formik";
import { createAlarm, updateAlarm } from '../api/alarm'

export interface AlarmPopupProps {
    alarm: Alarm | null,
    showModal: boolean,
    close: () => void
}

function AlarmModal({alarm, showModal, close}: AlarmPopupProps) {
    const initialAlarm = alarm ? alarm : {
        time: new Date(),
        label: '',
        enabled: true,
        repeat: false,
        repeat_sunday: false,
        repeat_monday: false,
        repeat_tuesday: false,
        repeat_wednesday: false,
        repeat_thursday: false,
        repeat_friday: false,
        repeat_saturday: false
    };


    const onSubmit = (alarm: Alarm) => {
        if (alarm.id) {
            updateAlarm(alarm)
                .then(() => close())
        } else {
            createAlarm(alarm)
                .then(() => close())
        }

    }

    return (
        <>
            <Modal show={showModal}>
                <Modal.Header>
                    <Modal.Title>{alarm ? 'Edit Alarm' : 'New Alarm'}</Modal.Title>
                </Modal.Header>
                <Modal.Body>

                    <Formik initialValues={{alarm: initialAlarm}} onSubmit={(values) => onSubmit(values.alarm)}>
                        {({values, handleChange, handleBlur}) => (

                            <Form>
                                <div>
                                    <TextField
                                        label="time"
                                        name='alarm.time'
                                        type='time'
                                        value={values.alarm.time}
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                        InputLabelProps={{
                                            shrink: true,
                                        }}
                                        inputProps={{
                                            step: 300, // 5 min
                                        }}
                                    />
                                </div>
                                <div>
                                    <TextField
                                        label="Label"
                                        name='alarm.label'
                                        value={values.alarm.label}
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                    />
                                </div>
                                <div>
                                    <FormControlLabel
                                        control={
                                            <Switch
                                                name="alarm.enabled"
                                                color="primary"
                                                checked={values.alarm.enabled}
                                                onChange={handleChange}
                                                onBlur={handleBlur}
                                            />
                                        }
                                        label="Enabled"
                                    />
                                </div>
                                <div>
                                    <FormControlLabel
                                        control={
                                            <Switch
                                                name="alarm.repeat"
                                                color="primary"
                                                checked={values.alarm.repeat}
                                                onChange={handleChange}
                                                onBlur={handleBlur}
                                            />
                                        }
                                        label="Repeat"
                                    />
                                </div>
                                {values.alarm.repeat && (
                                    <div>
                                        <FormGroup aria-label="position" row>
                                            <FormControlLabel
                                                checked={values.alarm.repeat_sunday}
                                                control={<Checkbox color="primary"/>}
                                                label="Sunday"
                                                name='alarm.repeat_sunday'
                                                labelPlacement="bottom"
                                                onChange={handleChange}
                                                onBlur={handleBlur}
                                            />
                                            <FormControlLabel
                                                checked={values.alarm.repeat_monday}
                                                control={<Checkbox color="primary"/>}
                                                label="Monday"
                                                name='alarm.repeat_monday'
                                                labelPlacement="bottom"
                                                onChange={handleChange}
                                                onBlur={handleBlur}
                                            />
                                            <FormControlLabel
                                                checked={values.alarm.repeat_tuesday}
                                                control={<Checkbox color="primary"/>}
                                                label="Tuesday"
                                                name='alarm.repeat_tuesday'
                                                labelPlacement="bottom"
                                                onChange={handleChange}
                                                onBlur={handleBlur}
                                            />
                                            <FormControlLabel
                                                checked={values.alarm.repeat_wednesday}
                                                control={<Checkbox color="primary"/>}
                                                label="Wednesday"
                                                name='alarm.repeat_wednesday'
                                                labelPlacement="bottom"
                                                onChange={handleChange}
                                                onBlur={handleBlur}
                                            />
                                            <FormControlLabel
                                                checked={values.alarm.repeat_thursday}
                                                control={<Checkbox color="primary"/>}
                                                label="Thursday"
                                                name='alarm.repeat_thursday'
                                                labelPlacement="bottom"
                                                onChange={handleChange}
                                                onBlur={handleBlur}
                                            />
                                            <FormControlLabel
                                                checked={values.alarm.repeat_friday}
                                                control={<Checkbox color="primary"/>}
                                                label="Friday"
                                                name='alarm.repeat_friday'
                                                labelPlacement="bottom"
                                                onChange={handleChange}
                                                onBlur={handleBlur}
                                            />
                                            <FormControlLabel
                                                checked={values.alarm.repeat_saturday}
                                                control={<Checkbox color="primary"/>}
                                                label="Saturday"
                                                name='alarm.repeat_saturday'
                                                labelPlacement="bottom"
                                                onChange={handleChange}
                                                onBlur={handleBlur}
                                            />
                                        </FormGroup>
                                    </div>
                                )}
                                <Button variant="secondary" onClick={close}>
                                    Close
                                </Button>
                                <Button variant='primary' type='submit'>
                                    Save Changes
                                </Button>
                            </Form>
                        )}
                    </Formik>

                </Modal.Body>
            </Modal>
        </>
    );
}

export default AlarmModal;