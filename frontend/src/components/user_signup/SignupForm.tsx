type SignupFormProps = {
    darkMode: boolean
};

function LanguageSelectComponent (): React.ReactElement {
    const languages = [
        {
            "name": "French",
            "flag": "🇫🇷"
        },
        {
            "name": "Russian",
            "flag": "🇫🇷"
        },
        {
            "name": "English",
            "flag": "🇫🇷"
        },
    ]
    const onChange = (event: any): void => {
        console.log(`changed to value`, event)
    };
    return (
        <div className={`w-full flex justify-between items-center my-4`}>
            <p>Language:</p>
            <select value={languages[0].name} onChange={onChange}>
                {languages.map((element, index) => <option value={element.name} key={index}>{element.flag}</option>)}
            </select>
        </div>
    )
}

export default function SignupForm ({darkMode}: SignupFormProps): React.ReactElement {
    const inputClass: string = `input-field bg-${darkMode ? 'dark' : 'light'}`;
    return(
        <form action="#" className={`flex flex-col my-10 text-${darkMode ? 'light' : 'dark'}`}>
            <input type="text" name="Name" id="Name" placeholder="Name" className={inputClass}/>
            <input type="email" name="E-mail" id="email" placeholder="Email" className={inputClass}/>
            <input type="password" name="Password" id="password" placeholder="Password" className={inputClass}/>
            <input type="password" name="Password-2" id="password-2" placeholder="Confirm password" className={inputClass}/>
            <LanguageSelectComponent /> 
            <input type="button" value="Sign up" className={`primary-button my-4`} />
        </form>
    )
}