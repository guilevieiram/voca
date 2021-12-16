import { useState } from "react";

type LoginFormProps = {
    darkMode: boolean,
    setToken: (token: string) => void
};

function LoginForm ({darkMode, setToken}: LoginFormProps): React.ReactElement {
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const changeEmail = (event: any) => setEmail(event.target.value);
    const changePassword = (event: any) => setPassword(event.target.value);
    const onSubmit = () => setToken('1'); // dummy method

    const inputClass: string = `input-field bg-${darkMode ? 'dark' : 'light'}`;
    return(
        <form action="#" className={`flex flex-col my-10 text-${darkMode ? 'light' : 'dark'}`} onSubmit={onSubmit}>
            <input type="email" name="E-mail" id="email" placeholder="Email" className={inputClass} onChange={changeEmail}/>
            <input type="password" name="Password" id="password" placeholder="Password" className={inputClass} onChange={changePassword}/>
            <input type="submit" value="Log in" className={`secondary-button bg-${darkMode ? 'dark' : 'light'}`} />
            <a href="#"className={`text-blue underline text-right`}>  Forgot password?</a>
        </form>
    )
};
export default LoginForm;