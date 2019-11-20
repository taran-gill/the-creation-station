import React from 'react';
import { Button } from '@rmwc/button';
import * as posenet from '@tensorflow-models/posenet';

import Connection from '../connection';

import './MediaCapturer.css';
import { drawSkeleton } from '../util/canvas';

const CONSTRAINTS = { audio: true, video: { facingMode: 'user' } };

const TYPES = ['video/webm;codecs=vp8', 'video/webm', ''];

class MediaCapturer extends React.Component {
    constructor(props) {
        super(props);
        this.video = React.createRef();
        this.canvas = React.createRef();

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

    async componentDidMount() {
        this.net = await posenet.load();
    }

    onStart = () => {
        const handleSuccess = async (stream) => {
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

            this.video.current.onloadedmetadata = this.detectPose;
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
        Connection.put('/upload', this.state.blob);
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

    detectPose = () => {
        const canvasContext = this.canvas.current.getContext('2d');
        Object.assign(this.canvas.current, { width: this.video.current.videoWidth, height: this.video.current.videoHeight });
        this.poseDetectionFrame(canvasContext);
    }

    poseDetectionFrame = (canvasContext) => {
        const findPoseDetectionFrame = async () => {
            const poses = await this.net.estimateSinglePose(
                this.video.current,
                1,
                true,
                8
            )

            canvasContext.clearRect(0, 0, this.video.current.videoWidth, this.video.current.videoHeight)
        
            canvasContext.save()
            canvasContext.scale(-1, 1)
            canvasContext.translate(-this.video.current.videoWidth, 0)
            canvasContext.drawImage(this.video.current, 0, 0, this.video.current.videoWidth, this.video.current.videoHeight)
            canvasContext.restore();

            console.log(poses.score)
            // if (score < 0.7) return;
            drawSkeleton(poses.keypoints, 0, canvasContext);

            requestAnimationFrame(findPoseDetectionFrame)
        }
        findPoseDetectionFrame()
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
                            <Button raised icon='play_arrow' label='Start' theme={['secondaryBg', 'onSecondary']} onClick={this.onStart} /> :
                            <Button raised danger icon='stop' label='Stop' onClick={this.onStop} />
                    }
                    
                    <video playsInline ref={this.video}></video>
                    <canvas ref={this.canvas}/>

                    {
                        this.state.blob &&
                            <Button raised icon='cloud_upload' label='Upload' theme={['secondaryBg', 'onSecondary']} onClick={this.onUpload} />
                    }
                </div>
            </React.Fragment>
        );
    }


}

export { MediaCapturer as default, MediaCapturer };
