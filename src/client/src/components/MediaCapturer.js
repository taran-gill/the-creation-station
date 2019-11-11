import React from 'react';
import { Button } from '@rmwc/button';

import './MediaCapturer.css';

navigator.getUserMedia = navigator.getUserMedia ||
						 navigator.webkitGetUserMedia ||
						 navigator.mozGetUserMedia ||
                         navigator.msGetUserMedia;

const MediaStream = window.MediaStream || window.webkitMediaStream;

if (MediaStream && !Reflect.has(MediaStream.prototype, 'stop')) {
    MediaStream.prototype.stop = function() {
        this.getAudioTracks().forEach(function(track) { track.stop(); });
        this.getVideoTracks().forEach(function(track) { track.stop(); });
    };
}

const CONSTRAINTS = {
    audio: true,
    video: true
};

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

            this.setState({ mediaRecorder, recording: true }, () => {
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
            this.downloadVideo();
        });
    }

    attachToVideoElement = () => {
        this.video.current.srcObject = this.stream;
    }

    releaseFromVideoElement = () => {
        this.video.current.srcObject = null;
    }

    downloadVideo = () => {
        const url = URL.createObjectURL(this.state.blob);
		const a = document.createElement('a');
		a.style.display = 'none';
		a.href = url;
		a.setAttribute('download', 'presentation');
		document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
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
                    {
                        !this.state.recording ?
                            <Button raised icon='play_arrow' label='Start' onClick={this.onStart} /> :
                            <Button raised danger icon='stop' label='Stop' onClick={this.onStop} />
                    }
                    
                    <video ref={this.video} autoPlay></video>
                </div>
            </React.Fragment>
        );
    }


}

export { MediaCapturer as default, MediaCapturer };
