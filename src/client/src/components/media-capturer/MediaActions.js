import React from 'react';
import { Button } from '@rmwc/button';

import './MediaActions.css';

class MediaActions extends React.Component {
    render() {
        const playButton = !this.props.recording ?
            <Button raised icon='play_arrow' label='Start' className='media-actions__start-button' onClick={this.props.onStart} /> :
            <Button raised danger icon='stop' label='Stop' className='media-actions__stop-button' onClick={this.props.onStop} />;

        const uploadButton = (
            <Button
                raised
                icon='cloud_upload'
                label='Upload'
                theme={['secondaryBg', 'onSecondary']}
                className='media-actions__upload-button'
                disabled={!this.props.blob}
                onClick={this.props.onUpload}
            />
        );

        return (
            <div className='media-actions'>
                When you're ready, { playButton } recording your presentation.

                <br />
                <br />

                Once you're happy with your work, { uploadButton } to see how you did!
            </div>
        );
    }
}

export { MediaActions as default, MediaActions };