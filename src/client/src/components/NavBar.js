import React from 'react';
import {
    TopAppBar,
    TopAppBarRow,
    TopAppBarSection,
    TopAppBarActionItem,
    TopAppBarTitle,
    TopAppBarFixedAdjust,
} from '@rmwc/top-app-bar';

import './NavBar.css';

import Logo from '../assets/logo.png';

class NavBar extends React.Component {
    render() {
        return (
            <React.Fragment>
                <TopAppBar className='navbar'>
                    <TopAppBarRow>
                        <TopAppBarSection>
                            <img src={Logo} className='navbar__logo' />
                            <TopAppBarTitle className='navbar__title'>THE CREATION STATION</TopAppBarTitle>
                        </TopAppBarSection>
                        <TopAppBarSection alignEnd>
                            <a href='https://github.com/taran-gill/the-creation-station' target="_blank" rel="noopener">
                                <i className="fa fa-github" alt='github'></i>
                            </a>
                        </TopAppBarSection>
                    </TopAppBarRow>
                </TopAppBar>
                <TopAppBarFixedAdjust />
            </React.Fragment>
        );
    }
}
export { NavBar as default, NavBar };