export default async function wakeBackend (url: string = "https://voca-backend.herokuapp.com") {
    const endpoint: string = url;
    const parameters: any = {
        headers: {
            "Content-Type": "application/json"
        },
        method: "GET"
    }
    await fetch(endpoint, parameters)
    .then(data => data.json())
    .then(response => {
        console.log(response);
    })
    .catch(e => {console.log(e)})
}