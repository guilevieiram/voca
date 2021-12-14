import { Link } from 'react-router-dom';
type NotFountPageProps = {
    darkMode: boolean
};

function NotFoundPage ({darkMode}: NotFountPageProps): React.ReactElement {
    return (
        <div>
            <h1>404 Error</h1>           
            <h2>This page cannot be found ...</h2>
            <p>Go back to our user page 
                <Link to = '/'> here .</Link>
            </p>
        </div>
    )
};

export default  NotFoundPage;