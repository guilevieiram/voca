type ReloadWordsPropsType = {
    reloadWords: () => void;
};

export default function ReloadWords ({reloadWords}: ReloadWordsPropsType): React.ReactElement {
    return(
        <div className="bottom-float">
            <button className="secondary-button px-10" onClick={reloadWords}>Refresh words</button>
        </div>
    )
}