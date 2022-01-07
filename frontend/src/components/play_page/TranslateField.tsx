import { useEffect, useState } from "react";

type TranslateFieldProps = {
    setScore: (score: number) => void,
    score: number | null,
    wordIndex: number
};

export default function TranslateField ({ setScore, score, wordIndex}: TranslateFieldProps): React.ReactElement {
    const [translatedWord, setTranslatedWord] = useState<string>("");
    const changeTranslatedWord = (event: any): void => setTranslatedWord(event.target.value);
    // This function needs to be implemented to support the api calls. Right now it does nothing.
    const submitWord = (event: any): void => {
        event.preventDefault();
        setTranslatedWord("");
        setScore(0.40);
    };  
    useEffect(() => {
        const inputElement: any = document.querySelector("#translate-word-input");
        inputElement.value = "";
    },[wordIndex])

    return (
        <div className="w-full">

            <form autoComplete="off" className="flex justify-between items-center">
                <input onChange={changeTranslatedWord} type="text" id="translate-word-input" placeholder="Translation" className="input-field w-full mr-4"/>
                <button onClick={submitWord} className="rounded-button px-3">{!translatedWord ? "?" : ">"}</button>
            </form>
        </div>
    )
};
