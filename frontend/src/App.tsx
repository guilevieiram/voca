import React, { useEffect, useState } from "react";
import Background from "./components/Background";
import Nav from "./components/Nav";
import UserLogin from "./components/user_login";
import UserSignup from "./components/user_signup";
import AddWordsPage from "./components/add_words";
import PlayPage from "./components/play_page";
import NotFoundPage from "./components/NotFoundPage";
import ConfigPage from "./components/config_page";
import UserPage from "./components/user_page";
import HomePage from "./components/home_page";

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

  const [userId, setUserId] = useState<number | null>(null);
  useEffect(() => {
    if (token === null) setUserId(null);
    else setUserId(parseInt(token));
  }, [token]);
  

  useEffect(() => {
    wakeBackend(apiEndpoint);
    loadTheme();
  }, [])

  return (
    <div className={`flex justify-center`}>
      <div className="max-w-xl w-full px-8 ">
        <Router>
          <Routes>
            <Route path='/' element={ifLoggedIn(<HomePage />)}/>
            <Route path="/login" element={ifNotLoggedIn(<UserLogin setToken={setToken}/>)}/>
            <Route path="/signup" element={ifNotLoggedIn(<UserSignup />)}/>
            <Route path="/add_words" element={ifLoggedIn(<AddWordsPage userId={userId}/>)} />
            <Route path="/play" element={ifLoggedIn(<PlayPage userId={userId}/>)} />
            <Route path="/user_page" element={ifLoggedIn(<UserPage userId={userId} />)}/>
            <Route path="/config" element={<ConfigPage />} />
            <Route path='*' element={<NotFoundPage />}/>
          </Routes>

          <Background />
          <Nav />

        </Router>
      </div>
    </div>
  );
}

export default App;
