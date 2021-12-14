type HomePageProps = {
    darkMode: boolean
};

function HomePage ({ darkMode }:HomePageProps): React.ReactElement {
    return(
        <div>
            <h1>Welcome home!</h1>
        </div>
    )
};

export default HomePage;