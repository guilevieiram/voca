import { useState, useEffect } from "react";

import EditableLine from "./EditableLine";
import EditableImage from "./EditableImage";
import Disconnect from "./Disconnect";

import { apiEndpoint } from "../../app.config";

import { getUser, updateUser, GetUserRequestState, UpdateUserRequestState, GetScoreRequestState } from "../../models";

type UserPageProps = {
    userId: number | null
};

type User = {
    email: string,
    name: string,
    photo: string
}

// for now user cannot eddit their photos for i dont know how to do that and I dont care for the moment.
export default function UserPage ({ userId }:UserPageProps): React.ReactElement {
    const [user, setUser] = useState<User>({email: "", name: "", photo: ""});

    const [getUserRequestState, setGetUserRequestState] = useState<GetUserRequestState>(GetUserRequestState.NotStarted);
    const [updateUserRequestState, setUpdateUserRequestState] = useState<UpdateUserRequestState>(UpdateUserRequestState.NotStarted);
    const updateUserData = (key: string, value: string ): void => updateUser(userId, key, value, setUpdateUserRequestState, apiEndpoint);

    useEffect(() => getUser(userId, setUser, setGetUserRequestState, apiEndpoint), []);
    useEffect(() => {
        switch(getUserRequestState){
            case GetUserRequestState.BackendIssue: {
                window.alert("Looks like our servers are down. Try again in a couple of minutes!");
                break;
            }
            case GetUserRequestState.UserNotFound: {
                window.alert("You've been disconnected, please login.");
                sessionStorage.removeItem("token");
                window.location.reload();
                break;
            }
            default: break;
        }
    }, [getUserRequestState]);
    useEffect(() => {
        switch(updateUserRequestState){
            case UpdateUserRequestState.Successful: {
                window.alert("Information updated successfully.");
                break;
            }
            case UpdateUserRequestState.BackendIssue: {
                window.alert("Looks like our servers are down. Try again in a couple of minutes!");
                break;
            }
            case UpdateUserRequestState.UserNotFound: {
                window.alert("You've been disconnected, please login.");
                sessionStorage.removeItem("token");
                window.location.reload();
                break;
            }
            default: break;
        }
    }, [updateUserRequestState]);

    return (
        <div className="w-full">
            <h1 className="page-title">User page</h1>
            <div className="h-bar mb-10"></div>
            <EditableImage apiKey="user_profile" placeholder={user.photo} changeFunction={updateUserData} />
            <EditableLine apiKey="user_name" label="Name" placeholder={user.name} inputType="text" changeFunction={updateUserData}/>
            <EditableLine apiKey="user_email" label="E-mail" placeholder={user.email} inputType="email" changeFunction={updateUserData}/>
            <Disconnect />
        </div>
    )
};