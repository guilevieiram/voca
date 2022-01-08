import React, { useEffect, useState } from "react";
import ShowTargetWord from "./ShowTargetWord";
import TranslateField from "./TranslateField";
import Score from "./Score";
import NextButton from "./NextButton";
import LoadMore from "./LoadMore";

import { apiEndpoint } from '../../app.config';
import { getWords, GetWordsRequestState } from "../../models";
import Loader from "../Loader";

type Word = {
    word: string,
    id: number
};

type PlayPageProps = {
    userId: number | null
};

const setWordsListInSessionStorage = (wordsList: Word[]): void => sessionStorage.setItem("wordList", JSON.stringify(wordsList));
const readWordsListFromSessionStorage = (): Word[] => {
    const wordListString: string | null = sessionStorage.getItem("wordList");
    if(wordListString === null || wordListString === "[]") return [{word: "", id: 0}];
    return JSON.parse(wordListString);
};

const setWordIndexInSessionStorage = (wordIndex: number) => sessionStorage.setItem("wordIndex", JSON.stringify(wordIndex));
const readWordIndexFromSessionStorage = (): number => {
    const wordIndex: string | null = sessionStorage.getItem("wordIndex");
    if(wordIndex === null) return 0;
    return JSON.parse(wordIndex);
};



// need to create a focus system to facilitate keyboard navigating when playing
export default function PlayPage ({ userId }: PlayPageProps): React.ReactElement {
    const [wordsList, setWordsList] = useState<Word[]>(readWordsListFromSessionStorage());
    const [targetWordIndex, setTargetWordIndex] = useState<number>(readWordIndexFromSessionStorage());
    const [targetWord, setTargetWord] = useState<Word>(wordsList[targetWordIndex]);
    const [score, setScore] = useState<number | null>(null);
    const [finished, setFinished] = useState<boolean>(false);
    const [requestState, setRequestState] = useState<GetWordsRequestState>(GetWordsRequestState.NotStarted);
    const nextWord = (): void => {
        setScore(null);
        if (targetWordIndex >= wordsList.length - 1) {
            setTargetWordIndex(0);
            return setFinished(true);
        }
        setTargetWordIndex(targetWordIndex + 1);
    }

    // to be soon fixed. the api should give the words ids
    const setWords = (words : string[]): void => setWordsList(words.map(wordString => {return {word: wordString, id: 0}}));
    const loadWords = (): void => {
        getWords(userId, setWords, setRequestState, apiEndpoint);
        setFinished(false);
        setTargetWordIndex(0);
    };

    useEffect(() => {if (JSON.stringify(wordsList) === JSON.stringify([{word: "", id: 0}])) loadWords();}, []);
    useEffect(() => setTargetWord(wordsList[targetWordIndex]), [targetWordIndex, wordsList]);

    useEffect(() => setWordIndexInSessionStorage(targetWordIndex), [targetWordIndex])
    useEffect(() => setWordsListInSessionStorage(wordsList), [wordsList])

    useEffect(() => {
        switch (requestState){
            case GetWordsRequestState.BackendIssue:{
                window.alert("Looks like our servers are down. Try again in a few minutes...");
                setWordsListInSessionStorage([]);
                break;
            }
            case GetWordsRequestState.UserNotFound:{
                window.alert("You've been disconnected, please login.");
                setWordsListInSessionStorage([]);
                sessionStorage.removeItem("token");
                window.location.reload();
                break;
            }
            default: break;
        }
    }, [requestState]);

    return (
        <div className="my-6">
            <h1 className="page-title ">Play</h1>
            <div className="h-bar"></div>
            {
                finished ? <LoadMore loadMoreWords={loadWords} />:
                requestState === GetWordsRequestState.BackendIssue? 
                <button onClick={window.location.reload} className="secondary-button ">Reload page.</button> :
                <>
                    <ShowTargetWord word={targetWord.word} />
                    <TranslateField setScore={setScore} score={score} wordIndex={targetWordIndex} />
                    <div className="w-full flex justify-around items-center my-6">
                        <Score score={score} />
                        <NextButton nextWord={nextWord} show={score !== null}/>
                    </div>
                </>
            }
        </div>
    )
}