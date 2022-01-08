enum UserLoginRequestState {
    NotStarted,
    Started,
    Waiting,
    Successful,
    WrongPassword,
    UserNotFound,
    BackendIssue
};

type setTokenType = (id: string) => void;
type setLoginStateType = (loginState: UserLoginRequestState) => void;

const loginUser = (email: string, password: string, setToken: setTokenType, setLoginState: setLoginStateType, url: string) => {
    const endpoint: string = `${url}user/login`;
    const data = {
        user_email: email,
        password: password
    };
    const parameters = {
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
        method: "POST"
    };

    setLoginState(UserLoginRequestState.Started);
    fetch(endpoint, parameters)
    .then( (data) => {
        setLoginState(UserLoginRequestState.Waiting);
        return data.json();
    })
    .then( (response) => {
        console.log(response)
        switch(response.code){
            case 1:{
                setLoginState(UserLoginRequestState.Successful);
                setToken(response.id);
                break;
            }
            case -2:{
                setLoginState(UserLoginRequestState.WrongPassword);
                break;
            }
            case -1:{
                setLoginState(UserLoginRequestState.UserNotFound);
                break;
            }
            default:{
                setLoginState(UserLoginRequestState.BackendIssue);
                break;
            }
        }
    })
    .catch( e => {
        setLoginState(UserLoginRequestState.BackendIssue);
        console.log(e);
    });
};

export {
    UserLoginRequestState,
    loginUser
};