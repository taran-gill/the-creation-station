import React from 'react';
import LoadingOverlay from 'react-loading-overlay';
import RingLoader from 'react-spinners/RingLoader';

import Connection from './connection';

import { NavBar } from './components/NavBar';
import { MediaCapturer } from './components/media-capturer/MediaCapturer';
import { Status } from './components/Status';

import './App.css';

class App extends React.Component {
    state = {
        statusMessage: null,
        messageLevel: 'info',
        statusOpen: false,
        loading: true,
        loadingMessage: 'Establishing connection to server'
    }

    componentDidMount() {
        setInterval(() => {
            if (this.state.loadingMessage.charAt(this.state.loadingMessage.length - 3) === '.') {
                this.setState({
                    loadingMessage: this.state.loadingMessage.substring(0, this.state.loadingMessage.length - 3)
                });
                return;
            }
            
            this.setState({
                loadingMessage: this.state.loadingMessage + '.'
            })
        }, 1000);

        const displayErr = (error) => {
            this._changeStatusMessage('Unable to establish connection to server.', 'error');
            console.error('Unable to establish connection to server.', error);
        }
    
        Connection.get('/ping')
            .then(res => {
                if (res !== 'pong') displayErr(res);
            })
            .catch(displayErr)
            .finally(() => {
                this._updateLoadingOverlay(false);
            })
    }

    _changeStatusMessage = (statusMessage, messageLevel = 'info') => {
        this.setState({ statusMessage, messageLevel, statusOpen: true });
    }

    _closeStatusMessage = () => { this.setState({ statusOpen: false }) }

    _updateLoadingOverlay = (isLoading, loadingMessage = '') => {
        this.setState({ loading: isLoading, loadingMessage });
    }

    render() {
        return (
            <LoadingOverlay
                active={this.state.loading}
                spinner={
                    <RingLoader
                        color={'#ffffff'}
                        css='margin: auto; margin-bottom: 15px;'
                    />
                }
                text={this.state.loadingMessage}
            >
                <NavBar />
                <Status
                    statusMessage={this.state.statusMessage}
                    messageLevel={this.state.messageLevel}
                    statusOpen={this.state.statusOpen}
                    closeStatusMessage={this._closeStatusMessage}
                />
                <MediaCapturer
                    changeStatusMessage={this._changeStatusMessage}
                    updateLoadingOverlay={this._updateLoadingOverlay}
                />
            </LoadingOverlay>
        );
    }

}

export default App;
