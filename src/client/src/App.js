import React from 'react';

import Connection from './connection';

import { NavBar } from './components/NavBar';
import { MediaCapturer } from './components/media-capturer/MediaCapturer';
import { Status } from './components/Status';

class App extends React.Component {
    state = {
        statusMessage: null,
        messageLevel: 'info',
        statusOpen: false,
    }

    componentDidMount() {
        const displayErr = (error) => {
            this._changeStatusMessage('Unable to establish connection to server.', 'error');
            console.error('Unable to establish connection to server.', error);
        }
    
        Connection.get('/ping')
            .then(res => {
                res === 'pong' ?
                    this._changeStatusMessage('Connection to server established!') :
                    displayErr(res);
            })
            .catch(displayErr);
    }

    _changeStatusMessage = (statusMessage, messageLevel = 'info') => {
        this.setState({ statusMessage, messageLevel, statusOpen: true });
    }

    _closeStatusMessage = () => { this.setState({ statusOpen: false }) }

    render() {
        return (
            <React.Fragment>
                <NavBar />
                <Status
                    statusMessage={this.state.statusMessage}
                    messageLevel={this.state.messageLevel}
                    statusOpen={this.state.statusOpen}
                    closeStatusMessage={this._closeStatusMessage}
                />
                <MediaCapturer changeStatusMessage={this._changeStatusMessage} />
            </React.Fragment>
        );
    }

}

export default App;
