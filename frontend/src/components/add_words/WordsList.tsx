import {BiTrashAlt} from 'react-icons/bi';

type WordsListProps = {
    words: string[],
    removeWord: (word: string) => void
};
type WordLineProps = {
    word: string,
    remove: () => void
};

function WordLine ({ word, remove }: WordLineProps): React.ReactElement {
    return (
        <div className="w-full">
            <div className="flex items-center">
                <p className="p-2 w-full">{word}</p>
                <span className="cursor-pointer mx-2" onClick={remove}>
                    <BiTrashAlt size={20}/>
                </span>
            </div>
            <div className="h-px bg-dark dark:bg-light w-full"></div>
        </div>
    )
};

export default function WordsList({ words, removeWord }: WordsListProps): React.ReactElement{
    return (
        <div className="w-full">
            {words.slice(0).reverse().map((word, index) => 
                <WordLine key={index} word={word} remove={() => removeWord(word)} />
            )}
        </div>
    )
};