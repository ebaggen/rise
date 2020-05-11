import React, {useEffect, useState} from 'react';
import './App.css';
import AlarmCard from './components/AlarmCard';
import AlarmForm from './components/AlarmForm';
import Fab from '@material-ui/core/Fab'
import AddIcon from '@material-ui/icons/Add';
import {fetchAlarms} from './api/alarm'
import Alarm from "./types/alarm";
import {Notification} from "./components/Notification";
import {NotificationSeverity} from "./enums/notificationSeverity";


function App() {

    const [alarms, setAlarms] = useState<Alarm[]>([]);
    const [showModal, setShowModal] = useState<{ alarm: Alarm | null, show: boolean }>({
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
            .then((alarms) => {
                console.log(alarms)
                alarms.sort((a: Alarm, b: Alarm) => a.time.isBefore( b.time) ? -1 : 1)
                setAlarms(alarms);
            });
    }

    return (
        <div className="App">
            <header className="App-header">
                <h1>RISE</h1>
            </header>
            <body className="App-body">

                <Notification
                    message={notification.message}
                    severity={notification.severity}
                    open={notification.open}
                    handleClose={() => setNotification({...notification, open: false})}
                />
                <AlarmForm
                    alarm={showModal.alarm}
                    show={showModal.show}
                    onClose={() => {
                        setShowModal({
                            alarm: null,
                            show: false
                        });
                        refreshState();
                    }}
                />
                <div>
                    {alarms.map((alarm) =>
                        <div key={alarm.id}>
                            <AlarmCard alarm={alarm} onClick={() => {
                                setShowModal({
                                    alarm: alarm,
                                    show: true
                                });
                            }}/>
                        </div>
                        )
                    }
                </div>
            </body>
            <footer className="App-footer">
                <Fab className="app-fab--absolute" aria-label="add" onClick={() => setShowModal({
                    alarm: null,
                    show: true
                })}>
                    <AddIcon/>
                </Fab>
            </footer>
        </div>
  );
}

export default App;
