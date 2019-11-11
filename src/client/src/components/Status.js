import React from 'react';

import Connection from '../connection';

import './Status.css';

const MESSAGES = {
    CONNECTED: 'Connection to server established!',
    UNABLE_TO_CONNECT: 'WARNING: Unable to establish connection to server'
}

class Status extends React.Component {
    state = {
        serverStatus: null
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

        const color = this.state.serverStatus === MESSAGES.CONNECTED ?
            'green' :
            'red';

        const icon = this.state.serverStatus === MESSAGES.CONNECTED ?
            'check' :
            'times';

        return (
            <div className='status' style={{ color }}>
                <i className={`fa fa-${icon}`}></i>
                <p>{this.state.serverStatus}</p>
            </div>
        );
    }
}

export { Status as default, Status };
