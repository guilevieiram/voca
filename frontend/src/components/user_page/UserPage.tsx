import EditableLine from "./EditableLine";
import EditableImage from "./EditableImage";
import { useState, useEffect } from "react";

type UserPageProps = {

};

type User = {
    email: string,
    name: string,
    photo: string
}

// for now user cannot eddit their photos for i dont know how to do that and I dont care for the moment.
export default function UserPage ({ }:UserPageProps): React.ReactElement {
    const [user, setUser] = useState<User>({email: "", name: "", photo: ""});
    
    // dummy update user data funcion. Later will be changed to the actual api call.
    const updateUserData = (key: string, value: string ): void =>  {
        console.log(`Changing user ${key} to value ${value}`);
    };

    useEffect(() => {
        //needs to be changed by the api call who will fetch the user data
        setUser({
            name: "Guilherme Vieira",
            email: "guile@gmail.com",
            photo: "https://icatcare.org/app/uploads/2018/07/Thinking-of-getting-a-cat.png"
        });
    }, []);

    return (
        <div className="w-full">
            <h1 className="page-title">User page</h1>
            <div className="h-bar mb-10"></div>
            <EditableImage apiKey="user_profile" placeholder={user.photo} changeFunction={updateUserData} />
            <EditableLine apiKey="user_name" label="Name" placeholder={user.name} inputType="text" changeFunction={updateUserData}/>
            <EditableLine apiKey="user_email" label="E-mail" placeholder={user.email} inputType="email" changeFunction={updateUserData}/>
        </div>
    )
};