type ScoreProps = {
    score: number | null
};

export default function Score ({ score }: ScoreProps): React.ReactElement {
    return (
        <div className="text-2xl">
            {
            score === null ?
            <></> :
            <p className={
                    // more cathegories can be added for a smother UX
                    score < 0.33 ?
                    "text-red" :
                    score < 0.66 ?
                    "text-yellow-400" :
                    score < 1 ?
                    "text-green-600":
                    ""
                }>{(score*100).toFixed(2)}%</p>
            }
        </div>
    )
};