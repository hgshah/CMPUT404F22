import { Route, Routes, NavLink, Outlet, BrowserRouter, Navigate } from "react-router-dom";
import React,{useState} from 'react';
import './App.css';
import Sidebar from './Sidebar';
import Feed from './Feed';
import News from './News';
import Inbox from './Inbox';
import Profile from "./Profile";

function App() {
  const [isMenu, setisMenu] = useState(false);
  const [isResponsiveclose, setResponsiveclose] = useState(false);
  const toggleClass = () => {
  };

  let boxClass = ["nav__container"];

  if(isMenu) {
    boxClass.push('responsive__nav__show');
  }else{
    boxClass.push('');
  }
  return (
    // bem
    <div className="app">
      {/*side bar */}
      <Sidebar />

      {/*feed */}
      <Feed />
      {/*widgets */}
      <News /> 

      {/* <ul className={boxClass.join(' ')} >
        
        <li><NavLink onClick={toggleClass} className={({ isActive }) => isActive ? "active" : ""} to="/Profile">Profile</NavLink></li>
        <li><NavLink onClick={toggleClass} className={({ isActive }) => isActive ? "active" : ""} to="/Inbox">Inbox</NavLink></li>
        <Outlet />
      </ul> */}

      {/* <Routes>
        <Route path="/profile" element={<Profile />} /> */}
        
        {/* Approach #2 */}
        {/*inbox*/}
        {/* <Route path="/inbox" element={<Inbox />} />
      </Routes> */}

    </div>
  );
}

export default App;
