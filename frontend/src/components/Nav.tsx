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

type NavProps = {
    darkMode: boolean
};

type ButtonProps = {
    active: boolean,
    icon: string,
    link: string,
    height: number
};

type NavLogoButtonProps = {
    icon: string,
    link: string,
    height: number
}

function Button ({active, icon, link, height}: ButtonProps): React.ReactElement {
    return (
        <div  className={`h-full z-10 flex justify-center items-end fill-${active ? 'purple' : 'dark'}`}>
            <a href={link}>
                <img src={icon} alt={icon} className={`h-${height} p-3 bottom-0 filter drop-shadow-lg`}/>
            </a>
        </div>
    )
};

function NavLogoButton ({icon, link, height}: NavLogoButtonProps):React.ReactElement {
    return (
        <a href={link} className={`h-full`}>
            <img src={icon} alt={icon} className={`h-${height} p-1 filter drop-shadow-lg`}/>
        </a>
    )
}

function Nav ({darkMode}: NavProps): React.ReactElement {
    const barFullSize: number = 16;
    const barBlueSize: number = 10;

    return (
        <div className={`absolute bottom-0 left-0 w-screen  h-${barFullSize} flex justify-center items-center`}>
            <div className={`w-screen h-${barBlueSize} absolute bottom-0 left-0 bg-blue`}></div>
            <div className={`max-w-2xl w-full h-full px-4 z-10 flex justify-around items-center`}>
                <Button active={false} icon={addIcon} link='' height={barBlueSize}/>
                <Button active={false} icon={homeIcon} link='' height={barBlueSize}/>
                <NavLogoButton icon={navLogo} link='' height={barFullSize}/>
                <Button active={false} icon={playIcon} link='' height={barBlueSize}/>
                <Button active={true} icon={pointsIcon} link='' height={barBlueSize}/>
            </div>
        </div>
    )
};

export default Nav