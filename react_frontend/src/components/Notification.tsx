import * as React from 'react';
import { NotificationSeverity} from "../enums/notificationSeverity";
import Snackbar from '@material-ui/core/Snackbar';
import MuiAlert, { AlertProps } from '@material-ui/lab/Alert';

export interface NotificationProps {
    message: string,
    severity: NotificationSeverity,
    open: boolean,
    handleClose: () => void
};

function Alert(props: AlertProps) {
    return <MuiAlert elevation={6} variant="filled" {...props} />;
}

export function Notification({message, severity, open, handleClose}: NotificationProps) {
    let alert = undefined;
    switch (severity) {
        case NotificationSeverity.Info:
            alert = (
                <Alert onClose={handleClose} severity="info">
                    {message}
                </Alert>
            );
            break;
        case NotificationSeverity.Error:
            alert = (
                <Alert onClose={handleClose} severity="error">
                    {message}
                </Alert>
            );
            break;
        case NotificationSeverity.Success:
            alert = (
                <Alert onClose={handleClose} severity="success">
                    {message}
                </Alert>
            );
            break;
        case NotificationSeverity.Warning:
            alert = (
                <Alert onClose={handleClose} severity="warning">
                    {message}
                </Alert>
            );
            break;
    }
    return (
        <Snackbar
            open={open}
            autoHideDuration={6000}
            onClose={(event?, reason?) => {
                if (reason !== 'clickaway'){
                    handleClose();
                }
            }}
        >
            {alert}
        </Snackbar>
    );
}