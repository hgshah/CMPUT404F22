// link: https://github.com/CleverProgrammers/twitter-clone
// author: CleverProgrammer: https://www.youtube.com/c/CleverProgrammer/videos
// license: https://www.apache.org/licenses/LICENSE-2.0

import "./Sidebar.css";
import { Link } from "react-router-dom";
import React,{useState} from 'react';
import SidebarOption from "./SidebarOption";
import LogoIcon from "@mui/icons-material/Psychology";
import HomeIcon from "@mui/icons-material/Home"
import ProfileIcon from '@mui/icons-material/Person2';
import InboxIcon from "@mui/icons-material/Mail";

import { Button } from '@mui/material';
function Sidebar(){
   
    return (
 <div className = "sidebar">
    {/* Sidebar option*/}
      
      
      <LogoIcon className="sidebar_logoicon"  /> 
      <div className="list">
         <ul>
            <li> <a href="/login">  Login </a> </li>
            <li> <a href="/home">  Home </a> </li>
            <li> <a href="/profile">  Profile </a> </li>
            <li> <a href="/inbox">  Inbox </a> </li>
         </ul>

      </div>
      
    
    
    {/* <Button variant="outlined" className = "sidebar_post" fullWidth> Post </Button> */}
 </div>
    );
}
export default Sidebar;
