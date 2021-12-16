import { Link } from 'react-router-dom';
type NotFountPageProps = {
    darkMode: boolean
};

function NotFoundPage ({darkMode}: NotFountPageProps): React.ReactElement {
    return (
        <div className={`flex flex-col justify-around items-start my-10 text-${darkMode ? 'light' : 'dark'}`}>
            <h1 className='my-4'>404 Error</h1>           
            <h2 className='my-4'>This page cannot be found ...</h2>
            <p className='my-4'>Go back to our user page <span className='underline'> <Link to = '/'>here.</Link></span></p>
        </div>
    )
};

export default  NotFoundPage;