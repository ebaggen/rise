import React, {useEffect, useState} from 'react';
import './App.css';
import AlarmCard from './components/AlarmCard';
import AlarmModal from './components/AlarmModal';
import Fab from '@material-ui/core/Fab'
import AddIcon from '@material-ui/icons/Add';
import {fetchAlarms} from './api/alarm'
import Alarm from "./types/alarm";
import {Notification} from "./components/Notification";
import {NotificationSeverity} from "./enums/notificationSeverity";
import moment from 'react-moment'


function App() {

    const [alarms, setAlarms] = useState([]);
    const [showModal, setShowModal] = useState({
        alarm: null,
        show: false
    });
    const [notification, setNotification] = useState({
        message: '',
        severity: NotificationSeverity.Info,
        open: false,
        }
    )

    useEffect(() => {
        refreshState();
    }, []);

    const refreshState = () => {
        fetchAlarms()
            .then(alarms => {
                alarms.sort((a: Alarm, b: Alarm) => a.time < b.time ? -1 : 1);
                setAlarms(alarms);
            });
    }

    return (
        <div className="App">
            <body className="App-body">
                <Notification
                    message={notification.message}
                    severity={notification.severity}
                    open={notification.open}
                    handleClose={() => setNotification({...notification, open: false})}
                />
                <AlarmModal
                    alarm={showModal.alarm}
                    showModal={showModal.show}
                    close={() => {
                        setShowModal({
                            alarm: null,
                            show: false
                        });
                        refreshState();
                    }}
                />
                <p>
                    {alarms.map(alarm =>
                        <div>
                            <AlarmCard alarm={alarm} onClick={() => {
                                setShowModal({
                                    alarm: alarm,
                                    show: true
                                });
                            }}/>
                            <hr/>
                        </div>
                        )
                    }
                </p>
                <Fab color="primary" aria-label="add" onClick={() => setShowModal({
                    alarm: null,
                    show: true
                })}>
                    <AddIcon/>
                </Fab>
            </body>
        </div>
  );
}

export default App;
