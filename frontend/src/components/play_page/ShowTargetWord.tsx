import {BiTrashAlt} from 'react-icons/bi';

type ShowTargetWordProps = {
    word: string,
    deleteWord: () => void
};

export default function ShowTargetWord ({ word, deleteWord }: ShowTargetWordProps): React.ReactElement {
   return (
        <div className="mt-12 mb-4 flex items-center justify-between">
            <h2 className=" text-md">{word}</h2>
            <span className="cursor-pointer mx-2" onClick={deleteWord}>
                <BiTrashAlt size={20}/>
            </span>
        </div>
    )
};