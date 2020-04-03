import * as React from 'react';
import Alarm from '../types/alarm';
import {Form, TimePicker, Input, Switch, Checkbox, Row, Col} from 'antd';
import moment from 'moment'
import {useState} from "react";

export interface AlarmFormProps {
    alarm: Alarm | null,
    onSubmit: (alarm: Alarm) => void
}

export function AlarmForm({alarm, onSubmit }: AlarmFormProps) {
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



    const [showDays, setShowDays] = useState(initialAlarm.repeat)

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
      <Form
          initialValues={initialAlarm}
          onFinish={onFinish}
      >
          <Form.Item
              label='Time'
              name='time'
              rules={[{ required: true, message: 'Alarm time required!' }]}
          >
              <TimePicker use12Hours format='h:mm A'/>
          </Form.Item>
          <Form.Item label='Label' name='label'>
              <Input />
          </Form.Item>
          <Form.Item label='Enabled' name='enabled' valuePropName="checked">
              <Switch />
          </Form.Item>
          <Form.Item label='Repeat' name='repeat'>
              <Checkbox onChange={(e) => setShowDays(e.target.checked)}/>
          </Form.Item>
          { showDays &&
              <Form.Item>
                  <Checkbox.Group>
                      <Row>
                          <Col>
                              <Checkbox name='repeat_sunday' value='sunday'>Sunday</Checkbox>
                          </Col>
                          <Col>
                              <Checkbox name='repeat_monday' value='monday'>Monday</Checkbox>
                          </Col>
                          <Col>
                              <Checkbox name='repeat_tuesday' value='tuesday'>Tuesday</Checkbox>
                          </Col>
                          <Col>
                              <Checkbox name='repeat_wednesday' value='wednesday'>Wednesday</Checkbox>
                          </Col>
                          <Col>
                              <Checkbox name='repeat_thursday' value='thursday'>Thursday</Checkbox>
                          </Col>
                          <Col>
                              <Checkbox name='repeat_friday' value='friday'>Friday</Checkbox>
                          </Col>
                          <Col>
                              <Checkbox name='repeat_saturday' value='saturday'>Saturday</Checkbox>
                          </Col>
                      </Row>
                  </Checkbox.Group>
              </Form.Item>
          }
      </Form>
    );
}