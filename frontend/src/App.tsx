import React, { useEffect } from "react";
import Background from "./components/Background";
import Nav from "./components/Nav";
import UserLogin from "./components/user_login";
import UserSignup from "./components/user_signup";
import NotFoundPage from "./components/NotFoundPage";
import HomePage from "./components/HomePage";
import ConfigPage from "./components/config_page";

import { loadTheme } from "./models";

import {
  HashRouter as Router,
  Route,
  Routes,
  Navigate
} from 'react-router-dom';

import { wakeBackend } from "./models";
import { apiEndpoint } from "./app.config";

function App(): React.ReactElement {

  const setToken = (userToken: string): void => sessionStorage.setItem('token', userToken);
  const getToken = (): string | null => sessionStorage.getItem('token');
  const token: string | null = getToken();
  const ifLoggedIn = (element: React.ReactElement): React.ReactElement => token ? element : <Navigate replace to="/login" />;
  const ifNotLoggedIn = (element: React.ReactElement): React.ReactElement => !token ? element : <Navigate replace to="/" />;

  useEffect(() => {
    wakeBackend(apiEndpoint);
    loadTheme();
  }, [])

  return (
    <div className={`flex justify-center`}>
      <div className="max-w-xl w-full px-8 ">
        <Router>
          <Background />
          <Nav />
          <Routes>
            <Route path='/' element={ifLoggedIn(<HomePage />)}/>
            <Route path="/login" element={ifNotLoggedIn(<UserLogin setToken={setToken}/>)}/>
            <Route path="/signup" element={ifNotLoggedIn(<UserSignup />)}/>
            <Route path="/config" element={<ConfigPage />} />
            <Route path='*' element={<NotFoundPage />}/>
          </Routes>
        </Router>
      </div>
    </div>
  );
}

export default App;
