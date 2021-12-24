enum UserLoginRequestState {
    NotStarted,
    Started,
    Waiting,
    Successful,
    WrongPassword,
    UserNotFound,
    BackendIssue
};
enum UserSignupRequestState {
    NotStarted,
    Started,
    Waiting,
    Successful,
    EmailInUse,
    BackendIssue
};

type setTokenType = (id: string) => void;
type setLoginStateType = (loginState: UserLoginRequestState) => void;
type setSignupStateType = (signupState: UserSignupRequestState) => void;

const loginUser = (email: string, password: string, setToken: setTokenType, setLoginState: setLoginStateType, url: string) => {
    const endpoint: string = `${url}/user/login`;
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

const signupUser = (name: string, email: string, password: string, language: string, setSignupState: setSignupStateType, url: string) => {
    const endpoint: string = `${url}/user/signup`;
    const data = {
        user_name: name,
        user_email: email,
        user_password: password,
        user_language: language,
        user_photo: ""
    };
    const parameters = {
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
        method: "POST"
    };

    setSignupState(UserSignupRequestState.Started);
    fetch(endpoint, parameters)
    .then( (data) => {
        setSignupState(UserSignupRequestState.Waiting);
        return data.json();
    })
    .then( (response) => {
        console.log(response);
        switch(response.code){
            case 1:{
                setSignupState(UserSignupRequestState.Successful);
                break;
            }
            case -6:{
                setSignupState(UserSignupRequestState.EmailInUse);
                break;
            }
            default:{
                setSignupState(UserSignupRequestState.BackendIssue);
                console.log("user signup request, default case");
                break;
            }
        }
    })
    .catch( e => {
        setSignupState(UserSignupRequestState.BackendIssue);
        console.log(e);
    });
};

export {
    UserLoginRequestState,
    UserSignupRequestState,
    loginUser,
    signupUser
}
