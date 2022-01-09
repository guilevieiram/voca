import { useEffect, useState } from "react";

import { apiEndpoint } from "../../app.config";
import { getScore, GetScoreRequestState } from "../../models";
import Loader from "../Loader";

type TranslateFieldProps = {
    setScore: (score: number) => void,
    wordId: number,
    wordIndex: number
};

export default function TranslateField ({ setScore, wordId, wordIndex}: TranslateFieldProps): React.ReactElement {
    const [translatedWord, setTranslatedWord] = useState<string>("");
    const [requestState, setRequestState] = useState<GetScoreRequestState>(GetScoreRequestState.NotStarted);
    const changeTranslatedWord = (event: any): void => setTranslatedWord(event.target.value);
    const submitWord = (event: any): void => {
        event.preventDefault();
        setTranslatedWord("");
        getScore(wordId, translatedWord, setScore, setRequestState, apiEndpoint)
    };  
    useEffect(() => {
        const inputElement: any = document.querySelector("#translate-word-input");
        inputElement.value = "";
    },[wordIndex])

    // Error handling with the screen alerts
    useEffect(() => {
        switch(requestState){
            case GetScoreRequestState.BackendIssue: {
                window.alert("Looks like our servers are down. Come back in a few minutes...");
                break;
            }
            case GetScoreRequestState.UserNotFound: {
                window.alert("You've been disconnected, please login.");
                sessionStorage.removeItem("token");
                window.location.reload();
                break;
            }
            case GetScoreRequestState.TranslationError: {
                window.alert("Looks like google cannot translate that... Try something else.");
                break;
            }
            case GetScoreRequestState.NlpError: {
                window.alert("Sorry, our Machine Learning model just crashed. Thank you for comming back in a few minutes.");
                break;
            }
            default: break;
        }
    })

    return (
        <div className="w-full">
            <form autoComplete="off" className="flex justify-between items-center">
                <input onChange={changeTranslatedWord} type="text" id="translate-word-input" placeholder="Translation" className="input-field w-full mr-4"/>
                <button onClick={submitWord} className="rounded-button px-3">{!translatedWord ? "?" : ">"}</button>
            </form>
            {
                requestState === GetScoreRequestState.Waiting ? <Loader /> : <></>
            }
        </div>
    )
};
