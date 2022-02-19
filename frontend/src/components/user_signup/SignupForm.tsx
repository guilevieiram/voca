import { useEffect, useState } from "react";
import { signupUser, UserSignupRequestState, getSupportedLanguages, Language} from '../../models';
import { useNavigate } from 'react-router-dom';
import { apiEndpoint } from "../../app.config";
import Loader from "../Loader";

type LanguageSelectComponentProps = {
    setLanguage: (language: string) => void,
    languagesGetSuccess: boolean | null,
    setLanguagesGetSuccess : (state: boolean) => void
};

function LanguageSelectComponent ({setLanguage, languagesGetSuccess, setLanguagesGetSuccess}: LanguageSelectComponentProps): React.ReactElement {
    const [languages, setLanguages] = useState<Language[]>([{
        name: "",
        flag: "",
        code: ""
    }]);

    const onChange = (event: any): void => setLanguage(event.target.value);
    useEffect((): void => {
        setLanguage(languages[0].code);
        getSupportedLanguages(apiEndpoint, setLanguages, setLanguagesGetSuccess);
    } , []);

    if(languagesGetSuccess !== true) return <></>

    return (
        <div className={`w-full flex justify-between items-center my-4`}>
            <p>Language:</p>
            <select className={`bg-light dark:bg-dark`} onChange={onChange}>
                {languages.map((element, index) => <option title={element.name} value={element.code} key={index} className={`bg-light dark:bg-dark`}>{element.flag}</option>)}
            </select>
        </div>
    )
};

export default function SignupForm (): React.ReactElement {
    const [name, setName] = useState<string>("");
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [passwordCheck, setPasswordCheck] = useState<string>("");
    const [matchPassword, setMatchPassword] = useState<boolean|null>(null);
    const [language, setLanguage] = useState<string>("");
    const [requestState, setRequestState] = useState<UserSignupRequestState>(UserSignupRequestState.NotStarted);
    const [languagesGetSuccess, setLanguagesGetSuccess] = useState<boolean|null>(null);

    const navigate = useNavigate();
    const onSubmit = (event: any): void => {
        event.preventDefault();
        if(!matchPassword) return;
        signupUser(name, email, password, language, setRequestState, apiEndpoint)
    };

    useEffect(():void => password && passwordCheck ? setMatchPassword(password === passwordCheck) : undefined , [password, passwordCheck]);
    useEffect(():void => {
        if(requestState === UserSignupRequestState.BackendIssue) window.alert("It seems like our servers are down at the moment ... \n Try again in a few minutes!");
        else if (requestState === UserSignupRequestState.Successful ) {
            window.alert("Signup successful!");
            navigate("/login");
        };
    }, [requestState]);
    useEffect((): void => {
        console.log(languagesGetSuccess)
        if(languagesGetSuccess === false) window.alert("It seems like our servers are down at the moment ...")
    }, [languagesGetSuccess])

    return(
        <form action="#" onSubmit={onSubmit} className={`flex flex-col my-10 text-dark dark:text-light`}>
            <input required onChange={(event: any):void => setName(event.target.value)} type="text" name="Name" id="Name" placeholder="Name" className={`input-field bg-light dark:bg-dark `}/>
            <input required onChange={(event: any):void => setEmail(event.target.value)} type="email" name="E-mail" id="email" placeholder="Email" className={requestState === UserSignupRequestState.EmailInUse ? 'input-field bg-light dark:bg-dark border-red' : 'input-field bg-light dark:bg-dark'}/>
            {
                requestState === UserSignupRequestState.EmailInUse ?
                <p className="text-sm text-red p-0">This email is already in use.</p> : <></>
            }
            <input required onChange={(event: any):void => setPassword(event.target.value)} type="password" name="Password" id="password" placeholder="Password" className={`input-field bg-light dark:bg-dark`}/>
            <input required onChange={(event: any):void => setPasswordCheck(event.target.value)} type="password" name="Password-2" id="password-2" placeholder="Confirm password" className={matchPassword === false ? "input-field bg-light dark:bg-dark border-red" : "input-field bg-light dark:bg-dark"}/>
            {
                matchPassword === false ?
                <p className="text-sm text-red p-0">Please make sure the passwords are the same.</p> : <></>
            }
            <LanguageSelectComponent setLanguage={setLanguage} languagesGetSuccess={languagesGetSuccess} setLanguagesGetSuccess={setLanguagesGetSuccess}/> 
            {
                requestState === UserSignupRequestState.Waiting ?
                <Loader/> :
                <input type="submit" value="Sign up" className={`primary-button my-4`} />
            }
        </form>
    )
};