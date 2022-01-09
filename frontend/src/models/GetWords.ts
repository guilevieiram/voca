enum GetWordsRequestState{
    NotStarted,
    Started,
    Waiting,
    Successful,
    UserNotFound, 
    BackendIssue
};

type Word = {
    word: string,
    id: number 
};
type setRequestStateType = (requestState: GetWordsRequestState) => void;
type setWordsType = (words: Word[]) => void;

function getWords (userId: number | null, setWords: setWordsType, setRequestState: setRequestStateType, url: string): void {
    const endpoint = `${url}language/get_words`;
    const data = {
        user_id: userId,
    };
    const parameters = {
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
        method: "POST"
    };

    setRequestState(GetWordsRequestState.Started)
    fetch(endpoint, parameters)
    .then( (data) => {
        setRequestState(GetWordsRequestState.Waiting);
        return data.json();
    })
    .then( (response) => {
        console.log(response);
        switch(response.code){
            case 1:{
                setRequestState(GetWordsRequestState.Successful);
                setWords(response.words);
                break;
            }
            case -5:{
                setRequestState(GetWordsRequestState.UserNotFound);
                break;
            }
            default:{
                setRequestState(GetWordsRequestState.BackendIssue);
                break;
            }
        }
    })
    .catch( e => {
        setRequestState(GetWordsRequestState.BackendIssue);
        console.log(e);
    });
};

export {
    GetWordsRequestState,
    getWords
};
export type { Word };
