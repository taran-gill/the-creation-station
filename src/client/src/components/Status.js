import React from 'react';
import { Snackbar } from '@rmwc/snackbar';

import Connection from '../connection';

import './Status.css';

const MESSAGES = {
    CONNECTED: 'Connection to server established!',
    UNABLE_TO_CONNECT: 'ERROR: Unable to establish connection to server'
}

class Status extends React.Component {
    state = {
        serverStatus: null,
        open: false
    }

    componentDidMount() {
        const displayErr = (error) => {
            this.setState({ serverStatus: MESSAGES.UNABLE_TO_CONNECT });
            console.error(MESSAGES.UNABLE_TO_CONNECT, error);
        }
    
        Connection.get('/ping')
            .then(res => {
                res === 'pong' ?
                    this.setState({ serverStatus: MESSAGES.CONNECTED }) :
                    displayErr(res);
            })
            .catch(displayErr);
    }

    render() {
        if (!this.state.serverStatus) return null;

        const snackbarClass = this.state.serverStatus === MESSAGES.CONNECTED ?
            'connected' :
            'error';

        return (
            <Snackbar
                open={!!this.state.serverStatus}
                onClose={evt => this.setState({ open: false })}
                message={this.state.serverStatus}
                dismissIcon
                timeout={10000}
                className={snackbarClass}
            />
        );
    }
}

export { Status as default, Status };
