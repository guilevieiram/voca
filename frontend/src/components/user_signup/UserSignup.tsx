import SignupForm from './SignupForm';
import RedirectToLogin from './RedirectToLogin';
type UserSignupProps = {
    darkMode: boolean
};

export default function UserSignup ({darkMode}: UserSignupProps): React.ReactElement {
    return (
        <div className={`w-full py-10`}>
            <h1 className={`page-title text-${darkMode ? 'light' : 'dark'}`}>Sign up!</h1>
            <SignupForm darkMode={darkMode} />
            <RedirectToLogin darkMode={darkMode}/>
        </div>
    )
};