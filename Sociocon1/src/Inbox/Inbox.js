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


// const tabList = [
//     {
//       id: 'all',
//       label: 'All',
//     },
//     {
//       id: 'mentions',
//       label: 'Mentions',
//     },
//   ]

export default function Inbox() {
    //initial selected tab will be activity
    const [currentTab, setCurrentTab] = useState("requests");
    
    // Handle when user changes tabs
    function handleActivityTab() {
        setCurrentTab("activity")
    }

    function handleRequestsTab() {
        setCurrentTab("requests")
    }

    function handleMessagesTab() {
        setCurrentTab("messages")
    }

    return (
    <div>
        <Sidebar/>
        
        <div
        
        className="Inbox">
            
            <div className="InboxHeader">
                <h1>Inbox</h1>
            </div>
            <ul className="choose">
                <TabDesc id="activity" title="Activity" currentTab={currentTab} setCurrentTab={setCurrentTab}/>
                <TabDesc id="requests" title="Friend Requests" currentTab={currentTab} setCurrentTab={setCurrentTab}/>
                <TabDesc id="messages" title="Messages" currentTab={currentTab} setCurrentTab={setCurrentTab}/>
                {/* <li className={currentTab === "activity" ? "current" : ""}
                onClick={handleActivityTab}>Activity</li>
                <li className={currentTab === "requests" ? "current" : ""}
                onClick={handleRequestsTab}>Friend Requests</li>
                <li className={currentTab === "messages" ? "current" : ""}
                onClick={handleMessagesTab}>Messages</li> */}
                
            </ul>
            <div className="outlet">
                <Tabs id="activity" currentTab={currentTab}>
                    {/* <p>Activity works</p> */}
                    <ActivityTab />
                </Tabs>
                <Tabs id="requests" currentTab={currentTab}>
                    <FriendRequestsTab />
                </Tabs>
                <Tabs id="messages" currentTab={currentTab}>
                    <MessagesTab />
                </Tabs>
                {/* {currentTab === "activity" ? <ActivityTab /> : ""}
                {currentTab === "requests" ? <FriendRequestsTab /> : ""}
                {currentTab === "messages" ? <MessagesTab /> : ""} */}
            </div>
        </div>
    </div>
  )
}