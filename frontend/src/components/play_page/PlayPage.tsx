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

// need to create a focus system to facilitate keyboard navigating when playing
export default function PlayPage (): React.ReactElement {
    const defaultWordList: Word[] = [{word:"", id: 0}]
    const [wordsList, setWordsList] = useState<Word[]>(defaultWordList);
    const [targetWordIndex, setTargetWordIndex] = useState<number>(0);
    const [targetWord, setTargetWord] = useState<Word>(wordsList[targetWordIndex]);
    const [score, setScore] = useState<number | null>(null);
    const [finished, setFinished] = useState<boolean>(false);
    const nextWord = (): void => {
        setScore(null);
        if (targetWordIndex >= wordsList.length - 1) return setFinished(true);
        setTargetWordIndex(targetWordIndex + 1);
    }
    const loadWords = (): void => {
        // test load words function, need to be changed for the api call.
        console.log("loading words")
        setWordsList([
            {word: "Planet", id: 5},
            {word: "House", id: 10},
            {word: "Floor", id: 3}
        ]);
        setFinished(false);
        setTargetWordIndex(0);
    };

    useEffect(() => loadWords(), []);
    useEffect(() => setTargetWord(wordsList[targetWordIndex]), [targetWordIndex, wordsList]);

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