import React from "react"

type SaveButtonProps = {
    saveWords: () => void
}

export default function SaveButton ({ saveWords }: SaveButtonProps): React.ReactElement {
    return <button className="primary-button px-10 py-3" onClick={saveWords}>Save</button>
}