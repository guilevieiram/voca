enum UpdateUserRequestState{
    NotStarted,
    Started,
    Waiting,
    Successful,
    UserNotFound,
    BackendIssue,
    ValueNotValid
};

type setRequestStateType = (requestState: UpdateUserRequestState) => void;

function updateUser (userId: number | null, property: string, value: string, setRequestState: setRequestStateType, url: string): void {
    const endpoint = `${url}user/update`;
    const data = {
        user_id: userId,
        property: property,
        value: value
    };
    const parameters = {
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
        method: "POST"
    };

    setRequestState(UpdateUserRequestState.Waiting)
    fetch(endpoint, parameters)
    .then( (data) => {
        return data.json();
    })
    .then( (response) => {
        console.log(response);
        switch(response.code){
            case 1:{
                setRequestState(UpdateUserRequestState.Successful);
                break;
            }
            case -5:{
                setRequestState(UpdateUserRequestState.UserNotFound);
                break;
            }
            default:{
                setRequestState(UpdateUserRequestState.BackendIssue);
                break;
            }
        }
    })
    .catch( e => {
        setRequestState(UpdateUserRequestState.BackendIssue);
        console.log(e);
    });
};

export {
    UpdateUserRequestState,
    updateUser 
}