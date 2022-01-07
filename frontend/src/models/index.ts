import wakeBackend from "./TestBackend";
import { loginUser, signupUser, UserLoginRequestState, UserSignupRequestState} from "./UserRequests";
import { getSupportedLanguages, Language } from "./GetSupportedLanguages";
import loadTheme from "./Theme";
import { addWords, AddWordsRequestState} from "./AddWords";
import { getWords, GetWordsRequestState } from "./GetWords";

export {
    wakeBackend,
    loginUser,
    signupUser,
    addWords,
    getWords,
    UserLoginRequestState,
    UserSignupRequestState,
    AddWordsRequestState,
    GetWordsRequestState,
    loadTheme,
    getSupportedLanguages
};
export type { Language };
