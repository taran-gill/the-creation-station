import React from 'react';

import { NavBar } from './components/NavBar';
import { MediaRecorder } from './components/MediaRecorder';

import Connection from './connection';

if (process.env.NODE_ENV === 'development') {
    const displayErr = (err) => {
        console.error('Unable to establish connection to server', err);
    }

    Connection.get('/ping')
        .then(res => {
            res === 'pong' ?
                console.log('Connection to server established!') :
                displayErr(res);
        })
        .catch(displayErr);
}

function App() {
    return (
        <React.Fragment>
            <NavBar />
            <MediaRecorder />
        </React.Fragment>
    );
}

export default App;
