import React from 'react';

const errors = {
    notSupported: 'In-browser recording not supported. Please switch browsers or upload an existing presentation on your device.'
};

class MediaRecorder extends React.Component {
    state = {
        error: null,
        stream: null,
    }

    async componentDidMount() {
        if (!window.MediaRecorder) {
            return this.setState({ error: errors.notSupported });
        }

        const stream = await this.getMediaStream();
        this.setState({ stream });
    }

    async getMediaStream() {
        try {
            const stream = await window.navigator.mediaDevices.getUserMedia({
                audio: true,
                video: { width: 1280, height: 720 }
            });
            return stream;
        } catch (error) {
            this.setState({ error });
        }
    }

    render() {
        if (this.state.error) {
            console.error(this.state.error)
            return <p>Err</p>
        }

        return (
            <React.Fragment>
                <video src={this.stream} controls/>
            </React.Fragment>
        )
    }
}

export { MediaRecorder as default, MediaRecorder };
