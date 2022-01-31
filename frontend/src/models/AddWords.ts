enum AddWordsRequestState {
    NotStarted,
    Started,
    Waiting,
    Successful,
    UserNotFound, 
    BackendIssue
};

type setRequestStateType = (requestState: AddWordsRequestState) => void;

function addWords(userId: number | null, wordsList: string[], setRequestState: setRequestStateType, url: string): void {
    const endpoint = `${url}language/add_words`;
    const data = {
        user_id: userId,
        words: wordsList
    };
    const parameters = {
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
        method: "POST"
    };

    setRequestState(AddWordsRequestState.Waiting)
    fetch(endpoint, parameters)
    .then( (data) => {
        return data.json();
    })
    .then( (response) => {
        console.log(response);
        switch(response.code){
            case 1:{
                setRequestState(AddWordsRequestState.Successful);
                break;
            }
            case -5:{
                setRequestState(AddWordsRequestState.UserNotFound);
                break;
            }
            default:{
                setRequestState(AddWordsRequestState.BackendIssue);
                break;
            }
        }
    })
    .catch( e => {
        setRequestState(AddWordsRequestState.BackendIssue);
        console.log(e);
    });
};

export {
    addWords,
    AddWordsRequestState
}