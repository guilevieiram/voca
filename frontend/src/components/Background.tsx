import React from 'react';
type BackgroundProps = {
    darkMode: boolean
};

function Background ({darkMode}: BackgroundProps):React.ReactElement{
    return(
        <div className={`bg-${darkMode ? 'dark' : 'light'} h-screen w-screen fixed top-0 left-0`}
            style={{zIndex:-10}}
        ></div>
    )
}

export default Background