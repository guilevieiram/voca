import {Link} from 'react-router-dom';

type GoToLoginProps = {

};

export default function GoToLogin (): React.ReactElement {
    return (
        <div className="py-6">
            <p>Already have an account?</p>
            <Link to="/login" className='no-underline hover:no-underline'>
                <div className="primary-button flex justify-center items-center">
                        Log in
                </div>
            </Link>
        </div>
    )
}