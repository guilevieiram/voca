import {Link} from 'react-router-dom';

export default function RedirectToLogin(): React.ReactElement {
    return (
        <div>
            <p className={`text-sm text-dark dark:text-light`}>Already have an account?</p>
            <Link to="/login">
                <button className={`secondary-button bg-light dark:bg-dark`}>Log in!</button>
            </Link>
        </div>
    )
};