import SignupForm from './SignupForm';
type UserSignupPageProps = {
    darkMode: boolean
};

export default function UserSignupPage ({darkMode}: UserSignupPageProps): React.ReactElement {
    return (
        <div className={`w-full py-10`}>
            <h1 className={`page-title text-${darkMode ? 'light' : 'dark'}`}>Sign up!</h1>
            <SignupForm darkMode={darkMode} />
        </div>
    )
};