import { CgArrowLongRight } from 'react-icons/cg';
type NextButtonProps = {
    nextWord: () => void,
    show: boolean
};

export default function NextButton ({ nextWord, show }: NextButtonProps): React.ReactElement {
    return (
        show ?
        <button onClick={nextWord} className="secondary-rounded-button w-max px-2">
            <CgArrowLongRight size={20}/>
        </button> :
        <></>
    )
};