import React, { useEffect, useState } from 'react';

import AddWordsBar from './AddWordsBar';
import SaveButton from './SaveButton';
import AddWordsList from './WordsList';
import Loader from '../Loader';

import { apiEndpoint } from '../../app.config';
import { addWords, AddWordsRequestState } from '../../models';

type AddWordsPageProps = {
    userId: number | null
};

const getWordsFromSessionStorage = (): string[] => {
    const storedWords: string | null = sessionStorage.getItem("words");
    if (storedWords) return JSON.parse(storedWords)
    else return []
};

export default function AddWordsPage ({ userId }: AddWordsPageProps): React.ReactElement {
    const [words, setWords] = useState<string[]>(getWordsFromSessionStorage());
    const [requestState, setRequestState] = useState<AddWordsRequestState>(AddWordsRequestState.NotStarted);
    const addWord = (word: string): void => {if (!words.includes(word)) setWords([...words, word])};
    const removeWord = (word: string): void => setWords(words.filter(item => item !== word));
    const saveWords = (): void => {
        if (words.length === 0){
            window.alert("Try adding some words before saving!");
            return 
        }
        addWords(userId, words, setRequestState, apiEndpoint)
        setWords([]);
    };

    useEffect(() => sessionStorage.setItem("words", JSON.stringify(words)), [words]);

    useEffect(() => {
        switch (requestState){
            case AddWordsRequestState.BackendIssue:{
                window.alert("Looks like our servers are down. Try again in a few minutes...");
                break;
            }
            case AddWordsRequestState.UserNotFound:{
                window.alert("You've been disconnected, please login.");
                sessionStorage.removeItem("token");
                window.location.reload();
                break;
            }
            case AddWordsRequestState.Successful:{
                window.alert("Words added successfully! You can now keep playing!");
                break;
            }
            default: break;
        }
    }, [requestState]);

    return (
        <div className='flex flex-col items-start min-h-screen'>
            <h1 className='page-title'>New vocabulary</h1>
            <div className="h-bar mb-6"></div>
            <AddWordsBar addWord={addWord}/>
            <AddWordsList words={words} removeWord={removeWord}/>

            <div className="bottom-float">
                {
                    requestState === AddWordsRequestState.Waiting ? <Loader /> :
                    <SaveButton saveWords={saveWords} />
                }
            </div>
        </div>
    )
}
