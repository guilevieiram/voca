enum UserSignupRequestState {
    NotStarted,
    Started,
    Waiting,
    Successful,
    EmailInUse,
    BackendIssue
};

type setSignupStateType = (signupState: UserSignupRequestState) => void;

const signupUser = (name: string, email: string, password: string, language: string, setSignupState: setSignupStateType, url: string) => {
    const endpoint: string = `${url}/user/signup`;
    const data = {
        user_name: name,
        user_email: email,
        user_password: password,
        user_language: language,
        user_photo: `https://avatars.dicebear.com/api/croodles-neutral/${email}svg`
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
    UserSignupRequestState,
    signupUser
}