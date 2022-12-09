import './App.css';
import {BrowserRouter as Router, Route, Routes, Switch } from "react-router-dom";
import Home from './Homepage/Home';
import Sidebar from './Sidebar';
import Feed from './Homepage/Feed';
import News from './News';
import Login from './Login';
import Profile from './MyProfile/Profile';
import Inbox from './Inbox/Inbox';
import {Button} from '@mui/material';

function App() {
  // const defaultDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  // const [theme, setTheme] = useLocalStorage('theme', defaultDark ? 'dark' : 'light');

  // const switchTheme = () => {
  //   const newTheme = theme === 'light' ? 'dark' : 'light'
  //   setTheme(newTheme)
  // }

  return (
    // bem
    <Router>
      {/* <div className="app" data-theme={theme}> */}
        <div className="app">
          {/* <Button onClick={switchTheme}>
            Switch to {theme === 'light' ? 'Dark' : 'Light'} Theme
          </Button> */}
        {/* link: https://www.youtube.com/watch?v=Ul3y1LXxzdU
            author: https://www.youtube.com/c/WebDevSimplified 
            License: https://creativecommons.org/choose/ */}
            
              <Routes>
                <Route path = "/login" element = {<Login/>} />
                <Route path = "/" element = {<Login/>} />
                <Route path = "/home" element = {<Home/>} />
                <Route path = "/profile" element = {<Profile/>} />
                <Route path = "/inbox" element = {<Inbox/>} />
              </Routes>
              
            
       
         </div>


    </Router>
     
    
  );
}

export default App;
