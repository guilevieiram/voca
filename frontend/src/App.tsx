import { useState } from "react";
import Background from "./components/Background";
import Nav from "./components/Nav";
import UserLogin from "./components/user_login";
import NotFoundPage from "./components/NotFoundPage";
import HomePage from "./components/HomePage";

import {
  BrowserRouter as Router,
  Route,
  Routes
} from 'react-router-dom';

function App(): React.ReactElement {
  const [darkMode, setDarkMode] = useState<boolean>(true);
  const toggleDarkMode = (): void => setDarkMode(!darkMode);
  const [userId, setUserId] = useState<number | null>(null);

  return (
    <div className={`flex justify-center`}>
      <Background darkMode={darkMode} />
      <Nav darkMode={darkMode} />

      <div className="max-w-xl w-full px-8 ">
        <Router>
          <Routes>
            <Route path='/' element={<HomePage darkMode={darkMode} />}/>
            <Route path="/login" element={<UserLogin darkMode={darkMode} />}/>
            <Route path='*' element={<NotFoundPage darkMode={darkMode} />}/>
          </Routes>
        </Router>
      </div>
    </div>
  );
}

export default App;
