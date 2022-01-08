enum GetUserRequestState{
    NotStarted,
    Started,
    Waiting,
    Successful,
    UserNotFound,
    BackendIssue,
};

type setRequestStateType = (requestState: GetUserRequestState) => void;
type User = {
    email: string,
    name: string,
    photo: string
};
type setUserType = (user: User) => void;

function getUser (userId: number | null, setUser: setUserType, setRequestState: setRequestStateType, url: string): void {
    const endpoint = `${url}user/get`;
    const data = {
        user_id: userId
    };
    const parameters = {
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
        method: "POST"
    };

    setRequestState(GetUserRequestState.Started)
    fetch(endpoint, parameters)
    .then( (data) => {
        setRequestState(GetUserRequestState.Waiting);
        return data.json();
    })
    .then( (response) => {
        console.log(response);
        switch(response.code){
            case 1:{
                setRequestState(GetUserRequestState.Successful);
                const {name, email, photo_url}= response.user;
                setUser({
                    name: name,
                    email: email,
                    photo: photo_url
                });
                break;
            }
            case -5:{
                setRequestState(GetUserRequestState.UserNotFound);
                break;
            }
            default:{
                setRequestState(GetUserRequestState.BackendIssue);
                break;
            }
        }
    })
    .catch( e => {
        setRequestState(GetUserRequestState.BackendIssue);
        console.log(e);
    });
};

export {
    GetUserRequestState,
    getUser
};