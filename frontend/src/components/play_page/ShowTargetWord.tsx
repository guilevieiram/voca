
type ShowTargetWordProps = {
    word: string
};

export default function ShowTargetWord ({ word }: ShowTargetWordProps): React.ReactElement {
   return (
        <div className="mt-12 mb-4">
            <h2 className=" text-md">{word}</h2>
        </div>
    )
};