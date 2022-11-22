import React from 'react'
import Sidebar from './Sidebar'
import {useState} from 'react';
import {Button} from '@mui/material';
import "./Login.css";

function Login() {
    const[value, setValue] = useState(""); 
    function handle() {
        alert("You are logged in")
    }
  return (
    <div className='login'>

        <div className='username'>
            <form>
                <input type="text" placeholder="Username" value={value} onChange={(e) => {setValue(e.target.value)}} />
            </form>
        </div>

        <div className='password'>
            <form>
                <input type="text" placeholder="Password" value={value} onChange={(e) => {setValue(e.target.value)}} />
            </form>
        </div>
        
        <div className='login_btn'>
            <Button onClick={handle}>Login</Button>
        </div>

            {/* <div className='username'>
                <input className='username_input' type="text" placeholder="Enter user name" value={value} onChange={(e) => {setValue(e.target.value)}} />
            </div>
            <div className="password">
                <input type="text" placeholder="Password" />
            </div>
                <div className="login_button">
                    <Button onClick={handle}>Login</Button>
            </div> */}
    </div>
  )
}

export default Login
