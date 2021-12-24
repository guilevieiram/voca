import {Link} from 'react-router-dom';

type RedirectToLoginProps = {
    darkMode: boolean
};

export default function RedirectToLogin({darkMode}: RedirectToLoginProps): React.ReactElement {
    return (
        <div>
            <p className={`text-sm text-${darkMode ? 'light' : 'dark'}`}>Already have an account?</p>
            <Link to="/login">
                <button className={`secondary-button bg-${darkMode ? 'dark' : 'light'}`}>Log in!</button>
            </Link>
        </div>
    )
};