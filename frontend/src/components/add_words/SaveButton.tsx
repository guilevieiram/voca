import React from "react"

type SaveButtonProps = {
    saveWords: () => void
}

export default function SaveButton ({ saveWords }: SaveButtonProps): React.ReactElement {
    return (
        <div className="fixed top-3/4 right-0 m-10">
            <button className="primary-button px-10 py-3" onClick={saveWords}>Save</button>
        </div>
    )
}