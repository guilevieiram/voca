import React, { useEffect, useState } from "react";
import ShowTargetWord from "./ShowTargetWord";
import TranslateField from "./TranslateField";
import Score from "./Score";
import NextButton from "./NextButton";
import LoadMore from "./LoadMore";

import { apiEndpoint } from '../../app.config';
import { getWords, GetWordsRequestState, Word, deleteWord, DeleteWordRequestState } from "../../models";
import ReloadWords from "./ReloadWords";

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
    const [getWordsRequestState, setGetWordsRequestState] = useState<GetWordsRequestState>(GetWordsRequestState.NotStarted);
    const [deleteWordRequestState, setDeleteWordsRequestState] = useState<DeleteWordRequestState>(DeleteWordRequestState.NotStarted);
    const nextWord = (): void => {
        setScore(null);
        if (targetWordIndex >= wordsList.length - 1) {
            setTargetWordIndex(0);
            return setFinished(true);
        }
        setTargetWordIndex(targetWordIndex + 1);
    }

    const loadWords = (): void => {
        getWords(userId, setWordsList, setGetWordsRequestState, apiEndpoint);
        setFinished(false);
        setTargetWordIndex(0);
    };

    const deleteCurrentWord = (): void => {
        deleteWord( targetWord.id, setDeleteWordsRequestState, apiEndpoint);
    };

    useEffect(() => {if (JSON.stringify(wordsList) === JSON.stringify([{word: "", id: 0}])) loadWords();}, []);
    useEffect(() => setTargetWord(wordsList[targetWordIndex]), [targetWordIndex, wordsList]);

    useEffect(() => setWordIndexInSessionStorage(targetWordIndex), [targetWordIndex])
    useEffect(() => setWordsListInSessionStorage(wordsList), [wordsList])

    useEffect(() => {
        switch (getWordsRequestState){
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
    }, [getWordsRequestState]);

    useEffect(() => {
        switch (deleteWordRequestState){
            case DeleteWordRequestState.BackendIssue:{
                window.alert("Looks like our servers are down. Try again in a few minutes ...");
                break;
            }
            case DeleteWordRequestState.WordNotFound:{
                window.alert("This word is no longer active in your account.");
                window.location.reload();
                break;
            }
            case DeleteWordRequestState.Successful:{
                window.alert("Word deleted successfully!");
                loadWords();
                break;
            }
            default: break;
        }
    }, [deleteWordRequestState]);

    return (
        <div className="my-6">
            <h1 className="page-title ">Play</h1>
            <div className="h-bar"></div>
            {
                finished ? <LoadMore loadMoreWords={loadWords} />:
                getWordsRequestState === GetWordsRequestState.BackendIssue? 
                <button onClick={() => window.location.reload()} className="secondary-button ">Reload page.</button> :
                <>
                    <ShowTargetWord word={targetWord.word} deleteWord={deleteCurrentWord} />
                    <TranslateField setScore={setScore} wordId={targetWord.id} wordIndex={targetWordIndex} />
                    <div className="w-full flex justify-around items-center my-6">
                        <Score score={score} />
                        <NextButton nextWord={nextWord} show={score !== null}/>
                    </div>
                </>
            }
            <ReloadWords reloadWords={loadWords}/>
        </div>
    )
}