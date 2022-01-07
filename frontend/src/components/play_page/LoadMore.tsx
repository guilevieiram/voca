type LoadMoreProps = {
    loadMoreWords: () => void
}

export default function LoadMore({ loadMoreWords }: LoadMoreProps): React.ReactElement {
    return(
        <div className="w-full my-10">
            <p>Congrats! You've trainned all your vocabulary!</p>
            <button onClick={loadMoreWords} className="secondary-button">Load more</button>
        </div>
    )
};