import React, { Component, useEffect, useState } from "react";
import Background from "./components/Background";
import Nav from "./components/Nav";
import UserLogin from "./components/user_login";
import UserSignupPage from "./components/user_signup";
import NotFoundPage from "./components/NotFoundPage";
import HomePage from "./components/HomePage";

import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate
} from 'react-router-dom';

function App(): React.ReactElement {
  const [darkMode, setDarkMode] = useState<boolean>(false);
  const toggleDarkMode = (): void => setDarkMode(!darkMode);

  const setToken = (userToken: string): void => sessionStorage.setItem('token', userToken);
  const getToken = (): string | null => sessionStorage.getItem('token');
  const token: string | null = getToken()
  const protect = (element: React.ReactElement): React.ReactElement => token ? element : <Navigate replace to="/login" />;

  return (
    <div className={`flex justify-center`}>
      <Background darkMode={darkMode} />
      <Nav darkMode={darkMode} />

      <div className="max-w-xl w-full px-8 ">
        <Router>
          <Routes>
            <Route path='/' element={protect(<HomePage darkMode={darkMode} />)}/>
            <Route path="/login" element={<UserLogin darkMode={darkMode} setToken={setToken}/>}/>
            <Route path="/signup" element={<UserSignupPage darkMode={darkMode} />}/>
            <Route path='*' element={<NotFoundPage darkMode={darkMode} />}/>
          </Routes>
        </Router>
      </div>
    </div>
  );
}

export default App;
