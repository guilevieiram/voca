import { useEffect, useState } from "react";
import { loginUser, UserLoginRequestState } from "../../models";
import Loader from  '../Loader';

type LoginFormProps = {
    darkMode: boolean,
    setToken: (token: string) => void
};


export default function LoginForm ({darkMode, setToken}: LoginFormProps): React.ReactElement {
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [requestState, setRequestState] = useState<UserLoginRequestState>(UserLoginRequestState.NotStarted);

    const changeEmail = (event: any) => setEmail(event.target.value);
    const changePassword = (event: any) => setPassword(event.target.value);
    const onSubmit = (event: any) => {
        event.preventDefault();
        loginUser(email, password, setToken, setRequestState, "http://127.0.0.1:5000");
    };

    useEffect(() => {
        if(requestState === UserLoginRequestState.BackendIssue) window.alert("It seems like our servers are down at the moment ... \n Try again in a few minutes!");
        else if (requestState === UserLoginRequestState.Successful) window.location.reload();
    }, [requestState]);

    return(
        <form action="#" onSubmit={onSubmit} className={`flex flex-col my-10 text-${darkMode ? 'light' : 'dark'}`}>
            <input type="email" name="E-mail" id="email" placeholder="Email" required className={`input-field bg-${darkMode ? 'dark' : 'light'} ${requestState === UserLoginRequestState.UserNotFound ? 'border-red' : '' }`} onChange={changeEmail}/>
            {
                requestState === UserLoginRequestState.UserNotFound ?
                <p className="text-sm text-red">This user does not exists.</p> : <></>
            }
            <input type="password" name="Password" id="password" placeholder="Password" required className={`input-field ${requestState === UserLoginRequestState.WrongPassword ? 'border-red' : ''} bg-${darkMode ? 'dark' : 'light'}`} onChange={changePassword}/>
            {
                requestState === UserLoginRequestState.WrongPassword ?
                <p className="text-sm text-red">Wrong password.</p> : <></>
            }
            {
                requestState === UserLoginRequestState.Waiting ?
                <Loader /> : <input type="submit" value="Log in" className={`secondary-button bg-${darkMode ? 'dark' : 'light'}`} />
            }
            <a href="https://google.com" className={`text-blue underline text-right`}>  Forgot password?</a>
        </form>
    )
};