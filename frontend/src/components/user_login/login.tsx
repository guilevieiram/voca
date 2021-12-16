import React from "react";
import ForgotPassword from './ForgotPassword';
import LoginForm from './LoginForm';

type UserLoginProps = {
    darkMode: boolean,
    setToken: (token: string) => void
};
function UserLogin ({darkMode, setToken}: UserLoginProps): React.ReactElement {
    return(
       <div className={`w-full h-screen py-10`}>
            <h1 className={`page-title text-${darkMode ? 'light' : 'dark'}`}>Login</h1>
            <div className="flex flex-col justify-between h-full ">
                <LoginForm darkMode={darkMode} setToken={setToken}/>
                <ForgotPassword />
            </div>
       </div> 
    )
};

export default UserLogin;