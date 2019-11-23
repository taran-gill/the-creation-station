import React from 'react';

import { NavBar } from './components/NavBar';
import { MediaCapturer } from './components/MediaCapturer';
import { Status } from './components/Status';

function App() {
    return (
        <React.Fragment>
            <NavBar />
            <Status />
            <MediaCapturer />
        </React.Fragment>
    );
}

export default App;
