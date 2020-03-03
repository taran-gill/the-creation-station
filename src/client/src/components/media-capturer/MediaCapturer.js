import React from 'react'

import './polyfill';
import { MediaActions } from './MediaActions';

import Connection from '../../connection';

import './MediaCapturer.css';

const CONSTRAINTS = { audio: true, video: true };

const TYPES = ['video/webm;codecs=vp8', 'video/webm', ''];

class MediaCapturer extends React.Component {
    constructor(props) {
        super(props);
        this.video = React.createRef();

        /* Don't need to force rerendering when the mediaChunk changes */
        this.mediaChunk = [];
        this.stream = null;
    }

    state = {
        error: null,
        recording: false,
        mediaRecorder: null,
        blob: null
    }

    onStart = () => {
        const handleSuccess = (stream) => {
            this.stream = stream;
			this.mediaChunk = [];

            const options = {
                mimeType: TYPES.filter(MediaRecorder.isTypeSupported)[0]
            };

			let mediaRecorder = new MediaRecorder(this.stream, options);

			mediaRecorder.ondataavailable = (event) => {
				if(event.data && event.data.size > 0) {
					this.mediaChunk.push(event.data);
				}
			};

            this.setState({ mediaRecorder, recording: true, blob: null }, () => {
                this.state.mediaRecorder.start(10);
                this.attachToVideoElement();
            });
        }

        const handleFailed = (error) => {
			this.setState({
                error: "Please enable webcam/microphone usage for in-browser recording."
            });

            console.error(error);
		};

		if (navigator.mediaDevices) {
			navigator.mediaDevices.getUserMedia(CONSTRAINTS)
                .then(handleSuccess)
                .catch(handleFailed);
		} else if (navigator.getUserMedia) {
			navigator.getUserMedia(CONSTRAINTS, handleSuccess, handleFailed);
		} else {
            this.setState({
                error: "Unable to record in-browser. Please switch browsers or upload an existing presentation on your device."
            });
		}
    }

    onStop = () => {
        this.state.mediaRecorder.stop();

        const blob = new Blob(this.mediaChunk, { type: 'video/webm' });

        this.stream.stop();
        this.stream.getTracks().forEach(track => track.stop());

        this.setState({
            blob,
            recording: false,
        }, () => {
            this.releaseFromVideoElement();
        });
    }

    onUpload = () => {
        const displayError = (err) => {
            this.props.changeStatusMessage('Upload failed.', 'error');
            if (err) console.error(err);
        }

        const formData = new FormData();
        formData.append('video' , 'video.webm');
        formData.append('video-blob', this.state.blob);

        Connection.put('/upload', formData)
            .then(res => {
                if (!res) return displayError();

                this.props.changeStatusMessage('Successfully uploaded!');
            })
            .catch(displayError);
    }

    attachToVideoElement = () => {
        this.video.current.autoplay = true;
        this.video.current.controls = false;
        this.video.current.muted = 'muted';
        this.video.current.srcObject = this.stream;
        this.video.current.src = null;
    }

    releaseFromVideoElement = () => {
        this.video.current.autoplay = false;
        this.video.current.controls = true;
        this.video.current.muted = false;
        this.video.current.srcObject = null;
        this.video.current.src = URL.createObjectURL(this.state.blob);
    }

    render() {
        if (this.state.error) {
            return (
                <p>{this.state.error}</p>
            );
        }
        
        return (
            <React.Fragment>
                <div className='media-capturer'>
                    <video ref={this.video}></video>

                    <MediaActions
                        recording={this.state.recording}
                        blob={this.state.blob}
                        onStart={this.onStart}
                        onStop={this.onStop}
                        onUpload={this.onUpload}
                    />
                </div>
            </React.Fragment>
        );
    }


}

export { MediaCapturer as default, MediaCapturer };
