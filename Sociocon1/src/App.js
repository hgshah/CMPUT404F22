import './App.css';
import {BrowserRouter as Router, Route, Routes, Switch } from "react-router-dom";
import Home from './Homepage/Home';
import Sidebar from './Sidebar';
import Feed from './Homepage/Feed';
import News from './News';
import Login from './Login';
import Profile from './Profile';
import Inbox from './Inbox/Inbox';
function App() {
  return (
    // bem
    <Router>
        <div className="app">
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
