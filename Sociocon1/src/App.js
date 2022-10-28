import './App.css';
import {BrowserRouter as Router, Route, Routes, Switch } from "react-router-dom";
import Home from './Home';
import Sidebar from './Sidebar';
import Feed from './Feed';
import News from './News';
import Login from './Login';
import Profile from './Profile';
import Inbox from './Inbox';
function App() {
  return (
    // bem
    <Router>
        <div className="app">
          
            
              <Routes>
                <Route path = "/" element = {<Home/>} />
                <Route path = "/login" element = {<Login/>} />
                <Route path = "/profile" element = {<Profile/>} />
                <Route path = "/inbox" element = {<Inbox/>} />
              </Routes>
              
            
       
         </div>


    </Router>
     
    
  );
}

export default App;
