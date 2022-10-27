import React from "react";
import "./Sidebar.css";
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
    <SidebarOption active Icon={HomeIcon} text = "Home" />
    <SidebarOption Icon={ProfileIcon} text = "Profile" />
    <SidebarOption Icon = {InboxIcon} text = "Inbox" />
    {/* <Button variant="outlined" className = "sidebar_post" fullWidth> Post </Button> */}
 </div>
    );
}
export default Sidebar;
