import SignupForm from './SignupForm';
import RedirectToLogin from './RedirectToLogin';

export default function UserSignup (): React.ReactElement {
    return (
        <div className={`w-full py-10`}>
            <h1 className={`page-title text-dark dark:text-light`}>Sign up!</h1>
            <SignupForm />
            <RedirectToLogin /> 
        </div>
    )
};