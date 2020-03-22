import * as React from 'react';
import Alarm from '../types/alarm';
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'
import { TextField, Switch, FormControlLabel } from '@material-ui/core'
import { KeyboardTimePicker } from '@material-ui/pickers/';

export interface AlarmPopupProps {
    initialAlarm: Alarm | null,
    showModal: boolean,
    close: () => void
};

function AlarmModal({initialAlarm, showModal, close}: AlarmPopupProps) {

    return (
        <>
          <Modal show={showModal}>
              <Modal.Header>
                  <Modal.Title>{initialAlarm ? 'Edit Alarm' : 'New Alarm'}</Modal.Title>
              </Modal.Header>
              <Modal.Body>
                  <form>
                      <TextField label="Label"/>
                      <FormControlLabel
                          control={
                              <Switch
                                  name="checked"
                                  color="primary"
                              />
                          }
                          label="Enabled"
                      />
                  </form>
              </Modal.Body>
              <Modal.Footer>
                  <Button variant="secondary" onClick={close}>
                      Close
                  </Button>
                  <Button variant='primary'>
                      Save Changes
                  </Button>
              </Modal.Footer>
          </Modal>
      </>
  );
}

export default AlarmModal;