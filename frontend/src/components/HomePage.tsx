type HomePageProps = {
    darkMode: boolean
};

export default function HomePage ({ darkMode }:HomePageProps): React.ReactElement {
    return(
        <div>
            <h1 className={`my-10 text-${darkMode ? 'light' : 'dark'}`}>Welcome home!</h1>
        </div>
    )
};