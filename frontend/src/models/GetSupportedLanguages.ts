type Language = {
    name: string,
    flag: string,
    code: string
}
type setLanguagesType = (languages: Language[]) => void;
type setSuccessType = (state: boolean) => void;

async function getSupportedLanguages(url: string, setLanguages: setLanguagesType, setSuccess: setSuccessType ) {

    const endpoint: string = `${url}language/supported_languages`;
    const parameters: any = {
        headers: {
            "Content-Type": "application/json"
        },
        method: "GET"
    }

    await fetch(endpoint, parameters)
    .then(data => data.json())
    .then(response => {
        switch (response.code){
            case 1:{
                setLanguages(response.languages);
                setSuccess(true);
                break;
            }
            default:{
                window.alert("Looks like our servers are down for the moment... Try again later!");
                setSuccess(false);
                break;
            }
        }
    })
    .catch(e => {
        console.log(e);
        setSuccess(false);
    })
}

export {
    getSupportedLanguages
};
export type { Language };
