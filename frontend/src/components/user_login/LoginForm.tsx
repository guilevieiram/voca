import { useEffect, useState } from "react";
import { loginUser, UserLoginRequestState } from "../../models";

type LoginFormProps = {
    darkMode: boolean,
    setToken: (token: string) => void
};

function Spinner(): React.ReactElement {
    return (
        <div className="w-fulli flex justify-center items-center my-6">
            <div className="h-10 w-10  border-2 border-b-0 rounded-full  border-blue "></div>
        </div>
    )
}

function LoginForm ({darkMode, setToken}: LoginFormProps): React.ReactElement {
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [loginState, setLoginState] = useState<UserLoginRequestState>(UserLoginRequestState.NotStarted);

    const changeEmail = (event: any) => setEmail(event.target.value);
    const changePassword = (event: any) => setPassword(event.target.value);
    const logUser = (event: any) => {
        event.preventDefault()
        loginUser(email, password, setToken, setLoginState, "http://127.0.0.1:5000")
    };

    useEffect(() => {
        if(loginState === UserLoginRequestState.BackendIssue){
            window.alert("It seems like our servers are down at the moment ... \n Try again in a few minutes!");
        } else if (loginState === UserLoginRequestState.Successful){
            window.location.reload();
        }
    }, [loginState])

    return(
        <form action="#" onSubmit={logUser} className={`flex flex-col my-10 text-${darkMode ? 'light' : 'dark'}`}>
            <input type="email" name="E-mail" id="email" placeholder="Email" required className={`input-field bg-${darkMode ? 'dark' : 'light'}`} onChange={changeEmail}/>
            <input type="password" name="Password" id="password" placeholder="Password" required className={`input-field ${loginState === UserLoginRequestState.WrongPassword ? 'border-red' : ''} bg-${darkMode ? 'dark' : 'light'}`} onChange={changePassword}/>
            {
                loginState === UserLoginRequestState.WrongPassword ?
                <p className="text-sm text-red">Wrong password.</p> : <></>
            }
            {loginState === UserLoginRequestState.Waiting ?
                <Spinner /> :
                <input type="submit" value="Log in" className={`secondary-button bg-${darkMode ? 'dark' : 'light'}`} />
            }
            <a href="https://google.com" className={`text-blue underline text-right`}>  Forgot password?</a>
        </form>
    )
};
export default LoginForm;