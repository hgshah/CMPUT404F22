import React from 'react'
import Sidebar from './Sidebar'
import {useState} from 'react';
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
    </div>
  )
}

export default Login
