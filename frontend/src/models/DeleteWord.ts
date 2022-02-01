enum DeleteWordRequestState {
    NotStarted,
    Started,
    Waiting,
    Successful,
    WordNotFound,
    BackendIssue
};

type setRequestStateType = (requestState: DeleteWordRequestState) => void;

function deleteWord(wordId: number, setRequestState: setRequestStateType, url: string ): void {
    const endpoint = `${url}language/inactivate_word`;
    const data = {
        word_id: wordId
    };
    const parameters = {
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
        method: "POST"
    };

    setRequestState(DeleteWordRequestState.Waiting);
    fetch(endpoint, parameters)
    .then( data => data.json())
    .then( response => {
        console.log(response);
        switch(response.code){
            case 1: {
                setRequestState(DeleteWordRequestState.Successful);
                break;
            }
            case -8: {
                setRequestState(DeleteWordRequestState.WordNotFound);
                break;
            }
            default:{
                setRequestState(DeleteWordRequestState.BackendIssue);
                break;
            }
        }
    })
    .catch( e => {
        setRequestState(DeleteWordRequestState.BackendIssue);
        console.log(e);
    });
};

export{
    DeleteWordRequestState,
    deleteWord
}