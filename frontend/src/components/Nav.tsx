// I'm still not sure how to do the purple icons idea work without changing the workings of the routing managemenet system.

import playIcon from '../assets/nav-icons/Play.svg';
// import playIconPurple from '../assets/nav-icons/Play-purple.svg';
import homeIcon from '../assets/nav-icons/Home.svg';
// import homeIconPurple from '../assets/nav-icons/Home-purple.svg';
import addIcon from '../assets/nav-icons/Add.svg';
// import addIconPurple from '../assets/nav-icons/Add-purple.svg';
import pointsIcon from '../assets/nav-icons/Points.svg';
// import pointsIconPurple from '../assets/nav-icons/Points-purple.svg';

import navLogo from '../assets/nav-logo.svg';
import React from 'react';
import {Link} from 'react-router-dom';

type ButtonProps = {
    active: boolean,
    icon: string,
    link: string
};

type NavLogoButtonProps = {
    icon: string,
    link: string
};

function Button ({active, icon, link}: ButtonProps): React.ReactElement {
    return (
        <div  className={
            active ?
            `h-full z-10 flex justify-center items-end fill-purple`:
            `h-full z-10 flex justify-center items-end fill-dark`
        }>
            <Link to={link}>
                <img src={icon} alt={icon} className={`h-10 p-3 bottom-0 filter drop-shadow-lg`}/>
            </Link>
        </div>
    )
};

function NavLogoButton ({icon, link}: NavLogoButtonProps):React.ReactElement {
    return (
        <a href={link} className={`h-full`}>
            <img src={icon} alt={icon} className={`h-16 p-1 filter drop-shadow-lg`}/>
        </a>
    )
};

export default function Nav (): React.ReactElement {

    return (
        <div className={`fixed bottom-0 left-0 w-screen  h-16 flex justify-center items-center`}>
            <div className={`w-screen h-10 absolute bottom-0 left-0 bg-blue`}></div>
            <div className={`max-w-2xl w-full h-full px-4 z-10 flex justify-around items-center`}>
                <Button active={false} icon={addIcon} link='/add_words' />
                <Button active={false} icon={homeIcon} link='/user_page' />
                <NavLogoButton icon={navLogo} link='/' />
                <Button active={false} icon={playIcon} link='/play' />
                <Button active={false} icon={pointsIcon} link='/config' />
            </div>
        </div>
    )
};