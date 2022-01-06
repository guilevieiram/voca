import DarkModeConfig from "./DarkModeConfig";

export default function ConfigPage () {
    return(
        <div className="">
            <h1 className="page-title ">Configurations</h1>
            <div className="w-full h-px border-dark bg-dark dark:bg-light"></div>
            <DarkModeConfig />
        </div>
    )
}