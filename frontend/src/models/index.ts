import wakeBackend from "./TestBackend";
import { loginUser, signupUser, UserLoginRequestState, UserSignupRequestState} from "./UserRequests";
import { getSupportedLanguages, Language } from "./GetSupportedLanguages";
import loadTheme from "./Theme";
import { addWords, AddWordsRequestState} from "./AddWords";
export {
    wakeBackend,
    loginUser,
    signupUser,
    addWords,
    UserLoginRequestState,
    UserSignupRequestState,
    AddWordsRequestState,
    loadTheme,
    getSupportedLanguages
};
export type { Language };
