import wakeBackend from "./TestBackend";
import loadTheme from "./Theme";
import { getSupportedLanguages, Language } from "./GetSupportedLanguages";
import { loginUser, UserLoginRequestState } from "./LoginUser";
import { signupUser, UserSignupRequestState } from "./SignupUser";
import { addWords, AddWordsRequestState } from "./AddWords";
import { getWords, GetWordsRequestState } from "./GetWords";
import { getScore, GetScoreRequestState } from "./GetScore";

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

    // requests states
    UserLoginRequestState,
    UserSignupRequestState,
    AddWordsRequestState,
    GetWordsRequestState,
    GetScoreRequestState
};
export type { Language };
