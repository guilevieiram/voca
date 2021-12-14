type LoginFormProps = {
    darkMode: boolean
};
function LoginForm ({darkMode}: LoginFormProps): React.ReactElement {
    const inputClass: string = `input-field bg-${darkMode ? 'dark' : 'light'}`;
    return(
        <form action="#" className={`flex flex-col my-10 text-${darkMode ? 'light' : 'dark'}`}>
            <input type="email" name="E-mail" id="email" placeholder="Email" className={inputClass}/>
            <input type="password" name="Password" id="password" placeholder="Password" className={inputClass}/>
            <input type="button" value="Log in" className={`secondary-button bg-${darkMode ? 'dark' : 'light'}`} />
            <a href="#"className={`text-blue underline text-right`}>  Forgot password?</a>
        </form>
    )
};
export default LoginForm;