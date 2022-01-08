import wakeBackend from "./TestBackend";
import loadTheme from "./Theme";
import { getSupportedLanguages, Language } from "./GetSupportedLanguages";
import { loginUser, UserLoginRequestState } from "./LoginUser";
import { signupUser, UserSignupRequestState } from "./SignupUser";
import { addWords, AddWordsRequestState } from "./AddWords";
import { getWords, GetWordsRequestState } from "./GetWords";
import { getScore, GetScoreRequestState } from "./GetScore";
import { getUser, GetUserRequestState } from "./GetUser";
import { updateUser, UpdateUserRequestState } from "./UpdateUser";

export {
    // request funcitons
    wakeBackend,
    loadTheme,
    getSupportedLanguages,
    loginUser,
    signupUser,
    addWords,
    getWords,
    getScore,
    getUser,
    updateUser,

    // requests states
    UserLoginRequestState,
    UserSignupRequestState,
    AddWordsRequestState,
    GetWordsRequestState,
    GetScoreRequestState,
    GetUserRequestState,
    UpdateUserRequestState
};
export type { Language };
