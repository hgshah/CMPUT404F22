import React, {useState} from "react"
import Sidebar from '../Sidebar'
import News from '../News'
import {NavLink, Routes, Route, Outlet } from "react-router-dom"
//import "./Style.css";
import "./styles/Inbox.css"
import ActivityTab from "./ActivityTab";
import FriendRequestsTab from "./FriendRequestsTab";
import MessagesTab from "./MessagesTab";
import TabDesc from "./TabDesc";
import Tabs from "./Tabs";
import RemPosts from "./RemPosts"
import LogoIcon from "@mui/icons-material/Psychology";
import HomeIcon from "@mui/icons-material/Home"
import ProfileIcon from '@mui/icons-material/Person2';
import InboxIcon from "@mui/icons-material/Mail";
import LoginIcon from '@mui/icons-material/Login';
import { Button } from '@mui/material';

export default function Inbox() {
    //initial selected tab will be activity
    const [currentTab, setCurrentTab] = useState("activity");
    const preferredName = localStorage.getItem("preferredName")
    
    return (
    <div>
        
            <LogoIcon fontSize="large" className="sidebar_logoicon"  /> 
        <div className="list">
            
                <Button> <a href="/login" className="login_link"> <LoginIcon/> Login </a> </Button> <br></br>
                <Button><a href="/home" className="home_link"> <HomeIcon/> Home </a> </Button> <br></br>
                <Button><a href="/profile" className="profile_link"> <ProfileIcon/> Profile </a> </Button> <br></br>
                <Button><a href="/inbox" className="inbox_link"> <InboxIcon/> Inbox </a> </Button>
            
                
            

        </div>
        <div
        
        className="Inbox">
            
            <div className="InboxHeader">
                <h1>Inbox</h1>
                <h3>User: {preferredName}</h3>
            </div>
            <ul className="choose">
                <TabDesc id="activity" title="Activity" currentTab={currentTab} setCurrentTab={setCurrentTab}/>
                <TabDesc id="requests" title="Friend Requests" currentTab={currentTab} setCurrentTab={setCurrentTab}/>
                <TabDesc id="authorlist" title="AuthorList" currentTab={currentTab} setCurrentTab={setCurrentTab}/>
                <TabDesc id="remposts" title="RemPosts" currentTab={currentTab} setCurrentTab={setCurrentTab}/>
            </ul>
            <div className="outlet">
                <Tabs id="activity" currentTab={currentTab}>
                    {/* <p>Activity works</p> */}
                    <ActivityTab />
                </Tabs>
                <Tabs id="requests" currentTab={currentTab}>
                    <FriendRequestsTab />
                </Tabs>
                <Tabs id="authorlist" currentTab={currentTab}>
                    <MessagesTab />
                </Tabs>
                <Tabs id="remposts" currentTab={currentTab}>
                    <RemPosts/>
                </Tabs>
            </div>
        </div>
        {/* <News/> */}
    </div>
  )
}