import ExplanatoryText from "./ExplanatoryText"
import Tutorial from "./Tutorial"
import Feedback from "./Feedback"
import GoToLogin from "./GoToLogin";

import vocaLogoLight from '../../assets/voca-logo-light.svg';
import vocaLogoDark from '../../assets/voca-logo-dark.svg';

const getLogo = (): string => {
    if(localStorage.theme === "light") return vocaLogoLight
    else return vocaLogoDark;
}

export default function HomePage (): React.ReactElement {
    return (
        <div className="w-full my-10 mb-40">
            <img src={getLogo()} alt="" className="mx-auto my-10 h-24 "/>
            <ExplanatoryText/>
            <GoToLogin />
            
            <Tutorial />
            <Feedback />
        </div>
    )
};