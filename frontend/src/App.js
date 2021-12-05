import {useState} from 'react';
import {
  HashRouter as Router,
  Route,
  Routes,
  Link
} from "react-router-dom";

import Nav from './components/Nav';
import Background from './components/Background';
import Login from './components/userLogin';

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const toggleMode = () => setDarkMode(!darkMode)
  const [sessionID, setSessionID] = useState(0)

  return (
    <Router basename="/" >

      <Background darkMode={darkMode}/>
      <Nav/>

      <Routes>
        <Route exact path="/" element={
          <p>Home</p>
        }></Route>
        <Route path="/login" element={
          <Login darkMode={darkMode}/>
        }></Route>
      </Routes>
    </Router>
  );
}

export default App;