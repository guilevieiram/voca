function Background({darkMode}){
    return <div style={{zIndex: -10}} className={`bg-${darkMode ? 'dark' : 'light'} h-screen w-screen absolute left-0 top-0`}></div>
};

export default Background;