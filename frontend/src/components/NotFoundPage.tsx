import { Link } from 'react-router-dom';

export default function NotFoundPage (): React.ReactElement {
    return (
        <div className={`flex flex-col justify-around items-start my-10 text-dark dark:text-light`}>
            <h1 className='my-4'>404 Error</h1>           
            <h2 className='my-4'>This page cannot be found ...</h2>
            <p className='my-4'>Go back to our user page <span className='underline'> <Link to = '/'>here.</Link></span></p>
        </div>
    )
};