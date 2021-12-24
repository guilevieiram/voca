import React from "react";
import RedirectToSignup from './RedirectToSignup';
import LoginForm from './LoginForm';

type UserLoginProps = {
    setToken: (token: string) => void
};

export default function UserLogin ({setToken}: UserLoginProps): React.ReactElement {
    return(
       <div className={`w-full h-screen py-10`}>
            <h1 className={`page-title text-dark dark:text-light`}>Login</h1>
            <div className="flex flex-col justify-between h-full ">
                <LoginForm setToken={setToken}/>
                <RedirectToSignup />
            </div>
       </div> 
    )
};