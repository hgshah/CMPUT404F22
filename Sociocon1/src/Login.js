import React from 'react'
import Sidebar from './Sidebar'
import {useState} from 'react';
import {TestFetcher} from "./page/TestFetcher";
function Login() {
    const[value, setValue] = useState(""); 
    function handle() {
        alert("You are logged in")
    }
  return (
    <div className='login'>
            <div className='username'>
                <input type="text" placeholder="Enter user name" value={value} onChange={(e) => {setValue(e.target.value)}} />
            </div>
            <div className="password">
                <input type="text" placeholder="password" />
            </div>
                <div className="login_button">
                    <button onClick={handle}>Login</button>
            </div>
            {
                /*
                Hello! let me inject my TestFetcher!
                Do not delete. We'll use this as reference!
                */
                TestFetcher()
            }
    </div>
  )
}

export default Login
