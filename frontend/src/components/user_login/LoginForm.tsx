import { useState } from "react";
import { loginUser, UserLoginRequestState } from "../../models";

type LoginFormProps = {
    darkMode: boolean,
    setToken: (token: string) => void
};
type Response = {
    code: number, 
    message: string,
    id?: number
};
type LoginButtonProps = {
    darkMode: boolean,
    logUser: () => void
};

function Spinner(): React.ReactElement {
    return (
        <div className="w-fulli flex justify-center items-center my-6">
            <div className="h-10 w-10  border-2 border-b-0 rounded-full  border-blue "></div>
        </div>
    )
}

function LoginButton ({darkMode, logUser}: LoginButtonProps): React.ReactElement {
    return <button onClick={logUser} className={`secondary-button bg-${darkMode ? 'dark' : 'light'}`}>Log in</button>
}

function LoginForm ({darkMode, setToken}: LoginFormProps): React.ReactElement {
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [loginState, setLoginState] = useState<UserLoginRequestState>(UserLoginRequestState.NotStarted);

    const changeEmail = (event: any) => setEmail(event.target.value);
    const changePassword = (event: any) => setPassword(event.target.value);
    const logUser = () => loginUser(email, password, setToken, setLoginState, "http://127.0.0.1:5000");

    const inputClass: string = `input-field bg-${darkMode ? 'dark' : 'light'}`;
    return(
        <form action="#" className={`flex flex-col my-10 text-${darkMode ? 'light' : 'dark'}`}>
            <input type="email" name="E-mail" id="email" placeholder="Email" className={inputClass} onChange={changeEmail}/>
            <input type="password" name="Password" id="password" placeholder="Password" className={inputClass} onChange={changePassword}/>
            {loginState === UserLoginRequestState.Waiting ?
                <Spinner /> :
                <LoginButton darkMode={darkMode} logUser={logUser} />
            }
            <a href="#"className={`text-blue underline text-right`}>  Forgot password?</a>
        </form>
    )
};
export default LoginForm;