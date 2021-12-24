import { useEffect, useState } from "react";
import { signupUser, UserSignupRequestState} from '../../models/UserRequests';
import { useNavigate } from 'react-router-dom';

type SignupFormProps = {
    darkMode: boolean
};
type LanguageSelectComponentProps = {
    darkMode: boolean,
    setLanguage: (language: string) => void;
};

function LanguageSelectComponent ({darkMode, setLanguage}: LanguageSelectComponentProps): React.ReactElement {
    const languages = [
        {
            "name": "French",
            "flag": "🇫🇷"
        },
        {
            "name": "Russian",
            "flag": "🇷🇺"
        },
        {
            "name": "English",
            "flag": "🇬🇧"
        },
    ]
    const onChange = (event: any): void => setLanguage(event.target.value);
    useEffect((): void => setLanguage(languages[0].name ), []);
    return (
        <div className={`w-full flex justify-between items-center my-4`}>
            <p>Language:</p>
            <select className={`bg-${darkMode ? 'dark' : 'light'}`} onChange={onChange}>
                {languages.map((element, index) => <option value={element.name} key={index} className={`bg-${darkMode ? 'dark' : 'light'}`}>{element.flag}</option>)}
            </select>
        </div>
    )
};

export default function SignupForm ({darkMode}: SignupFormProps): React.ReactElement {
    const navigate = useNavigate();

    const [name, setName] = useState<string>("");
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [passwordCheck, setPasswordCheck] = useState<string>("");
    const [matchPassword, setMatchPassword] = useState<boolean|null>(null);
    const [language, setLanguage] = useState<string>("");
    const [requestState, setRequestState] = useState<UserSignupRequestState>(UserSignupRequestState.NotStarted);
    const onSubmit = (event: any): void => {
        event.preventDefault();
        if(!matchPassword) return;
        console.log(name, email, password, language)
        signupUser(name, email, password, language, setRequestState, "http://127.0.0.1:5000")
    };
    useEffect(():void => password && passwordCheck ? setMatchPassword(password === passwordCheck) : undefined , [password, passwordCheck]);
    useEffect(():void => {
        if(requestState === UserSignupRequestState.BackendIssue) window.alert("It seems like our servers are down at the moment ... \n Try again in a few minutes!");
        else if (requestState === UserSignupRequestState.Successful) {
            window.alert("Signup successful!");
            navigate("/login");
        };
    }, [requestState]);

    return(
        <div>
            <form action="#" onSubmit={onSubmit} className={`flex flex-col my-10 text-${darkMode ? 'light' : 'dark'}`}>
                <input required onChange={(event: any):void => setName(event.target.value)} type="text" name="Name" id="Name" placeholder="Name" className={`input-field bg-${darkMode ? 'dark' : 'light'} `}/>
                <input required onChange={(event: any):void => setEmail(event.target.value)} type="email" name="E-mail" id="email" placeholder="Email" className={`input-field bg-${darkMode ? 'dark' : 'light'} ${requestState === UserSignupRequestState.EmailInUse ? 'border-red' : ''} `}/>
                <p className="text-sm text-red p-0">{requestState === UserSignupRequestState.EmailInUse ? "This email is already in use." : ""}</p>
                <input required onChange={(event: any):void => setPassword(event.target.value)} type="password" name="Password" id="password" placeholder="Password" className={`input-field bg-${darkMode ? 'dark' : 'light'} `}/>
                <input required onChange={(event: any):void => setPasswordCheck(event.target.value)} type="password" name="Password-2" id="password-2" placeholder="Confirm password" className={`input-field bg-${darkMode ? 'dark' : 'light'} ${matchPassword === false ? "border-red" : ""}`}/>
                <p className="text-sm text-red p-0">{matchPassword === false ? "Please make sure the passwords are the same" : ""}</p>
                <LanguageSelectComponent setLanguage={setLanguage} darkMode={darkMode}/> 
                <input type="submit" value="Sign up" className={`primary-button my-4`} />
            </form>
        </div>
    )
};