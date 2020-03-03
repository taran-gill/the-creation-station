import React from 'react';
import { Snackbar } from '@rmwc/snackbar';

import './Status.css';

class Status extends React.Component {
    render() {
        return (
            <Snackbar
                open={this.props.statusOpen}
                onClose={this.props.closeStatusMessage}
                message={this.props.statusMessage}
                dismissIcon
                timeout={10000}
                className={this.props.messageLevel}
            />
        );
    }
}

export { Status as default, Status };
