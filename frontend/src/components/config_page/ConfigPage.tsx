import DarkModeConfig from "./DarkModeConfig";

export default function ConfigPage () {
    return(
        <div className="my-10">
            <h1 className="my-6 text-dark dark:text-light">Configurations</h1>
            <div className="w-full h-px border-dark bg-dark dark:bg-light"></div>
            <DarkModeConfig />
        </div>
    )
}