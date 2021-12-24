import React from 'react';

export default function Background ():React.ReactElement{
    return(
        <div className={`bg-light dark:bg-dark h-screen w-screen fixed top-0 left-0`}
            style={{zIndex:-10}}
        ></div>
    )
};