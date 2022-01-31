enum GetScoreRequestState{
    NotStarted,
    Started,
    Waiting,
    Successful,
    UserNotFound,
    BackendIssue,
    // still don't know if we should give user this level of detail
    TranslationError,
    NlpError
};

type setRequestStateType = (requestState: GetScoreRequestState) => void;
type setScoreType = (setScore: number) => void;

function getScore (wordId: number, word: string, setScore: setScoreType, setRequestState: setRequestStateType, url: string): void {
    const endpoint = `${url}language/score`;
    const data = {
        word_id: wordId,
        word: word
    };
    const parameters = {
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
        method: "POST"
    };

    setRequestState(GetScoreRequestState.Waiting)
    fetch(endpoint, parameters)
    .then( (data) => {
        return data.json();
    })
    .then( (response) => {
        console.log(response);
        switch(response.code){
            case 1:{
                setRequestState(GetScoreRequestState.Successful);
                setScore(response.score);
                break;
            }
            case -5:{
                setRequestState(GetScoreRequestState.UserNotFound);
                break;
            }
            case -9: case -10: case -14: {
                setRequestState(GetScoreRequestState.TranslationError);
                break;
            }
            case -11: {
                setRequestState(GetScoreRequestState.NlpError);
                break;
            }
            default:{
                setRequestState(GetScoreRequestState.BackendIssue);
                break;
            }
        }
    })
    .catch( e => {
        setRequestState(GetScoreRequestState.BackendIssue);
        console.log(e);
    });
};

export {
    GetScoreRequestState,
    getScore 
}