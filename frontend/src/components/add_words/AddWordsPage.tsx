import React, { useEffect, useState } from 'react';

import AddWordsBar from './AddWordsBar';
import SaveButton from './SaveButton';
import AddWordsList from './WordsList';

const getWordsFromSessionStorage = (): string[] => {
    const storedWords: string | null = sessionStorage.getItem("words");
    if (storedWords) return JSON.parse(storedWords)
    else return []
};

export default function AddWordsPage (): React.ReactElement {
    const [words, setWords] = useState<string[]>(getWordsFromSessionStorage());
    const addWord = (word: string): void => {if (!words.includes(word)) setWords([...words, word])};
    const removeWord = (word: string): void => setWords(words.filter(item => item !== word));
    const saveWords = (): void => {
        // in this function we need to call the server api to actually save the words...
        console.log("saving words...")
        setWords([]);
        window.alert("Your new vocabulary has been saved!")
    };

    useEffect(() => {
        sessionStorage.setItem("words", JSON.stringify(words));
    }, [words])

    return (
        <div className='flex flex-col items-start min-h-screen'>
            <h1 className='page-title'>New vocabulary</h1>
            <AddWordsBar addWord={addWord}/>
            <AddWordsList words={words} removeWord={removeWord}/>
            <SaveButton saveWords={saveWords} />
        </div>
    )
}
