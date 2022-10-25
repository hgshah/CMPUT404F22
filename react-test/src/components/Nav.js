import { NavLink, Outlet } from "react-router-dom";
import React,{useState} from 'react';
import {FiAlignRight,FiXCircle,FiChevronDown } from "react-icons/fi";
import "./Nav.css";

const Nav = () => {
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
  <div className='nav'>
    <ul className={boxClass.join(' ')} >
      <li><NavLink onClick={toggleClass} className={({ isActive }) => isActive ? "active" : ""} to="/">Home</NavLink></li>
      <li><NavLink onClick={toggleClass} className={({ isActive }) => isActive ? "active" : ""} to="/Profile">Profile</NavLink></li>
      <li><NavLink onClick={toggleClass} className={({ isActive }) => isActive ? "active" : ""} to="/invoice">Inbox</NavLink></li>

      <Outlet />
    </ul>
  </div>
  );
};

export default Nav;
