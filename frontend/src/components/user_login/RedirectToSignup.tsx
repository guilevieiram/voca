import {Link} from 'react-router-dom';

export default function RedirectToSignup (): React.ReactElement {
    return(
        <div className="w-full mb-32" >
            <p className={`text-blue py-2`}>Don't have an account?</p>
            <Link to="/signup">
                <button className={`primary-button`}>Sign Up!</button>
            </Link>
        </div>
    )
};