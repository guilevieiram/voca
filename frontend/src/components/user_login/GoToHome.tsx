import {Link} from "react-router-dom";
type GoToHomeProps = {}
export default function GoToHome({}: GoToHomeProps): React.ReactElement {
    return (
        <div className="mb-10">
            <h2 className=" text-lg">Want to know more?</h2>
            <Link to="/home" 
                className=" text-blue hover:text-dark dark:hover:text-light "
            >
                Check out our home page!
            </Link>

        </div>
    )
}