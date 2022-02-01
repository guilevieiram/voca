import wakeBackend from "./TestBackend";
import loadTheme from "./Theme";
import { getSupportedLanguages, Language } from "./GetSupportedLanguages";
import { loginUser, UserLoginRequestState } from "./LoginUser";
import { signupUser, UserSignupRequestState } from "./SignupUser";
import { addWords, AddWordsRequestState } from "./AddWords";
import { getWords, GetWordsRequestState, Word } from "./GetWords";
import { getScore, GetScoreRequestState } from "./GetScore";
import { getUser, GetUserRequestState } from "./GetUser";
import { updateUser, UpdateUserRequestState } from "./UpdateUser";
import { deleteWord, DeleteWordRequestState } from "./DeleteWord";

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
    deleteWord,

    // requests states
    UserLoginRequestState,
    UserSignupRequestState,
    AddWordsRequestState,
    GetWordsRequestState,
    GetScoreRequestState,
    GetUserRequestState,
    UpdateUserRequestState,
    DeleteWordRequestState,
};
export type { Language, Word };
