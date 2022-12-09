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
import LoginIcon from '@mui/icons-material/Login';
import { Button } from '@mui/material';
function Sidebar(){
   
   return (
 <div className = "sidebar">
    {/* Sidebar option*/}
      
      
      <LogoIcon fontSize="large" className="sidebar_logoicon"  /> 
      <div className="list">
         
            <Button> <a href="/login" className="login_link"> <LoginIcon/> Login </a> </Button> <br></br>
            <Button><a href="/home" className="home_link"> <HomeIcon/> Home </a> </Button> <br></br>
            <Button><a href="/profile" className="profile_link"> <ProfileIcon/> Profile </a> </Button> <br></br>
            <Button><a href="/inbox" className="inbox_link"> <InboxIcon/> Inbox </a> </Button>
         
            
         

      </div>
      
    
    
    {/* <Button variant="outlined" className = "sidebar_post" fullWidth> Post </Button> */}
 </div>
    );
}
export default Sidebar;
