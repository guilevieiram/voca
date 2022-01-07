import React, { useEffect, useState } from "react";
import ShowTargetWord from "./ShowTargetWord";
import TranslateField from "./TranslateField";
import Score from "./Score";
import NextButton from "./NextButton";
import LoadMore from "./LoadMore";

type Word = {
    word: string,
    id: number
};

const setWordsListInSessionStorage = (wordsList: Word[]): void => sessionStorage.setItem("wordList", JSON.stringify(wordsList));
const readWordsListFromSessionStorage = (): Word[] => {
    const wordListString: string | null = sessionStorage.getItem("wordList");
    if(wordListString === null) return [{word: "", id: 0}]
    return JSON.parse(wordListString);
}

const setWordIndexInSessionStorage = (wordIndex: number) => sessionStorage.setItem("wordIndex", JSON.stringify(wordIndex));
const readWordIndexFromSessionStorage = (): number => {
    const wordIndex: string | null = sessionStorage.getItem("wordIndex");
    if(wordIndex === null) return 0;
    return JSON.parse(wordIndex);
}

// need to create a focus system to facilitate keyboard navigating when playing
export default function PlayPage (): React.ReactElement {
    const [wordsList, setWordsList] = useState<Word[]>(readWordsListFromSessionStorage());
    const [targetWordIndex, setTargetWordIndex] = useState<number>(readWordIndexFromSessionStorage());
    const [targetWord, setTargetWord] = useState<Word>(wordsList[targetWordIndex]);
    const [score, setScore] = useState<number | null>(null);
    const [finished, setFinished] = useState<boolean>(false);
    const nextWord = (): void => {
        setScore(null);
        if (targetWordIndex >= wordsList.length - 1) {
            setTargetWordIndex(0);
            return setFinished(true);
        }
        setTargetWordIndex(targetWordIndex + 1);
    }
    const loadWords = (): void => {
        // test load words function, need to be changed for the api call.
        const words: Word[] = [
            {word: "Planet", id: 5},
            {word: "House", id: 10},
            {word: "Floor", id: 3}
        ]
        setWordsList(words);
        setFinished(false);
        setTargetWordIndex(0);
    };

    useEffect(() => {if (JSON.stringify(wordsList) === JSON.stringify([{word: "", id: 0}])) loadWords();}, []);
    useEffect(() => setTargetWord(wordsList[targetWordIndex]), [targetWordIndex, wordsList]);

    useEffect(() => setWordIndexInSessionStorage(targetWordIndex), [targetWordIndex])
    useEffect(() => setWordsListInSessionStorage(wordsList), [wordsList])

    return (
        <div className="my-6">
            <h1 className="page-title ">Play</h1>
            <div className="h-bar"></div>
            {
                finished ?
                <LoadMore loadMoreWords={loadWords} />:
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