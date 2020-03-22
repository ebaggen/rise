import React, {useEffect, useState} from 'react';
import './App.css';
import AlarmCard from './components/AlarmCard';
import AlarmModal from './components/AlarmModal';
import Fab from '@material-ui/core/Fab'
import AddIcon from '@material-ui/icons/Add';
import Alarm from './types/alarm'



function App() {

    const [alarms, setAlarms] = useState([]);
    const [showModal, setShowModal] = useState({
        alarm: null,
        show: false
    });

    useEffect(() => {
        fetch('/api/alarms')
            .then(res => res.json())
            .then(data => {
                setAlarms(data.alarms);
        });
    }, []);

    return (
        <div className="App">
            <body className="App-body">
                <AlarmModal
                    initialAlarm={showModal.alarm}
                    showModal={showModal.show}
                    close={() => {
                        setShowModal({
                            alarm: null,
                            show: false
                        })
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
