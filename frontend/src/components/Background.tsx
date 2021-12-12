type BackgroundProps = {
    darkMode: boolean
};

function Background ({darkMode}: BackgroundProps) {
    return(
        <div className={`bg-${darkMode ? 'dark' : 'light'} h-screen w-screen absolute top-0 left-0`}></div>
    )
}

export default Background