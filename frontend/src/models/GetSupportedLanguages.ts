type Language = {
    name: string,
    flag: string,
    code: string
}
type setLanguagesType = (languages: Language[]) => void;

async function getSupportedLanguages(url: string, setLanguages: setLanguagesType) {

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
                break;
            }
            default:{
                break;
            }
        }
    })
    .catch(e => {console.log(e)})
}

export {
    getSupportedLanguages
};
export type { Language };
