import * as React from 'react';
import Alarm from '../types/alarm';
import {
    Form,
    TimePicker,
    Input,
    Switch,
    Checkbox,
    Row,
    Col,
    Modal, Popconfirm
} from 'antd';
import moment from 'moment'
import {useState} from "react";
import {IconButton} from "@material-ui/core";
import DeleteIcon from "@material-ui/icons/Delete";
import {createAlarm, deleteAlarm, updateAlarm} from "../api/alarm";

export interface AlarmFormProps {
    alarm: Alarm | null,
    show: boolean,
    onClose: () => void
}

export default function AlarmForm({alarm, show, onClose}: AlarmFormProps) {
    const initialAlarm = alarm ? alarm : {
        time: moment(),
        label: '',
        enabled: true,
        repeat: true,
        repeat_sunday: true,
        repeat_monday: true,
        repeat_tuesday: true,
        repeat_wednesday: true,
        repeat_thursday: true,
        repeat_friday: true,
        repeat_saturday: true
    };

    const onSubmit = (alarm: Alarm) => {
        if (alarm.id) {
            updateAlarm(alarm)
                .then(onClose)
        } else {
            createAlarm(alarm)
                .then(onClose)
        }
    };

    const onConfirmDelete = (alarmId?: number) => {
        if (alarmId) {
            deleteAlarm(alarmId)
                .then(onClose)
        }

    };

    const [showDays, setShowDays] = useState(initialAlarm.repeat);
    const [form] = Form.useForm();

    const onFinish = (values: any) => {
        onSubmit({
            time: values.time,
            label: values.label,
            enabled: values.enabled,
            repeat: values.repeat,
            repeat_sunday: values.repeat_sunday,
            repeat_monday: values.repeat_monday,
            repeat_tuesday: values.repeat_tuesday,
            repeat_wednesday: values.repeat_wednesday,
            repeat_thursday: values.repeat_thursday,
            repeat_friday: values.repeat_friday,
            repeat_saturday: values.repeat_saturday
        });
    };

    return (
        <Modal
            visible={show}
            title={alarm ? 'Edit Alarm' : 'New Alarm'}
            okText={alarm ? 'Update' : 'Add'}
            onCancel={onClose}
            onOk={() => {
                form.validateFields()
                    .then((values) => {
                        form.resetFields();
                        console.log(values as Alarm);
                        onClose();
                        /*
                        if (alarm.id) {
                            updateAlarm(alarm)
                                .then(onClose)
                        } else {
                            createAlarm(alarm)
                                .then(onClose)
                        }
                        */

                    })
            }}
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
            <Form
                form={form}
                initialValues={initialAlarm}
                onFinish={onFinish}
            >
                <Form.Item
                    label='Time'
                    name='time'
                    rules={[{required: true, message: 'Alarm time required!'}]}
                >
                    <TimePicker use12Hours format='h:mm A'/>
                </Form.Item>
                <Form.Item label='Label' name='label'>
                    <Input/>
                </Form.Item>
                <Form.Item label='Enabled' name='enabled' valuePropName="checked">
                    <Switch/>
                </Form.Item>
                <Form.Item label='Repeat' name='repeat'>
                    <Checkbox onChange={(e) => setShowDays(e.target.checked)}/>
                </Form.Item>
                {showDays &&
                    <Form.Item name='days'>
                        <Checkbox.Group>
                            <Row>
                                <Col>
                                    <Checkbox name='repeat_sunday' value='repeat_sunday'>Sunday</Checkbox>
                                </Col>
                                <Col>
                                    <Checkbox name='repeat_monday' value='repeat_monday'>Monday</Checkbox>
                                </Col>
                                <Col>
                                    <Checkbox name='repeat_tuesday' value='repeat_tuesday'>Tuesday</Checkbox>
                                </Col>
                                <Col>
                                    <Checkbox name='repeat_wednesday' value='repeat_wednesday'>Wednesday</Checkbox>
                                </Col>
                                <Col>
                                    <Checkbox name='repeat_thursday' value='repeat_thursday'>Thursday</Checkbox>
                                </Col>
                                <Col>
                                    <Checkbox name='repeat_friday' value='repeat_friday'>Friday</Checkbox>
                                </Col>
                                <Col>
                                    <Checkbox name='repeat_saturday' value='repeat_saturday'>Saturday</Checkbox>
                                </Col>
                            </Row>
                        </Checkbox.Group>
                    </Form.Item>
                }
            </Form>
        </Modal>
    );
}