import { useRef, useState } from "react";

type AddWordsBarProps = {
    addWord: (word: string) => void
};

export default function AddWordsBar ({ addWord }: AddWordsBarProps ): React.ReactElement {
    const [word, setWord] = useState<string>("");
    const changeWord = (event: any): void => setWord(event.target.value);
    const clearInput = (): void => {
        const inputField: any = document.querySelector("#add-word-input");
        inputField.value = "";
    };
    const sumbitWord = (event: any): void => {
        event.preventDefault();
        addWord(word);
        clearInput();
    };
    return(
        <div className="my-2 w-full">
            <form className="flex items-center w-full" autoComplete="off" >
                <input id="add-word-input" type="text" placeholder="Add words" className="input-field w-full mr-4" onChange={changeWord}/>
                <button onClick={sumbitWord} className="rounded-button px-2 mr-4 text-lg ">+</button>
            </form>
        </div>
    )
}