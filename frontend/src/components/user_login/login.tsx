import React from "react";
import ForgotPassword from './ForgotPassword';
import LoginForm from './LoginForm';

type UserLoginProps = {
    darkMode: boolean
};
function UserLogin ({darkMode}: UserLoginProps): React.ReactElement {
    return(
       <div className={`w-full h-screen py-10`}>
            <h1 className={` mx-4 filter drop-shadow-md text-${darkMode ? 'light' : 'dark'}`}>Login</h1>
            <div className="flex flex-col justify-between h-full ">
                <LoginForm darkMode={darkMode}/>
                <ForgotPassword />
            </div>

       </div> 
    )
};

export default UserLogin;